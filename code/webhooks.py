"""Chapter 12: receiving webhooks safely, and sending them.

Receiver:  fastapi dev webhooks.py
Sender:    python webhooks.py            (posts one signed event to the receiver)
"""
import hashlib
import hmac
import json
import time
import uuid

from fastapi import FastAPI, Header, HTTPException, Request

SECRET = b"whsec_shared_secret_for_the_lab"     # shared once, out of band, between sender and receiver
TOLERANCE = 300                                  # seconds: reject old or replayed deliveries

app = FastAPI(title="Webhook receiver")
seen_events: set[str] = set()


def sign(timestamp: int, body: bytes) -> str:
    mac = hmac.new(SECRET, f"{timestamp}.".encode() + body, hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={mac}"


def verify(header: str, body: bytes, now: float | None = None) -> bool:
    try:
        parts = dict(p.split("=", 1) for p in header.split(","))
        timestamp = int(parts["t"])
    except (ValueError, KeyError):
        return False
    if abs((now or time.time()) - timestamp) > TOLERANCE:
        return False
    expected = sign(timestamp, body).split("v1=")[1]
    return hmac.compare_digest(expected, parts.get("v1", ""))       # constant-time comparison


@app.post("/webhooks/orders", status_code=204)
async def receive(request: Request, webhook_signature: str = Header()):
    body = await request.body()                  # verify the raw bytes, before parsing JSON
    if not verify(webhook_signature, body):
        raise HTTPException(401, "Bad signature")
    event = json.loads(body)
    if event["id"] in seen_events:               # deliveries can repeat: process each event once
        return
    seen_events.add(event["id"])
    print("processing", event["type"], event["data"])


if __name__ == "__main__":
    import requests

    event = {"id": f"evt_{uuid.uuid4().hex[:12]}", "type": "order.paid",
             "created": int(time.time()), "data": {"order_id": 42, "total": 19.5}}
    body = json.dumps(event).encode()
    resp = requests.post("http://127.0.0.1:8000/webhooks/orders", data=body, timeout=5,
                         headers={"Content-Type": "application/json",
                                  "Webhook-Signature": sign(int(time.time()), body)})
    print("delivered:", resp.status_code)
