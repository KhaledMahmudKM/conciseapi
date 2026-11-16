"""Chapter 11: versions, deprecation, request IDs and structured logs.

Run:   fastapi dev library_ops.py
Try:   curl -i http://127.0.0.1:8000/v1/books/1
       curl -i http://127.0.0.1:8000/v2/books/1
"""
import json
import logging
import time
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, FastAPI, HTTPException, Request, Response

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("library")

app = FastAPI(title="Library API", version="2.0.0")

BOOKS = {
    1: {"id": 1, "title": "Good Omens", "authors": ["Terry Pratchett", "Neil Gaiman"], "year": 1990},
    2: {"id": 2, "title": "Emma", "authors": ["Jane Austen"], "year": 1815},
}

DEPRECATED_AT = datetime(2026, 9, 1, tzinfo=timezone.utc)
SUNSET_AT = datetime(2027, 3, 1, tzinfo=timezone.utc)


# ---------------------------------------------------------------- middleware: request IDs, timing, logs
@app.middleware("http")
async def observe(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    start = time.perf_counter()
    response = await call_next(request)
    ms = (time.perf_counter() - start) * 1000
    response.headers["X-Request-ID"] = request_id          # the client can quote it in a support ticket
    response.headers["Server-Timing"] = f"app;dur={ms:.1f}"
    log.info(json.dumps({"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                         "request_id": request_id, "method": request.method,
                         "path": request.url.path, "status": response.status_code,
                         "duration_ms": round(ms, 1)}))
    return response


def find(book_id: int) -> dict:
    if book_id not in BOOKS:
        raise HTTPException(404, "No such book")
    return BOOKS[book_id]


# ---------------------------------------------------------------- v1: one author as a string (deprecated)
v1 = APIRouter(prefix="/v1", tags=["v1 (deprecated)"], deprecated=True)


@v1.get("/books/{book_id}")
def get_book_v1(book_id: int, response: Response):
    b = find(book_id)
    response.headers["Deprecation"] = f"@{int(DEPRECATED_AT.timestamp())}"       # RFC 9745
    response.headers["Sunset"] = SUNSET_AT.strftime("%a, %d %b %Y %H:%M:%S GMT")  # RFC 8594
    response.headers["Link"] = f'</v2/books/{book_id}>; rel="successor-version"'
    return {"id": b["id"], "title": b["title"], "author": ", ".join(b["authors"]), "year": b["year"]}


# ---------------------------------------------------------------- v2: a list of authors (breaking change)
v2 = APIRouter(prefix="/v2", tags=["v2"])


@v2.get("/books/{book_id}")
def get_book_v2(book_id: int):
    return find(book_id)


app.include_router(v1)
app.include_router(v2)


@app.get("/health")
def health():
    return {"status": "ok"}
