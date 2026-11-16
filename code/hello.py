"""Chapter 2: the smallest useful API.

Run:   fastapi dev hello.py
Try:   curl http://127.0.0.1:8000/hello/Ada
"""
from fastapi import FastAPI

app = FastAPI(title="Hello API")


@app.get("/")
def root():
    return {"message": "Hello, API"}


@app.get("/hello/{name}")
def greet(name: str, excited: bool = False):
    text = f"Hello, {name}"
    return {"greeting": text + ("!" if excited else ".")}
