# Chapter 7: Documenting APIs with OpenAPI

An API is only as useful as its documentation. Developers need to know which endpoints exist, what to send, and what comes back, and they need that information to be correct. The **OpenAPI Specification** solves both problems by describing an API in a machine-readable document from which documentation, client libraries, tests, and more can be generated. This chapter explains the format and how to get the most from it.

## A short history

OpenAPI began as **Swagger**, created in 2011. In 2016 it was donated to the Linux Foundation's OpenAPI Initiative and renamed the OpenAPI Specification; the name "Swagger" lives on in tools such as Swagger UI. Version 3.0 arrived in 2017, and 3.1 (2021) aligned its schemas fully with JSON Schema. The latest version, **3.2**, released in September 2025, adds features such as streaming media types and hierarchical tags while remaining compatible with 3.1. FastAPI generates OpenAPI 3.1 documents.

## The document

An OpenAPI document is a single JSON or YAML file describing the whole contract.

<figure class="diagram">
<svg viewBox="0 0 720 310" style="width:100%;height:auto;max-width:720px" role="img" aria-label="The structure of an OpenAPI document: openapi version, info with title and version, servers, paths with operations, each operation with parameters, request body and responses, and components with reusable schemas and security schemes referenced through $ref." xmlns="http://www.w3.org/2000/svg">
<style>
.a7a{ font-family:var(--sans),sans-serif; }
.a7a .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a7a .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a7a .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a7a .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a7a .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a7a .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a7a .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a7a .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a7a .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a7a .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a7a .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a7a .s{ fill:var(--text-dim); font-size:13px; }
.a7a .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a7a .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a7a .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a7a .c{ fill:var(--text-faint); font-size:12.5px; }
.a7a .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a7a .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a7a .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a7a .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a7a-a); }
.a7a .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a7a-a); marker-start:url(#a7a-s); }
.a7a .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a7a-g); }
.a7a .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a7a-a); }
.a7a .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a7a .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a7a .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a7a .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a7a .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a7a .ks-teal{ fill:#0F6E56; font-size:13px; }
.a7a .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a7a .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a7a .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a7a .kb-teal, :root[data-theme="dark"] .a7a .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a7a .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a7a .kh-teal{ fill:#5DCAA5; }
.a7a .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a7a-teal); }
.a7a .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a7a-teal); }
.a7a .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a7a .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a7a .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a7a .ks-amber{ fill:#854F0B; font-size:13px; }
.a7a .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a7a .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a7a .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a7a .kb-amber, :root[data-theme="dark"] .a7a .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a7a .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a7a .kh-amber{ fill:#EF9F27; }
.a7a .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a7a-amber); }
.a7a .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a7a-amber); }
.a7a .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a7a .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a7a .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a7a .ks-purple{ fill:#534AB7; font-size:13px; }
.a7a .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a7a .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a7a .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a7a .kb-purple, :root[data-theme="dark"] .a7a .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a7a .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a7a .kh-purple{ fill:#AFA9EC; }
.a7a .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a7a-purple); }
.a7a .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a7a-purple); }
.a7a .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a7a .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a7a .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a7a .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a7a .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a7a .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a7a .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a7a .kb-gray, :root[data-theme="dark"] .a7a .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a7a .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a7a .kh-gray{ fill:#B4B2A9; }
.a7a .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a7a-gray); }
.a7a .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a7a-gray); }
.a7a .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a7a-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a7a-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a7a-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a7a-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a7a-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a7a-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a7a-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a7a">
<rect x="20" y="16" width="220" height="40" rx="5" class="k-gray"/>
<text x="130.0" y="40.5" text-anchor="middle" class="km-gray">openapi: 3.1.0</text>
<rect x="20" y="66" width="220" height="40" rx="5" class="k-gray"/>
<text x="130.0" y="90.5" text-anchor="middle" class="km-gray">info: title, version</text>
<rect x="20" y="116" width="220" height="40" rx="5" class="k-gray"/>
<text x="130.0" y="140.5" text-anchor="middle" class="km-gray">servers: [url]</text>
<rect x="270" y="16" width="430" height="170" rx="8" class="k-teal"/>
<text x="290" y="40" text-anchor="start" class="kh-teal">paths</text>
<rect x="290" y="52" width="390" height="34" rx="5" class="pnl"/>
<text x="485.0" y="73.5" text-anchor="middle" class="m">/books/{book_id}:</text>
<rect x="310" y="94" width="370" height="30" rx="4" class="pnl"/>
<text x="495.0" y="113.5" text-anchor="middle" class="m">get: parameters, responses</text>
<rect x="310" y="130" width="370" height="30" rx="4" class="pnl"/>
<text x="495.0" y="149.5" text-anchor="middle" class="m">patch: requestBody, responses</text>
<rect x="270" y="200" width="430" height="96" rx="8" class="k-purple"/>
<text x="290" y="224" text-anchor="start" class="kh-purple">components</text>
<rect x="290" y="236" width="190" height="44" rx="5" class="pnl"/>
<text x="385.0" y="262.5" text-anchor="middle" class="m">schemas: Book, BookIn</text>
<rect x="490" y="236" width="190" height="44" rx="5" class="pnl"/>
<text x="585.0" y="262.5" text-anchor="middle" class="m">securitySchemes</text>
<path d="M600 162 C 640 190, 640 210, 600 234" class="ad-purple"/>
<text x="690" y="196" text-anchor="end" class="kh-purple">$ref</text>
<rect x="20" y="200" width="220" height="96" rx="7" class="k-amber"/>
<text x="130.0" y="234.5" text-anchor="middle" class="ks-amber">one file, YAML or JSON,</text>
<text x="130.0" y="252.5" text-anchor="middle" class="ks-amber">describes the whole</text>
<text x="130.0" y="270.5" text-anchor="middle" class="ks-amber">contract</text>
</g>
</svg>
<figcaption>Paths say what you can call; components hold the shapes those calls use. $ref links them without repetition.</figcaption>
</figure>

| Section | Contents |
|---|---|
| `openapi` | The specification version, such as `3.1.0` |
| `info` | Title, version of **your** API, description, contact, licence |
| `servers` | Base URLs, such as production and staging |
| `paths` | Every endpoint: method, parameters, request body, possible responses |
| `components` | Reusable parts: `schemas` (data models), `securitySchemes`, shared parameters and responses |
| `security`, `tags` | Default authentication requirements; groups of operations for documentation |

Here is part of the document FastAPI generated for `GET /books/{book_id}`, shown as YAML:

```yaml
paths:
  /books/{book_id}:
    get:
      tags: [books]
      summary: Get one book
      operationId: get_book_books__book_id__get
      parameters:
        - name: book_id
          in: path
          required: true
          schema: {type: integer, title: Book Id}
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {$ref: '#/components/schemas/Book'}
        '404':
          description: No such book
components:
  schemas:
    Book:
      type: object
      required: [id, title, author]
      properties:
        id:    {type: integer}
        title: {type: string}
        year:  {anyOf: [{type: integer}, {type: 'null'}]}
```

`$ref` points to a reusable definition, so the `Book` schema is written once and used by every operation that returns a book. The schemas are JSON Schema, exactly as in Chapter 4.

## Generating it with FastAPI

FastAPI builds the document from your code: routes become `paths`, Pydantic models become `schemas`, and type hints become parameter definitions. You improve the result by adding information that code alone cannot express:

```python
app = FastAPI(
    title="Library API",
    version="1.0.0",
    description="A small REST API used throughout the Concise Book on APIs.",
    openapi_tags=[{"name": "books", "description": "Create, read, update and delete books."}],
)

@app.get("/books/{book_id}", response_model=Book, tags=["books"], summary="Get one book",
         responses={404: {"description": "No such book"}})
```

- `summary`, `description`, and docstrings become the human-readable text.
- `tags` group operations in the documentation.
- `responses` documents status codes other than the main one.
- `Field(examples=[...])` puts realistic examples into the schemas.

## Hands on: the docs, and their limits

Run the Library API (`fastapi dev library.py`) and open:

- **http://127.0.0.1:8000/docs**, **Swagger UI**: an interactive page where you can send requests.
- **http://127.0.0.1:8000/redoc**, **ReDoc**: a three-column reference layout.
- **http://127.0.0.1:8000/openapi.json**, the document itself.

Save the document to a file, which is how you would hand it to other tools:

```bash
curl -s http://127.0.0.1:8000/openapi.json -o openapi.json
python -c "import json; d = json.load(open('openapi.json')); print(d['openapi'], list(d['paths']))"
```

```text
3.1.0 ['/books', '/books/{book_id}']
```

Now look carefully at the `422` responses in Swagger UI. They describe FastAPI's **default** validation error, with a `detail` array, but Chapter 6 replaced that with **problem details**. The document and the behaviour disagree. Generated documentation is only as accurate as the information the framework has; custom exception handlers are invisible to it. Two lessons follow. First, document custom error responses explicitly with `responses=`. Second, **test** the API against its own description, which is exactly what contract-testing tools do.

## What the document is good for

<figure class="diagram">
<svg viewBox="0 0 720 270" style="width:100%;height:auto;max-width:720px" role="img" aria-label="One OpenAPI document feeds many tools: interactive documentation such as Swagger UI and Redoc, client SDK generators, server stubs, mock servers, contract tests and linters, and API gateways that validate requests." xmlns="http://www.w3.org/2000/svg">
<style>
.a7b{ font-family:var(--sans),sans-serif; }
.a7b .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a7b .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a7b .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a7b .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a7b .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a7b .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a7b .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a7b .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a7b .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a7b .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a7b .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a7b .s{ fill:var(--text-dim); font-size:13px; }
.a7b .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a7b .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a7b .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a7b .c{ fill:var(--text-faint); font-size:12.5px; }
.a7b .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a7b .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a7b .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a7b .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a7b-a); }
.a7b .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a7b-a); marker-start:url(#a7b-s); }
.a7b .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a7b-g); }
.a7b .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a7b-a); }
.a7b .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a7b .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a7b .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a7b .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a7b .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a7b .ks-blue{ fill:#185FA5; font-size:13px; }
.a7b .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a7b .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a7b .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a7b .kb-blue, :root[data-theme="dark"] .a7b .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a7b .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a7b .kh-blue{ fill:#85B7EB; }
.a7b .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a7b-blue); }
.a7b .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a7b-blue); }
.a7b .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a7b .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a7b .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a7b .ks-teal{ fill:#0F6E56; font-size:13px; }
.a7b .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a7b .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a7b .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a7b .kb-teal, :root[data-theme="dark"] .a7b .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a7b .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a7b .kh-teal{ fill:#5DCAA5; }
.a7b .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a7b-teal); }
.a7b .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a7b-teal); }
.a7b .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a7b .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a7b .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a7b .ks-amber{ fill:#854F0B; font-size:13px; }
.a7b .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a7b .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a7b .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a7b .kb-amber, :root[data-theme="dark"] .a7b .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a7b .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a7b .kh-amber{ fill:#EF9F27; }
.a7b .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a7b-amber); }
.a7b .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a7b-amber); }
.a7b .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
</style>
<defs><marker id="a7b-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a7b-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a7b-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a7b-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a7b-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a7b-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker></defs>
<g class="a7b">
<rect x="260" y="100" width="200" height="70" rx="7" class="k-amber"/>
<text x="360.0" y="130.5" text-anchor="middle" class="kb-amber">openapi.json</text>
<text x="360.0" y="148.5" text-anchor="middle" class="ks-amber">the contract</text>
<rect x="20" y="20" width="200" height="54" rx="7" class="k-teal"/>
<text x="120.0" y="42.5" text-anchor="middle" class="kb-teal">interactive docs</text>
<text x="120.0" y="60.5" text-anchor="middle" class="ks-teal">Swagger UI, Redoc</text>
<line x1="258" y1="135" x2="222" y2="47" class="ar"/>
<rect x="500" y="20" width="200" height="54" rx="7" class="k-blue"/>
<text x="600.0" y="42.5" text-anchor="middle" class="kb-blue">client SDKs</text>
<text x="600.0" y="60.5" text-anchor="middle" class="ks-blue">Python, TypeScript, Go</text>
<line x1="462" y1="135" x2="498" y2="47" class="ar"/>
<rect x="20" y="112" width="200" height="54" rx="7" class="k-teal"/>
<text x="120.0" y="134.5" text-anchor="middle" class="kb-teal">mock servers</text>
<text x="120.0" y="152.5" text-anchor="middle" class="ks-teal">test clients early</text>
<line x1="258" y1="135" x2="222" y2="139" class="ar"/>
<rect x="500" y="112" width="200" height="54" rx="7" class="k-blue"/>
<text x="600.0" y="134.5" text-anchor="middle" class="kb-blue">server stubs</text>
<text x="600.0" y="152.5" text-anchor="middle" class="ks-blue">design first</text>
<line x1="462" y1="135" x2="498" y2="139" class="ar"/>
<rect x="20" y="204" width="200" height="54" rx="7" class="k-teal"/>
<text x="120.0" y="226.5" text-anchor="middle" class="kb-teal">contract tests, linting</text>
<text x="120.0" y="244.5" text-anchor="middle" class="ks-teal">Schemathesis, Spectral</text>
<line x1="258" y1="135" x2="222" y2="231" class="ar"/>
<rect x="500" y="204" width="200" height="54" rx="7" class="k-blue"/>
<text x="600.0" y="226.5" text-anchor="middle" class="kb-blue">API gateways</text>
<text x="600.0" y="244.5" text-anchor="middle" class="ks-blue">validate requests</text>
<line x1="462" y1="135" x2="498" y2="231" class="ar"/>
</g>
</svg>
<figcaption>The description is worth more than the documentation page it produces: it is a machine-readable contract.</figcaption>
</figure>

- **Documentation.** Swagger UI, ReDoc, and many hosted portals render it.
- **Client SDKs.** Generators such as OpenAPI Generator produce client libraries in dozens of languages. For example, `openapi-python-client generate --path openapi.json` creates a typed Python package for the Library API.
- **Mock servers.** Tools such as Prism serve fake responses from the document, so frontend teams can start before the backend exists.
- **Testing.** **Schemathesis** reads the document and generates thousands of requests, including edge cases, then checks that every response matches the description. It would catch the `422` mismatch above.
- **Linting.** **Spectral** checks a document against style rules ("every operation needs a summary", "paths must be lowercase").
- **Gateways.** API gateways can import the document and reject requests that do not match it before they reach your service.

## Code-first or design-first?

<figure class="diagram">
<svg viewBox="0 0 720 250" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Code-first versus design-first. Code-first: write the server code, generate the OpenAPI document from it, then publish documentation. Design-first: write and review the OpenAPI document, then generate server stubs, client SDKs and mocks from it, and implement the server to match." xmlns="http://www.w3.org/2000/svg">
<style>
.a7c{ font-family:var(--sans),sans-serif; }
.a7c .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a7c .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a7c .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a7c .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a7c .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a7c .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a7c .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a7c .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a7c .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a7c .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a7c .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a7c .s{ fill:var(--text-dim); font-size:13px; }
.a7c .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a7c .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a7c .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a7c .c{ fill:var(--text-faint); font-size:12.5px; }
.a7c .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a7c .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a7c .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a7c .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a7c-a); }
.a7c .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a7c-a); marker-start:url(#a7c-s); }
.a7c .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a7c-g); }
.a7c .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a7c-a); }
.a7c .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a7c .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a7c .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a7c .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a7c .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a7c .ks-teal{ fill:#0F6E56; font-size:13px; }
.a7c .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a7c .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a7c .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a7c .kb-teal, :root[data-theme="dark"] .a7c .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a7c .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a7c .kh-teal{ fill:#5DCAA5; }
.a7c .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a7c-teal); }
.a7c .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a7c-teal); }
.a7c .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a7c .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a7c .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a7c .ks-amber{ fill:#854F0B; font-size:13px; }
.a7c .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a7c .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a7c .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a7c .kb-amber, :root[data-theme="dark"] .a7c .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a7c .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a7c .kh-amber{ fill:#EF9F27; }
.a7c .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a7c-amber); }
.a7c .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a7c-amber); }
.a7c .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
</style>
<defs><marker id="a7c-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a7c-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a7c-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a7c-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a7c-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker></defs>
<g class="a7c">
<text x="20" y="26" text-anchor="start" class="kh-teal">code-first (this book's labs)</text>
<rect x="20" y="38" width="200" height="44" rx="7" class="k-teal"/>
<text x="120.0" y="64.5" text-anchor="middle" class="kb-teal">write FastAPI code</text>
<rect x="252" y="38" width="200" height="44" rx="7" class="k-teal"/>
<text x="352.0" y="64.5" text-anchor="middle" class="kb-teal">generate openapi.json</text>
<line x1="222" y1="60" x2="250" y2="60" class="ar"/>
<rect x="484" y="38" width="200" height="44" rx="7" class="k-teal"/>
<text x="584.0" y="64.5" text-anchor="middle" class="kb-teal">publish docs</text>
<line x1="454" y1="60" x2="482" y2="60" class="ar"/>
<text x="20" y="134" text-anchor="start" class="kh-amber">design-first</text>
<rect x="20" y="146" width="200" height="44" rx="7" class="k-amber"/>
<text x="120.0" y="172.5" text-anchor="middle" class="kb-amber">write openapi.yaml</text>
<rect x="252" y="146" width="200" height="44" rx="7" class="k-amber"/>
<text x="352.0" y="172.5" text-anchor="middle" class="kb-amber">review with consumers</text>
<line x1="222" y1="168" x2="250" y2="168" class="ar"/>
<rect x="484" y="146" width="200" height="44" rx="7" class="k-amber"/>
<text x="584.0" y="172.5" text-anchor="middle" class="kb-amber">generate stubs, mocks, SDKs</text>
<line x1="454" y1="168" x2="482" y2="168" class="ar"/>
<text x="360" y="226" text-anchor="middle" class="c">either way, the OpenAPI document is the single source of truth for the contract</text>
</g>
</svg>
<figcaption>Code-first is quick for small teams; design-first lets consumers review the contract before anyone writes code.</figcaption>
</figure>

- **Code-first**, as in this book: write the server, generate the document. It is fast and keeps document and code in sync, as long as the code expresses everything.
- **Design-first**: write the OpenAPI document (usually in YAML), review it with the people who will use the API, then generate server stubs and clients from it and implement to match. It is slower to start but catches design mistakes before anyone writes code, which matters for public APIs.

Many teams combine them: design the contract first, then implement it with a code-first framework and use contract tests to prove the implementation matches the design.

## Beyond request and response

OpenAPI describes request and response APIs. Related specifications cover other shapes: **AsyncAPI** describes event-driven and message-based APIs (Kafka topics, MQTT, WebSockets), and the OpenAPI Initiative's **Arazzo** specification describes multi-step workflows across several API calls.

## Summary

- **OpenAPI** describes an HTTP API in one machine-readable JSON or YAML document. The current version is **3.2** (2025); FastAPI produces **3.1**.
- The document has **paths** (operations) and **components** (reusable schemas and security schemes), linked by **$ref**.
- FastAPI generates it from routes, models, and type hints; add **summaries**, **tags**, **examples**, and extra **responses**.
- The document drives **docs**, **SDKs**, **mocks**, **contract tests**, **linting**, and **gateways**.
- Generated docs can drift from behaviour; **test the API against its description**.
- **Code-first** is quick; **design-first** lets consumers review the contract early.
