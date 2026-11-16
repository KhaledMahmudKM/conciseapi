"""Chapter 11: automated tests for the Library API (run: pytest -q)."""
import pytest
from fastapi.testclient import TestClient

import echo
import hello
import library

client = TestClient(library.app)


@pytest.fixture(autouse=True)
def fresh_data():
    library.reset()


def test_hello():
    c = TestClient(hello.app)
    assert c.get("/hello/Ada", params={"excited": True}).json() == {"greeting": "Hello, Ada!"}


def test_echo_reflects_the_request():
    r = TestClient(echo.app).post("/echo?x=1", json={"a": 1})
    assert r.json()["method"] == "POST" and r.json()["query"] == {"x": "1"}
    assert TestClient(echo.app).get("/status/418").status_code == 418


def test_list_filter_and_sort():
    r = client.get("/books", params={"author": "austen", "sort": "-year"})
    assert r.status_code == 200
    assert [b["title"] for b in r.json()["items"]] == ["Emma", "Pride and Prejudice"]


def test_pagination_link_header():
    r = client.get("/books", params={"limit": 2})
    assert r.json()["total"] == 5 and len(r.json()["items"]) == 2
    assert 'rel="next"' in r.headers["Link"] and "offset=2" in r.headers["Link"]
    last = client.get("/books", params={"limit": 2, "offset": 4})
    assert "Link" not in last.headers


def test_create_returns_201_and_location():
    r = client.post("/books", json={"title": "Kindred", "author": "Octavia E. Butler", "year": 1979})
    assert r.status_code == 201
    assert r.headers["Location"] == f"/books/{r.json()['id']}"
    assert client.get(r.headers["Location"]).json()["title"] == "Kindred"


def test_validation_errors_are_problem_details():
    r = client.post("/books", json={"title": "", "author": "X", "role": "admin"})
    assert r.status_code == 422
    assert r.headers["Content-Type"] == "application/problem+json"
    fields = {e["field"] for e in r.json()["errors"]}
    assert {"title", "role"} <= fields


def test_not_found_is_problem_details():
    r = client.get("/books/999")
    assert r.status_code == 404
    assert r.json()["title"] == "Not Found" and r.json()["instance"] == "/books/999"


def test_put_patch_delete():
    assert client.put("/books/3", json={"title": "Dune", "author": "Frank Herbert", "year": 1966}).json()["year"] == 1966
    r = client.patch("/books/3", json={"year": 1965})
    assert r.json()["year"] == 1965 and r.json()["title"] == "Dune"
    assert client.delete("/books/3").status_code == 204
    assert client.get("/books/3").status_code == 404
    assert client.delete("/books/3").status_code == 404


def test_openapi_document():
    spec = client.get("/openapi.json").json()
    assert spec["openapi"].startswith("3.")
    assert set(spec["paths"]) == {"/books", "/books/{book_id}"}
    assert "BookIn" in spec["components"]["schemas"]
