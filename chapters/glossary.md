# Glossary

**Access token.** A credential, usually short-lived, that a client presents to an API to prove it is allowed to make a request.

**API (application programming interface).** A contract that lets one piece of software use another: what you can ask for, how to ask, and what you get back.

**API gateway.** A reverse proxy in front of APIs that handles cross-cutting concerns such as TLS, authentication, rate limiting, and routing.

**API key.** A long random string that identifies a client application.

**Authentication (authn).** Establishing who is making a request.

**Authorization (authz).** Deciding whether an authenticated caller may perform a given action.

**Authorization code flow.** The OAuth flow in which a user logs in at the authorization server and the client exchanges a one-time code for tokens. Used with PKCE.

**Authorization server.** The OAuth component that authenticates users and issues tokens.

**Backoff.** Waiting between retries, usually for exponentially increasing times, often with random **jitter**.

**Bearer token.** A token that grants access to whoever holds it, sent as `Authorization: Bearer <token>`.

**BFLA.** Broken function level authorization: ordinary users can call privileged functions (OWASP API5).

**BOLA.** Broken object level authorization: a caller can access objects that belong to others by changing an ID (OWASP API1).

**Cache-Control.** The HTTP header that says whether and for how long a response may be cached.

**Claim.** A statement inside a token, such as `sub` (subject) or `exp` (expiry).

**Client credentials flow.** The OAuth flow in which an application obtains a token for itself, with no user involved.

**Code-first, design-first.** Generating the API description from code, or writing the description first and building to match.

**Collection.** A resource that contains other resources, such as `/books`.

**Content negotiation.** Choosing a representation format using headers such as `Accept`.

**CORS (cross-origin resource sharing).** The mechanism by which a server tells browsers which other origins may read its responses.

**CRUD.** Create, read, update, delete: the basic operations on stored data.

**Cursor pagination.** Paging with an opaque marker of the last item seen, rather than a numeric offset.

**Deprecation.** Marking a feature or version as discouraged and scheduled for removal; also the HTTP header that signals it (RFC 9745).

**Endpoint.** A URL and method that an API exposes, such as `GET /books/{id}`.

**ETag.** An identifier for a specific version of a representation, used for caching and concurrency control.

**FastAPI.** The Python web framework used in this book, built on Starlette and Pydantic.

**GraphQL.** A query language and runtime for APIs where clients specify exactly which fields they want.

**gRPC.** A remote procedure call framework using Protocol Buffers over HTTP/2.

**HATEOAS.** Hypermedia as the engine of application state: responses include links describing what the client can do next.

**HMAC.** A hash-based message authentication code: a signature computed with a shared secret, used for JWTs (HS256) and webhooks.

**Idempotent.** An operation that has the same effect whether performed once or several times.

**Idempotency key.** A unique value sent with a request so that the server can recognise and safely replay retries.

**JSON.** JavaScript Object Notation, the most common data format for web APIs.

**JSON Schema.** A vocabulary for describing and validating the structure of JSON data.

**JWT (JSON Web Token).** A compact, signed token format carrying claims as JSON.

**Mass assignment.** Copying all client-supplied fields into a stored object, letting clients set fields they should not (part of OWASP API3).

**Media type.** A label for a data format, such as `application/json`; also called a MIME type.

**Middleware.** Code that runs for every request, before and after the handler.

**Mutation.** A GraphQL operation that changes data.

**OAuth 2.0.** A framework for delegated authorization, letting applications access APIs on behalf of users with limited permissions.

**Observability.** The ability to understand a running system from its logs, metrics, and traces.

**OpenAPI.** A specification for describing HTTP APIs in a machine-readable JSON or YAML document.

**OpenID Connect (OIDC).** An identity layer on top of OAuth 2.0 that issues ID tokens describing the user.

**Optimistic concurrency.** Allowing updates only if the resource has not changed since it was read, checked with `If-Match`.

**OWASP.** The Open Worldwide Application Security Project, which publishes the API Security Top 10.

**Pagination.** Returning a large collection in pages.

**PKCE.** Proof Key for Code Exchange: a random verifier that binds an authorization code to the client that requested it.

**Problem details.** A standard JSON format for API errors (RFC 9457).

**Protocol Buffers (protobuf).** A compact binary serialization format with a schema language, used by gRPC.

**Pydantic.** A Python library for data validation using type hints, used by FastAPI.

**Rate limiting.** Restricting how many requests a client may make in a period.

**Representation.** The form in which a resource is transferred, such as a JSON document.

**Resource.** Anything an API exposes that can be named with a URL.

**Resource server.** The OAuth term for the API that accepts access tokens.

**REST.** Representational State Transfer, an architectural style for networked applications based on resources, standard methods, and representations.

**Safe method.** An HTTP method that does not change server state, such as `GET`.

**Scope.** A named permission attached to a token, such as `books:read`.

**SDK.** Software development kit: a client library that wraps an API for a particular language.

**Server-sent events (SSE).** A standard for streaming text events from server to browser over HTTP.

**SSRF.** Server side request forgery: tricking a server into making requests to destinations of the attacker's choosing (OWASP API7).

**Stateless.** Each request carries everything needed to process it; the server keeps no per-client session between requests.

**Status code.** The three-digit number in an HTTP response that summarises the outcome.

**Sunset.** The date after which a deprecated resource may stop working; also its HTTP header (RFC 8594).

**TLS.** Transport Layer Security, the encryption behind HTTPS.

**Token bucket.** A rate-limiting algorithm in which requests spend tokens that refill at a steady rate.

**Uvicorn.** The ASGI server that runs FastAPI applications.

**Versioning.** Publishing incompatible changes under a new version identifier while keeping the old one available for a time.

**Webhook.** An HTTP callback: a provider sends a request to a URL you registered when an event occurs.

**WebSocket.** A protocol giving a full-duplex, long-lived connection between browser and server.
