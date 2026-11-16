"""Chapter 10: a client that retries politely.

Start the server:   fastapi dev library_perf.py
Then run:           python retry_client.py
"""
import random
import time
import uuid

import requests

BASE = "http://127.0.0.1:8000"
RETRYABLE = {429, 502, 503, 504}


def call_with_retries(method: str, url: str, attempts: int = 5, **kwargs) -> requests.Response:
    """Retry on timeouts and retryable status codes, with exponential backoff and full jitter."""
    for attempt in range(attempts):
        try:
            resp = requests.request(method, url, timeout=(3, 10), **kwargs)
        except (requests.ConnectionError, requests.Timeout) as exc:
            resp, reason = None, type(exc).__name__
        else:
            if resp.status_code not in RETRYABLE:
                return resp
            reason = resp.status_code
        if attempt == attempts - 1:
            break
        retry_after = resp.headers.get("Retry-After") if resp is not None else None
        delay = float(retry_after) if retry_after and retry_after.isdigit() else random.uniform(0, 0.5 * 2**attempt)
        print(f"  attempt {attempt + 1} failed ({reason}); waiting {delay:.2f}s")
        time.sleep(delay)
    raise RuntimeError(f"giving up on {method} {url}")


# 1. Hit the rate limit on purpose: 15 quick calls against a burst of 10
for i in range(15):
    r = call_with_retries("GET", f"{BASE}/limited/books")
    print(i + 1, r.status_code, "remaining:", r.headers.get("X-RateLimit-Remaining"))

# 2. A POST is only safe to retry with an Idempotency-Key: the same key never creates two orders
key = str(uuid.uuid4())
first = call_with_retries("POST", f"{BASE}/orders", json={"book_id": 1}, headers={"Idempotency-Key": key})
again = call_with_retries("POST", f"{BASE}/orders", json={"book_id": 1}, headers={"Idempotency-Key": key})
print("same order both times:", first.json()["id"] == again.json()["id"],
      "| replayed:", again.headers.get("Idempotent-Replayed"))

# 3. Start a slow job and poll it
r = requests.post(f"{BASE}/reports", timeout=5)
status_url = BASE + r.headers["Location"]
while True:
    job = requests.get(status_url, timeout=5).json()
    print("job:", job["status"])
    if job["status"] == "done":
        print("result:", job["result"])
        break
    time.sleep(float(r.headers.get("Retry-After", 1)))
