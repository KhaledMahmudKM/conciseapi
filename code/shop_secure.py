"""Chapter 9: the same Shop API with each flaw fixed.

Run:   fastapi dev shop_secure.py
Users: Authorization: Bearer token-alice | token-bob | token-admin
"""
import copy
import ipaddress
import socket
from urllib.parse import urlparse

import requests
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, EmailStr, Field

import shop_insecure

app = FastAPI(title="Shop API (secure)")

USERS = copy.deepcopy(shop_insecure.USERS)
TOKENS = dict(shop_insecure.TOKENS)
ORDERS = copy.deepcopy(shop_insecure.ORDERS)
COVER_HOSTS = {"covers.openlibrary.org"}          # allowlist for server-side fetches

bearer = HTTPBearer()


def current_user(cred: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    user_id = TOKENS.get(cred.credentials)
    if user_id is None or user_id not in USERS:
        raise HTTPException(401, "Invalid token")
    return USERS[user_id]


def require_admin(user: dict = Depends(current_user)) -> dict:
    if user["role"] != "admin":
        raise HTTPException(403, "Admins only")
    return user


class PublicUser(BaseModel):            # only what the client may see
    id: int
    name: str
    email: str
    credit: int


class UserUpdate(BaseModel):            # only what the client may change
    model_config = ConfigDict(extra="forbid")
    name: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = None


class CoverRequest(BaseModel):
    url: str = Field(max_length=500)


def fetch(url: str) -> str:
    return requests.get(url, timeout=3, allow_redirects=False).text[:200]


def safe_cover_url(url: str) -> bool:
    u = urlparse(url)
    if u.scheme != "https" or u.hostname not in COVER_HOSTS or u.port not in (None, 443):
        return False
    try:
        addresses = {i[4][0] for i in socket.getaddrinfo(u.hostname, 443)}
    except socket.gaierror:
        return False
    return all(ipaddress.ip_address(a).is_global for a in addresses)


# API1 fixed: check that the object belongs to the caller; answer 404 so IDs cannot be probed
@app.get("/orders/{order_id}")
def get_order(order_id: int, user: dict = Depends(current_user)):
    order = ORDERS.get(order_id)
    if order is None or order["owner"] != user["id"]:
        raise HTTPException(404, "No such order")
    return order


# API3 fixed (read): a response model filters out internal fields
@app.get("/users/me", response_model=PublicUser)
def read_me(user: dict = Depends(current_user)):
    return user


# API3 fixed (write): an explicit input model; unknown fields such as role or credit are rejected
@app.patch("/users/me", response_model=PublicUser)
def update_me(changes: UserUpdate, user: dict = Depends(current_user)):
    user.update(changes.model_dump(exclude_unset=True))
    return user


# API4 fixed: the server enforces a maximum page size
@app.get("/orders")
def list_orders(limit: int = Query(default=10, ge=1, le=50), user: dict = Depends(current_user)):
    mine = [o for o in ORDERS.values() if o["owner"] == user["id"]]
    return mine[:limit]


# API5 fixed: the function checks the caller's role, not just that they logged in
@app.delete("/admin/users/{user_id}", status_code=204)
def delete_user(user_id: int, admin: dict = Depends(require_admin)):
    USERS.pop(user_id, None)


# API7 fixed: only https URLs on an allowlisted host that resolves to public addresses
@app.post("/covers/preview")
def preview_cover(body: CoverRequest, user: dict = Depends(current_user)):
    if not safe_cover_url(body.url):
        raise HTTPException(400, "URL not allowed")
    return {"preview": fetch(body.url)}
