"""Chapter 12: GraphQL, webhooks, server-sent events and gRPC."""
import json
import subprocess
import sys
import time
from pathlib import Path

from fastapi.testclient import TestClient

import graphql_app
import sse_app
import webhooks


def test_graphql_query_and_mutation():
    c = TestClient(graphql_app.app)
    q = '{ books(yearAfter: 1900) { title author { name books { title } } } }'
    data = c.post("/graphql", json={"query": q}).json()["data"]
    assert data["books"][0]["title"] == "Dune"
    assert data["books"][0]["author"]["name"] == "Frank Herbert"
    m = 'mutation { addBook(title: "Persuasion", authorId: 1, year: 1817) { id title } }'
    assert c.post("/graphql", json={"query": m}).json()["data"]["addBook"]["title"] == "Persuasion"
    bad = c.post("/graphql", json={"query": "{ books { isbn } }"}).json()
    assert "errors" in bad


def test_webhook_signatures():
    c = TestClient(webhooks.app)
    body = json.dumps({"id": "evt_1", "type": "order.paid", "data": {"order_id": 1}}).encode()
    good = webhooks.sign(int(time.time()), body)
    h = {"Content-Type": "application/json"}
    assert c.post("/webhooks/orders", content=body, headers={**h, "Webhook-Signature": good}).status_code == 204
    assert c.post("/webhooks/orders", content=body + b" ", headers={**h, "Webhook-Signature": good}).status_code == 401
    old = webhooks.sign(int(time.time()) - 3600, body)
    assert c.post("/webhooks/orders", content=body, headers={**h, "Webhook-Signature": old}).status_code == 401
    assert c.post("/webhooks/orders", content=body, headers={**h, "Webhook-Signature": good}).status_code == 204
    assert webhooks.seen_events == {"evt_1"}                     # the repeat was not processed twice


def test_server_sent_events():
    with TestClient(sse_app.app).stream("GET", "/events?count=2") as r:
        assert r.headers["content-type"].startswith("text/event-stream")
        text = "".join(r.iter_text())
    assert text.count("event: stock") == 2 and "id: 2" in text


def test_grpc_roundtrip():
    folder = Path(__file__).resolve().parent.parent / "grpc_demo"
    subprocess.run([sys.executable, "-m", "grpc_tools.protoc", "-I.", "--python_out=.",
                    "--grpc_python_out=.", "library.proto"], cwd=folder, check=True)
    import server
    srv = server.serve(port=50061)
    try:
        import grpc
        import library_pb2
        import library_pb2_grpc
        with grpc.insecure_channel("127.0.0.1:50061") as ch:
            stub = library_pb2_grpc.LibraryStub(ch)
            assert stub.GetBook(library_pb2.GetBookRequest(id=3), timeout=2).title == "Dune"
            titles = [b.title for b in stub.ListBooks(library_pb2.ListBooksRequest(author="Jane Austen"), timeout=2)]
            assert titles == ["Pride and Prejudice", "Emma"]
            try:
                stub.GetBook(library_pb2.GetBookRequest(id=99), timeout=2)
                raise AssertionError("expected NOT_FOUND")
            except grpc.RpcError as err:
                assert err.code() == grpc.StatusCode.NOT_FOUND
    finally:
        srv.stop(0)
