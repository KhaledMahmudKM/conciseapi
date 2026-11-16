"""Chapter 9: a deliberately VULNERABLE API. Never deploy this.

Each endpoint contains one OWASP API Security Top 10 (2023) flaw, marked API1, API3, ...
shop_secure.py is the same API with every flaw fixed.

Run:   fastapi dev shop_insecure.py
Users: Authorization: Bearer token-alice   (customer)
       Authorization: Bearer token-bob     (customer)
       Authorization: Bearer token-admin   (admin)
"""
import requests
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

app = FastAPI(title="Shop API (INSECURE)")

USERS = {
    1: {"id": 1, "name": "alice", "email": "alice@example.com", "role": "customer",
        "credit": 20, "password_hash": "scrypt$9f2c...", "is_internal_tester": False},
    2: {"id": 2, "name": "bob", "email": "bob@example.com", "role": "customer",
        "credit": 5, "password_hash": "scrypt$51aa...", "is_internal_tester": False},
    3: {"id": 3, "name": "root", "email": "admin@example.com", "role": "admin",
        "credit": 0, "password_hash": "scrypt$00ff...", "is_internal_tester": True},
}
TOKENS = {"token-alice": 1, "token-bob": 2, "token-admin": 3}
ORDERS = {i: {"id": i, "owner": 1 if i % 2 else 2, "item": f"book #{i}", "total": 10 + i} for i in range(1, 2001)}

bearer = HTTPBearer()


def current_user(cred: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    user_id = TOKENS.get(cred.credentials)
    if user_id is None:
        raise HTTPException(401, "Invalid token")
    return USERS[user_id]


def fetch(url: str) -> str:
    return requests.get(url, timeout=3).text[:200]


# API1 Broken Object Level Authorization: any logged-in user can read any order
@app.get("/orders/{order_id}")
def get_order(order_id: int, user: dict = Depends(current_user)):
    if order_id not in ORDERS:
        raise HTTPException(404, "No such order")
    return ORDERS[order_id]


# API3 Broken Object Property Level Authorization (read side): returns every field, secrets included
@app.get("/users/me")
def read_me(user: dict = Depends(current_user)):
    return user


# API3 again (write side, "mass assignment"): any field can be changed, including role and credit
@app.patch("/users/me")
def update_me(changes: dict, user: dict = Depends(current_user)):
    user.update(changes)
    return user


# API4 Unrestricted Resource Consumption: the client chooses any page size
@app.get("/orders")
def list_orders(limit: int = 10, user: dict = Depends(current_user)):
    mine = [o for o in ORDERS.values() if o["owner"] == user["id"]]
    return mine[:limit]


# API5 Broken Function Level Authorization: an admin function that only checks login
@app.delete("/admin/users/{user_id}", status_code=204)
def delete_user(user_id: int, user: dict = Depends(current_user)):
    USERS.pop(user_id, None)


# API7 Server Side Request Forgery: the server fetches whatever URL the client names
@app.post("/covers/preview")
def preview_cover(body: dict, user: dict = Depends(current_user)):
    return {"preview": fetch(body["url"])}

