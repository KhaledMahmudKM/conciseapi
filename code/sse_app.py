"""Chapter 12: pushing updates to the client with server-sent events.

Run:   fastapi dev sse_app.py
Try:   curl -N http://127.0.0.1:8000/events
"""
import asyncio
import json
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI(title="Server-sent events")


async def ticker(count: int):
    for i in range(1, count + 1):
        data = {"seq": i, "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "stock": {"Dune": 10 - i}}
        yield f"id: {i}\nevent: stock\ndata: {json.dumps(data)}\n\n"
        await asyncio.sleep(1)


@app.get("/events")
def events(count: int = 5):
    return StreamingResponse(ticker(min(count, 60)), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache"})
