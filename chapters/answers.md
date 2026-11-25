# Answers to Chapter Questions

Answers and short explanations for the **Check your understanding** questions at the end of each chapter. Try the questions first; each section links back to them.

## Chapter 1: What Is an API?

**1. A. A contract that lets one program use another without knowing how it is built**

The contract is what matters; the implementation behind it can change.

**2. C. The menu**

The menu lists what you can order and what you get; the kitchen can change behind it.

**3. B. Calls cross a network, so they can be slow or fail**

Delays, timeouts and partial failures are normal over a network.

**4. D. Teams can work independently and change their implementations behind the contract**

APIs let teams work independently, let implementations change, and let capabilities be shared.

**5. B. Clients you do not control depend on them, and a change can break them**

Chapter 11 covers how to evolve an API without breaking clients.

**6. D. GraphQL**

gRPC uses Protocol Buffers over HTTP/2; webhooks push events to the client.

**7. A. Webhooks**

The client registers a URL, and the provider sends an HTTP request to it.

**8. C. A client library that wraps the API in functions for a programming language**

SDKs save consumers from building HTTP requests by hand.

[Back to the questions](01-what-is-an-api.md#check-your-understanding)

## Chapter 2: The Lab

**1. D. An ASGI server that runs the FastAPI application**

FastAPI is the framework; uvicorn is the server; curl and requests are clients; pytest runs tests.

**2. B. As a decorated Python function**

A decorator such as @app.get("/books/{book_id}") maps a method and path to the function.

**3. D. 42**

format=short is a query parameter, after the ?.

**4. A. 422, before your function runs**

Type hints drive validation; invalid input never reaches your code.

**5. C. Interactive documentation generated from the API's OpenAPI description**

Try it out sends real requests from the browser.

**6. D. To keep the project's packages separate from the system and other projects**

Each project gets its own isolated set of installed packages.

**7. B. Serialises it, usually to JSON, as the response body**

The framework extracts and validates input, calls your function, and serialises the result.

**8. C. pytest**

The code folder ships with tests for every example.

[Back to the questions](02-lab.md#check-your-understanding)

## Chapter 3: HTTP for APIs

**1. A. A blank line**

A message is a start line, headers, a blank line, then an optional body.

**2. C. POST**

Repeating a POST may create a second resource; idempotency keys make retries safe.

**3. D. Repeating the same request has the same effect as sending it once**

Safe means it changes nothing; GET is both safe and idempotent, PUT and DELETE are idempotent only.

**4. B. 401**

401 really means unauthenticated; 403 means authenticated but not allowed.

**5. C. The server failed**

2xx is success, 4xx a client error, 5xx a server error.

**6. A. With the Accept header**

This is content negotiation; Content-Type describes the body actually sent.

**7. D. HTTP/3**

HTTP/2 multiplexes over one TCP connection; all versions share the same semantics.

**8. C. Each request carries everything needed, so any server can handle it**

No server needs to remember previous requests, so a load balancer can send each request anywhere.

[Back to the questions](03-http.md#check-your-understanding)

## Chapter 4: JSON and Data Formats

**1. B. Six**

Object, array, string, number, boolean and null.

**2. C. {"name": "Ada"}**

Names and strings use double quotes; no trailing commas or comments.

**3. A. As an ISO 8601 string with a time zone**

For example "2026-11-25T14:30:00Z".

**4. A. JavaScript numbers are exact only up to 2^53, so larger IDs can silently change**

9007199254740993 becomes 9007199254740992 in a browser.

**5. C. As an integer in the smallest unit, or a decimal string**

Floating-point rounding errors are unacceptable for money.

**6. B. It leaves room to add fields such as a total or next-page link without breaking clients**

A bare array cannot grow new top-level fields.

**7. D. Which JSON documents are valid: types, required fields and limits**

Pydantic models can generate JSON Schema and validate input against it.

**8. B. Protocol Buffers**

It is compact and fast, but not human-readable.

[Back to the questions](04-json.md#check-your-understanding)

## Chapter 5: Designing REST APIs

**1. A. /books/42**

Use nouns, plural collections, lowercase, and no file extensions or implementation details.

**2. C. PUT sends the complete new state; PATCH sends only the changes**

With PUT, any field left out is reset.

**3. B. POST /books**

POST on a collection creates; GET, PUT, PATCH and DELETE act on items.

**4. D. A state change, such as PATCH /orders/42 with {"status": "cancelled"}**

Next, consider a new resource such as POST /orders/42/cancellations; use an action endpoint only as a last resort.

**5. B. Pages shift when items are added or removed, causing duplicates or misses, and deep offsets are slow**

Cursor pagination avoids both, but allows only forward and back.

**6. D. So no client can request a huge page that overloads the server**

Always paginate, and cap limit even when the client asks for more.

**7. D. Level 3**

Most well-designed APIs sit at level 2: resources, methods and status codes used properly.

**8. C. Consistency**

One naming style, one error format, one pagination scheme across the whole API.

[Back to the questions](05-rest-design.md#check-your-understanding)

## Chapter 6: Building a REST API

**1. D. Each shape has different rules: clients never send id, updates are partial, output includes server fields**

One resource, several shapes.

**2. B. Rejects requests that contain unknown fields**

A typo such as 'titel' is reported instead of silently ignored.

**3. D. 201 Created with a Location header**

Location gives the URL of the new resource.

**4. A. 204 No Content**

There is nothing more to say, so there is no body.

**5. C. So only fields the client actually sent are changed, not fields that defaulted to None**

Without it, omitted fields would overwrite stored values with defaults.

**6. C. RFC 9457**

Problem Details for HTTP APIs; errors say what went wrong and how to fix it, without leaking internals.

**7. B. In a Link header**

Clients should follow the links the server provides.

**8. C. Always set a timeout**

Without a timeout, a stuck server can hang the client indefinitely.

[Back to the questions](06-building.md#check-your-understanding)

## Chapter 7: Documenting APIs with OpenAPI

**1. A. An HTTP API, in one machine-readable JSON or YAML document**

It was called Swagger until 2016; the current version is 3.2.

**2. C. 3.1**

3.2 (2025) is the current specification version.

**3. D. Reusable schemas and security schemes, referenced with $ref**

paths describe the operations; components hold the shared pieces.

**4. B. Swagger UI at /docs and ReDoc at /redoc**

The raw document is at /openapi.json.

**5. C. Generates requests from it and tests that the API behaves as described**

Generated documentation can drift from behaviour; test the API against its description.

**6. A. Lints the OpenAPI document against style rules**

Linting catches inconsistent naming, missing descriptions and similar problems.

**7. A. Consumers can review the contract before any code is written**

Code-first is quicker to start; design-first catches design problems early.

**8. C. AsyncAPI**

Arazzo describes multi-step workflows across API calls.

[Back to the questions](07-openapi.md#check-your-understanding)

## Chapter 8: Authentication and Authorization

**1. B. Who are you? 401**

Authorization answers what you may do; a failure is 403.

**2. C. As hashes, like passwords**

A leaked database then does not reveal usable keys.

**3. A. No, it is signed, not encrypted, so anyone can read it**

Never put secrets in a JWT; the signature only proves it was not changed.

**4. A. It stops forged tokens that claim alg none or switch algorithms**

Verify signature, algorithm, expiry, issuer and audience.

**5. C. A JWT is hard to revoke, so a short lifetime limits damage if one leaks**

A longer-lived refresh token gets new access tokens without logging in again.

**6. B. Authorization code with PKCE**

OAuth 2.1 removes the password and implicit grants.

**7. D. Client credentials**

The service authenticates as itself.

**8. B. Login, with an ID token that tells the client who the user is**

ID tokens are for the client; access tokens are for the API.

[Back to the questions](08-auth.md#check-your-understanding)

## Chapter 9: API Security

**1. A. Authorization failures by authenticated users**

The OWASP API Security Top 10 (2023) is dominated by authorization problems.

**2. C. API1 Broken object level authorization**

Check ownership of every object.

**3. B. 404, so it does not reveal that the object exists**

404 hides which IDs exist.

**4. D. Input models with extra fields forbidden, instead of raw dictionaries**

This is API3, broken object property level authorization (mass assignment).

**5. B. API5 Broken function level authorization**

Check the role for every function.

**6. D. The server can be made to fetch internal addresses such as the metadata service at 169.254.169.254, which hands out credentials**

Fetch client-supplied URLs only through an allowlist, https only, public IPs only, no redirects.

**7. A. Browser users, by controlling which sites' scripts may read your API's responses**

CORS does not protect your API; curl ignores it entirely.

**8. C. Write a test for it**

Tests keep fixed vulnerabilities from coming back; layer defences too.

[Back to the questions](09-api-security.md#check-your-understanding)

## Chapter 10: Performance and Reliability

**1. D. The average hides the slow tail that users actually notice**

A p95 of 300 ms means 95% of requests finish within 300 ms.

**2. B. 304 Not Modified, with no body**

The client reuses its cached copy.

**3. D. The update succeeds only if the resource still has the ETag the client read; otherwise 412**

This is optimistic concurrency; 428 means the server requires If-Match.

**4. A. Token bucket**

Each client's bucket refills at a steady rate; each request spends a token.

**5. C. 429 Too Many Requests with a Retry-After header**

Retry-After tells the client when to try again.

**6. D. Only transient ones, such as timeouts, 429 and 503**

A 400 will fail the same way every time.

**7. B. So many clients do not retry at exactly the same moments and overload the server again**

Random spread breaks up synchronised retry waves.

**8. C. 202 Accepted with a status URL to poll**

The client checks the status resource until the job finishes.

[Back to the questions](10-performance.md#check-your-understanding)

## Chapter 11: Evolving and Operating APIs

**1. A. Adding a new optional field to a response**

Additive changes are safe if clients ignore fields they do not recognise.

**2. C. In the URL path, such as /v2/**

Version only for breaking changes, and keep few versions alive.

**3. D. Sunset**

Sunset is RFC 8594; Deprecation (RFC 9745) says it is deprecated.

**4. B. 410 Gone**

410 says the resource existed and was removed on purpose.

**5. C. Centralising TLS, authentication, rate limits, routing and inventory**

It sits in front of the services.

**6. A. A request ID**

Pass it on every downstream call and include it in every log line.

**7. A. Secrets, such as tokens and passwords**

Logs are widely accessible and kept for a long time.

**8. C. A vendor-neutral standard and toolkit for traces, metrics and logs**

It lets you switch observability back ends without changing your code.

[Back to the questions](11-evolving.md#check-your-understanding)

## Chapter 12: Beyond REST

**1. B. It has one endpoint and a typed schema, and the client chooses the response shape**

Changes are made with mutations.

**2. C. Query depth and complexity, since one query can ask for a huge amount of work**

Also check authorization in every resolver, and watch for N+1 queries.

**3. A. Queries are usually sent with POST to one URL**

HTTP caches key on method and URL.

**4. A. Messages carry tags instead of names, so changing a tag breaks compatibility**

Tags are how protobuf stays backward compatible.

**5. C. Calls between internal services**

Compact messages, generated stubs and HTTP/2 streaming suit service-to-service traffic.

**6. B. Verify the signature and reject stale timestamps**

Anyone can send a request to your URL; the signature proves the provider sent it.

**7. D. Providers retry, so the same event can arrive more than once**

Make handlers idempotent, keyed by the event ID.

**8. B. WebSockets**

SSE pushes events only from server to browser, over plain HTTP.

[Back to the questions](12-beyond-rest.md#check-your-understanding)
