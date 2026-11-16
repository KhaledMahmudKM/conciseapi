"""Chapter 3: an API that shows you what HTTP looks like from the server side.

Run:   fastapi dev echo.py
Try:   curl -v -X POST http://127.0.0.1:8000/echo -H "Content-Type: application/json" -d '{"a": 1}'
       curl -i http://127.0.0.1:8000/status/418
"""
from fastapi import FastAPI, Request, Response

app = FastAPI(title="Echo API")


@app.api_route("/echo", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def echo(request: Request):
    body = await request.body()
    return {
        "method": request.method,
        "path": request.url.path,
        "query": dict(request.query_params),
        "headers": dict(request.headers),
        "body": body.decode("utf-8", errors="replace"),
    }


@app.get("/status/{code}")
def status(code: int, response: Response):
    response.status_code = code
    return {"you_asked_for": code}


@app.get("/headers")
def custom_headers(response: Response):
    response.headers["X-Book"] = "Concise APIs"
    response.headers["Cache-Control"] = "max-age=60"
    return {"look": "at the response headers"}
