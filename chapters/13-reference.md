# Chapter 13: Quick Reference

A compact summary of the commands, codes, and headers used throughout the book.

## curl

| Task | Command |
|---|---|
| GET, show body | `curl -s URL` |
| Show response headers too | `curl -i URL` |
| Show the full exchange, TLS included | `curl -v URL` |
| Only the status code | `curl -s -o /dev/null -w "%{http_code}\n" URL` |
| Send JSON | `curl -X POST URL -H "Content-Type: application/json" -d '{"k": "v"}'` |
| JSON from a file | `curl -X POST URL -H "Content-Type: application/json" -d @book.json` |
| Form data | `curl -X POST URL -d "username=ada&password=lovelace"` |
| Bearer token | `curl URL -H "Authorization: Bearer $TOKEN"` |
| API key | `curl URL -H "X-API-Key: $KEY"` |
| Follow redirects | `curl -L URL` |
| Conditional GET | `curl -i URL -H 'If-None-Match: "etag"'` |
| Stream (SSE) | `curl -N URL` |
| Time a request | `curl -s -o /dev/null -w "%{time_total}s\n" URL` |
| Pretty-print JSON | `curl -s URL \| python -m json.tool` |

## Python requests

```python
import requests

s = requests.Session()                                   # reuse connections
r = s.get(url, params={"author": "austen"}, timeout=5)   # always a timeout
r.raise_for_status()                                     # 4xx and 5xx become exceptions
data = r.json()
r = s.post(url, json={"title": "Kindred"}, headers={"Authorization": f"Bearer {token}"}, timeout=5)
location = r.headers["Location"]
next_url = r.links.get("next", {}).get("url")            # parsed Link header
```

## FastAPI essentials

| Need | Code |
|---|---|
| Path parameter | `def f(book_id: int)` with route `"/books/{book_id}"` |
| Query parameter with limits | `limit: int = Query(default=10, ge=1, le=100)` |
| JSON body | `def f(data: BookIn)` with a Pydantic model |
| Header | `if_match: str \| None = Header(default=None)` |
| Status code | `@app.post(..., status_code=201)` |
| Filter the response | `@app.get(..., response_model=Book)` |
| Set a response header | `response.headers["Location"] = "/books/6"` |
| Error | `raise HTTPException(404, "No such book")` |
| Dependency (auth) | `user: dict = Depends(current_user)` |
| Scopes | `Security(current_user, scopes=["books:read"])` |
| Reject unknown fields | `model_config = ConfigDict(extra="forbid")` |
| Partial update | `changes.model_dump(exclude_unset=True)` |
| Run in development | `fastapi dev app.py` |
| Docs | `/docs`, `/redoc`, `/openapi.json` |

## Methods

| Method | Purpose | Safe | Idempotent | Body |
|---|---|---|---|---|
| `GET` | Read | Yes | Yes | No |
| `HEAD` | Headers only | Yes | Yes | No |
| `OPTIONS` | Capabilities, CORS preflight | Yes | Yes | No |
| `POST` | Create, or any action | No | No | Yes |
| `PUT` | Replace | No | Yes | Yes |
| `PATCH` | Partial update | No | No | Yes |
| `DELETE` | Remove | No | Yes | Optional |

## Status codes

| Code | Name | Use it when |
|---|---|---|
| 200 | OK | Success with a body |
| 201 | Created | A resource was created; send `Location` |
| 202 | Accepted | Work was queued; send a status URL |
| 204 | No Content | Success with no body, such as `DELETE` |
| 301, 308 | Moved Permanently, Permanent Redirect | The URL has changed for good (308 keeps the method) |
| 304 | Not Modified | The client's cached copy is current |
| 400 | Bad Request | Malformed request |
| 401 | Unauthorized | Missing or invalid credentials; send `WWW-Authenticate` |
| 403 | Forbidden | Authenticated, but not allowed |
| 404 | Not Found | No such resource (or hidden from this caller) |
| 405 | Method Not Allowed | Wrong method for this URL |
| 409 | Conflict | Conflicts with current state, such as a duplicate |
| 410 | Gone | Removed for good, such as a sunset version |
| 412 | Precondition Failed | `If-Match` did not match |
| 415 | Unsupported Media Type | Wrong `Content-Type` |
| 422 | Unprocessable Content | Well-formed but invalid data |
| 428 | Precondition Required | Send `If-Match` |
| 429 | Too Many Requests | Rate limited; send `Retry-After` |
| 500 | Internal Server Error | A bug; log it, do not expose details |
| 502, 504 | Bad Gateway, Gateway Timeout | An upstream service failed or was slow |
| 503 | Service Unavailable | Overloaded or in maintenance; send `Retry-After` |

## Headers

| Header | Direction | Purpose |
|---|---|---|
| `Accept` | Request | Formats the client can handle |
| `Content-Type` | Both | Format of the body |
| `Authorization` | Request | Credentials: `Bearer ...`, `Basic ...` |
| `WWW-Authenticate` | Response | How to authenticate (with 401) |
| `Location` | Response | URL of a new or moved resource |
| `Link` | Response | Related URLs: `rel="next"`, `rel="successor-version"` |
| `Cache-Control` | Both | Caching rules |
| `ETag` | Response | Version of a representation |
| `If-None-Match` | Request | Conditional GET |
| `If-Match` | Request | Conditional update |
| `Retry-After` | Response | When to try again (429, 503, 202) |
| `Idempotency-Key` | Request | Makes a `POST` safe to retry |
| `X-Request-ID` | Both | Correlates logs for one request |
| `Deprecation`, `Sunset` | Response | Version retirement (RFC 9745, RFC 8594) |
| `Origin`, `Access-Control-Allow-Origin` | Request, response | CORS |

## Standards mentioned in this book

| Standard | Topic |
|---|---|
| RFC 9110 | HTTP semantics: methods, status codes, headers |
| RFC 9111 | HTTP caching |
| RFC 8259 | JSON |
| RFC 3339 | Date and time format (a profile of ISO 8601) |
| RFC 9457 | Problem details for HTTP APIs |
| RFC 8288 | Web linking (`Link` header) |
| RFC 6749 | OAuth 2.0 |
| RFC 7636 | PKCE |
| RFC 9700 | OAuth 2.0 security best current practice |
| RFC 7519 | JSON Web Token |
| RFC 9745, RFC 8594 | `Deprecation` and `Sunset` headers |
| RFC 6455 | WebSockets |
| OpenAPI 3.1, 3.2 | HTTP API descriptions |
| OWASP API Security Top 10, 2023 | API security risks |

## The lab code

| File | Chapter | What it shows |
|---|---|---|
| `hello.py` | 2 | A first endpoint |
| `echo.py` | 3 | Inspecting HTTP requests |
| `json_demo.py` | 4 | JSON pitfalls and JSON Schema |
| `library.py`, `client.py` | 5 to 7 | A complete REST API and client |
| `library_auth.py` | 8 | API keys, JWT, scopes |
| `shop_insecure.py`, `shop_secure.py` | 9 | OWASP flaws and fixes |
| `library_perf.py`, `retry_client.py` | 10 | Caching, rate limits, idempotency, async jobs |
| `library_ops.py` | 11 | Versioning, deprecation, request IDs |
| `graphql_app.py`, `grpc_demo/`, `webhooks.py`, `sse_app.py` | 12 | Beyond REST |
| `tests/` | all | 30 pytest tests |

## Further reading

- The FastAPI documentation, at fastapi.tiangolo.com, including its tutorial and security sections.
- MDN Web Docs on HTTP, at developer.mozilla.org: methods, status codes, headers, CORS, caching.
- The OpenAPI Specification, at spec.openapis.org.
- The OWASP API Security Project, at owasp.org.
- oauth.net, a guide to OAuth 2.0, OAuth 2.1, and related specifications.
- Public API design guides from Google, Microsoft, and Zalando, which show how large organisations make these decisions consistently.
