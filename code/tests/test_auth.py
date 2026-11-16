"""Chapter 8: authentication and authorization behave as the chapter describes."""
import time

import jwt
from fastapi.testclient import TestClient

import library_auth as auth

client = TestClient(auth.app)


def token(user, password, scope=None):
    data = {"username": user, "password": password}
    if scope:
        data["scope"] = scope
    return client.post("/token", data=data)


def bearer(t):
    return {"Authorization": f"Bearer {t}"}


def test_api_key():
    assert client.get("/partner/books").status_code == 401
    assert client.get("/partner/books", headers={"X-API-Key": "wrong"}).status_code == 401
    r = client.get("/partner/books", headers={"X-API-Key": "demo-key-123"})
    assert r.status_code == 200 and r.json()["client"] == "partner-bookshop"


def test_login_and_scopes():
    assert token("ada", "nope").status_code == 401
    t = token("ada", "lovelace").json()
    assert t["token_type"] == "bearer" and set(t["scope"].split()) == {"books:read", "books:write"}
    assert client.post("/books", json={"title": "Kindred"}, headers=bearer(t["access_token"])).status_code == 201


def test_cannot_get_more_scope_than_allowed():
    t = token("bob", "builder", scope="books:read books:write").json()
    assert t["scope"] == "books:read"
    assert client.get("/books", headers=bearer(t["access_token"])).status_code == 200
    r = client.post("/books", json={"title": "x"}, headers=bearer(t["access_token"]))
    assert r.status_code == 403 and "books:write" in r.json()["detail"]


def test_missing_expired_and_forged_tokens():
    assert client.get("/books").status_code == 401
    now = int(time.time())
    expired = jwt.encode({"sub": "ada", "scope": "books:read", "iss": auth.ISSUER, "aud": auth.AUDIENCE,
                          "iat": now - 3600, "exp": now - 60}, auth.SECRET_KEY, algorithm="HS256")
    assert client.get("/books", headers=bearer(expired)).json()["detail"] == "Token expired"
    forged = jwt.encode({"sub": "ada", "scope": "books:write", "iss": auth.ISSUER, "aud": auth.AUDIENCE,
                         "exp": now + 600}, "attacker-guessed-key-0123456789abcdef", algorithm="HS256")
    assert client.get("/books", headers=bearer(forged)).status_code == 401
    unsigned = jwt.encode({"sub": "ada", "scope": "books:read", "iss": auth.ISSUER, "aud": auth.AUDIENCE,
                           "exp": now + 600}, None, algorithm="none")
    assert client.get("/books", headers=bearer(unsigned)).status_code == 401


def test_token_contents_are_readable_by_anyone():
    t = token("ada", "lovelace").json()["access_token"]
    claims = jwt.decode(t, options={"verify_signature": False})   # no key needed to READ a JWT
    assert claims["sub"] == "ada" and claims["exp"] - claims["iat"] == auth.TOKEN_TTL
