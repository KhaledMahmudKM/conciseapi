"""Chapters 10 and 11: caching, rate limits, idempotency, async jobs, versions, request IDs."""
from fastapi.testclient import TestClient

import library_ops as ops
import library_perf as perf

c = TestClient(perf.app)


def test_etag_and_304():
    first = c.get("/books/1")
    tag = first.headers["ETag"]
    again = c.get("/books/1", headers={"If-None-Match": tag})
    assert again.status_code == 304 and again.content == b""


def test_optimistic_concurrency():
    tag = c.get("/books/2").headers["ETag"]
    assert c.put("/books/2", json={"title": "Emma", "year": 1815}).status_code == 428
    assert c.put("/books/2", json={"title": "Emma!", "year": 1815}, headers={"If-Match": tag}).status_code == 200
    assert c.put("/books/2", json={"title": "Emma?", "year": 1815}, headers={"If-Match": tag}).status_code == 412


def test_rate_limit():
    perf.buckets.clear()
    codes = [c.get("/limited/books", headers={"X-API-Key": "k1"}).status_code for _ in range(15)]
    assert codes[:10] == [200] * 10 and 429 in codes[10:]
    r = c.get("/limited/books", headers={"X-API-Key": "k1"})
    if r.status_code == 429:
        assert int(r.headers["Retry-After"]) >= 1
    assert c.get("/limited/books", headers={"X-API-Key": "k2"}).status_code == 200   # buckets are per client


def test_idempotency_key():
    h = {"Idempotency-Key": "abc-123"}
    a = c.post("/orders", json={"book_id": 1}, headers=h)
    b = c.post("/orders", json={"book_id": 1}, headers=h)
    assert a.json()["id"] == b.json()["id"] and b.headers["Idempotent-Replayed"] == "true"
    assert c.post("/orders", json={"book_id": 2}, headers=h).status_code == 422
    assert c.post("/orders", json={"book_id": 1}).status_code == 422          # the header is required


def test_async_job():
    r = c.post("/reports")
    assert r.status_code == 202 and r.headers["Location"].startswith("/reports/")
    assert c.get(r.headers["Location"]).json()["status"] in {"queued", "running", "done"}


def test_versions_and_deprecation():
    o = TestClient(ops.app)
    v1 = o.get("/v1/books/1")
    assert v1.json()["author"] == "Terry Pratchett, Neil Gaiman"
    assert v1.headers["Deprecation"].startswith("@") and v1.headers["Sunset"].endswith("GMT")
    assert 'rel="successor-version"' in v1.headers["Link"]
    v2 = o.get("/v2/books/1", headers={"X-Request-ID": "trace-42"})
    assert v2.json()["authors"] == ["Terry Pratchett", "Neil Gaiman"]
    assert v2.headers["X-Request-ID"] == "trace-42" and "Deprecation" not in v2.headers
