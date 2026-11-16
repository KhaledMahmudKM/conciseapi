# Code for the Concise Book on APIs

Every example from the book, tested with Python 3.13.

## Set up

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run an example

```bash
fastapi dev library.py             # then open http://127.0.0.1:8000/docs
```

| File | Chapter | What it shows |
|---|---|---|
| `hello.py` | 2 | A first endpoint |
| `echo.py` | 3 | Inspecting HTTP requests, status codes, headers |
| `json_demo.py` | 4 | JSON pitfalls and JSON Schema (run with `python json_demo.py`) |
| `library.py`, `client.py` | 5 to 7 | A complete REST API and a requests client |
| `library_auth.py` | 8 | API keys, JWT bearer tokens, scopes |
| `shop_insecure.py`, `shop_secure.py` | 9 | OWASP API Top 10 flaws, and their fixes |
| `library_perf.py`, `retry_client.py` | 10 | Caching, rate limiting, retries, idempotency keys, async jobs |
| `library_ops.py` | 11 | Versioning, deprecation headers, request IDs, JSON logs |
| `graphql_app.py` | 12 | GraphQL with Strawberry |
| `grpc_demo/` | 12 | gRPC: generate stubs, then run `server.py` and `client.py` |
| `webhooks.py` | 12 | Signed webhooks: receiver and sender |
| `sse_app.py` | 12 | Server-sent events |

`shop_insecure.py` is deliberately vulnerable. Run it only on your own machine.

## Test

```bash
pytest -q
```

All 30 tests should pass. The gRPC test generates its stubs automatically.
