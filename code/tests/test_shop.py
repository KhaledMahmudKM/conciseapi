"""Chapter 9: each flaw is exploitable in shop_insecure and blocked in shop_secure."""
import copy

import pytest
from fastapi.testclient import TestClient

import shop_insecure as bad
import shop_secure as good

ALICE = {"Authorization": "Bearer token-alice"}
BOB = {"Authorization": "Bearer token-bob"}
USERS0 = copy.deepcopy(bad.USERS)


@pytest.fixture(autouse=True)
def reset_users():
    for mod in (bad, good):
        mod.USERS.clear()
        mod.USERS.update(copy.deepcopy(USERS0))


@pytest.fixture
def insecure():
    return TestClient(bad.app)


@pytest.fixture
def secure():
    return TestClient(good.app)


def test_api1_bola(insecure, secure):
    # order 2 belongs to bob; alice asks for it
    assert insecure.get("/orders/2", headers=ALICE).status_code == 200      # leak
    assert secure.get("/orders/2", headers=ALICE).status_code == 404        # fixed
    assert secure.get("/orders/1", headers=ALICE).status_code == 200        # her own order still works


def test_api3_excessive_data(insecure, secure):
    assert "password_hash" in insecure.get("/users/me", headers=ALICE).json()
    assert set(secure.get("/users/me", headers=ALICE).json()) == {"id", "name", "email", "credit"}


def test_api3_mass_assignment(insecure, secure):
    r = insecure.patch("/users/me", json={"role": "admin", "credit": 9999}, headers=ALICE)
    assert r.json()["role"] == "admin" and r.json()["credit"] == 9999           # privilege escalation
    assert secure.patch("/users/me", json={"credit": 9999}, headers=ALICE).status_code == 422
    assert secure.patch("/users/me", json={"name": "Alice"}, headers=ALICE).json()["name"] == "Alice"


def test_api4_resource_consumption(insecure, secure):
    assert len(insecure.get("/orders?limit=1000000", headers=ALICE).json()) == 1000
    assert secure.get("/orders?limit=1000000", headers=ALICE).status_code == 422


def test_api5_bfla(insecure, secure):
    assert insecure.delete("/admin/users/2", headers=ALICE).status_code == 204   # a customer deleted bob
    assert secure.delete("/admin/users/2", headers=ALICE).status_code == 403
    assert secure.delete("/admin/users/2", headers={"Authorization": "Bearer token-admin"}).status_code == 204


def test_api7_ssrf(insecure, secure, monkeypatch):
    fetched = []
    monkeypatch.setattr(bad, "fetch", lambda url: fetched.append(url) or "secret")
    monkeypatch.setattr(good, "fetch", lambda url: fetched.append(url) or "image")
    metadata = "http://169.254.169.254/latest/meta-data/"
    assert insecure.post("/covers/preview", json={"url": metadata}, headers=ALICE).json() == {"preview": "secret"}
    for url in (metadata, "http://localhost:8000/admin", "https://evil.example/x.jpg", "file:///etc/passwd"):
        assert secure.post("/covers/preview", json={"url": url}, headers=ALICE).status_code == 400
    assert fetched == [metadata]                                     # the secure app fetched nothing
