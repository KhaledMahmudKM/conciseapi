"""Chapter 10: caching, rate limiting, idempotency and long-running jobs.

Run:   fastapi dev library_perf.py
Try:   curl -i http://127.0.0.1:8000/books/1
       curl -i http://127.0.0.1:8000/books/1 -H 'If-None-Match: "<etag from the first response>"'
"""
import hashlib
import json
import threading
import time
import uuid

from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Library API: performance and reliability")

BOOKS = {1: {"id": 1, "title": "Dune", "year": 1965}, 2: {"id": 2, "title": "Emma", "year": 1815}}


# ---------------------------------------------------------------- 1. conditional requests and caching
def etag_of(obj) -> str:
    digest = hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:16]
    return f'"{digest}"'


@app.get("/books/{book_id}")
def get_book(book_id: int, response: Response, if_none_match: str | None = Header(default=None)):
    book = BOOKS.get(book_id)
    if book is None:
        raise HTTPException(404, "No such book")
    tag = etag_of(book)
    headers = {"ETag": tag, "Cache-Control": "private, max-age=60"}
    if if_none_match == tag:                       # the client's copy is still current
        return Response(status_code=304, headers=headers)
    response.headers.update(headers)
    return book


@app.put("/books/{book_id}")
def put_book(book_id: int, book: dict, if_match: str | None = Header(default=None)):
    current = BOOKS.get(book_id)
    if current is None:
        raise HTTPException(404, "No such book")
    if if_match is None:
        raise HTTPException(428, "Send If-Match with the ETag you last read")
    if if_match != etag_of(current):               # someone else changed it since you read it
        raise HTTPException(412, "The book changed; read it again")
    BOOKS[book_id] = {"id": book_id, "title": str(book.get("title")), "year": book.get("year")}
    return BOOKS[book_id]


# ---------------------------------------------------------------- 2. rate limiting (token bucket)
RATE = 5            # tokens added per second
BURST = 10          # bucket size
buckets: dict[str, tuple[float, float]] = {}
lock = threading.Lock()


def take_token(client: str) -> tuple[bool, float, float]:
    """Return (allowed, tokens_left, seconds_until_next_token)."""
    now = time.monotonic()
    with lock:
        tokens, last = buckets.get(client, (BURST, now))
        tokens = min(BURST, tokens + (now - last) * RATE)
        allowed = tokens >= 1
        if allowed:
            tokens -= 1
        buckets[client] = (tokens, now)
    return allowed, tokens, (1 - tokens) / RATE if tokens < 1 else 0.0


@app.middleware("http")
async def rate_limit(request: Request, call_next):
    if not request.url.path.startswith("/limited"):
        return await call_next(request)
    client = request.headers.get("X-API-Key") or request.client.host
    allowed, left, wait = take_token(client)
    if not allowed:
        retry = max(1, round(wait + 0.5))
        return JSONResponse({"title": "Too Many Requests", "status": 429},
                            status_code=429, headers={"Retry-After": str(retry),
                                                      "X-RateLimit-Limit": str(BURST),
                                                      "X-RateLimit-Remaining": "0"})
    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(BURST)
    response.headers["X-RateLimit-Remaining"] = str(int(left))
    return response


@app.get("/limited/books")
def limited_books():
    return list(BOOKS.values())


# ---------------------------------------------------------------- 3. idempotency keys
class OrderIn(BaseModel):
    book_id: int
    quantity: int = 1


orders: dict[str, dict] = {}
idempotency: dict[str, tuple[str, dict]] = {}       # key -> (request fingerprint, stored response)


@app.post("/orders", status_code=201)
def create_order(order: OrderIn, response: Response, idempotency_key: str = Header()):
    fingerprint = hashlib.sha256(order.model_dump_json().encode()).hexdigest()
    if idempotency_key in idempotency:
        seen_fp, stored = idempotency[idempotency_key]
        if seen_fp != fingerprint:
            raise HTTPException(422, "Idempotency-Key reused with a different request")
        response.headers["Idempotent-Replayed"] = "true"
        return stored                              # same answer, no second order
    new = {"id": str(uuid.uuid4()), **order.model_dump()}
    orders[new["id"]] = new
    idempotency[idempotency_key] = (fingerprint, new)
    return new


# ---------------------------------------------------------------- 4. long-running work: 202 Accepted
jobs: dict[str, dict] = {}


def build_report(job_id: str) -> None:
    jobs[job_id]["status"] = "running"
    time.sleep(2)                                   # pretend this is slow
    jobs[job_id].update(status="done", result={"books": len(BOOKS)})


@app.post("/reports", status_code=202)
def start_report(background: BackgroundTasks, response: Response):
    job_id = uuid.uuid4().hex[:8]
    jobs[job_id] = {"id": job_id, "status": "queued"}
    background.add_task(build_report, job_id)
    response.headers["Location"] = f"/reports/{job_id}"
    response.headers["Retry-After"] = "1"
    return jobs[job_id]


@app.get("/reports/{job_id}")
def report_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(404, "No such job")
    return jobs[job_id]
