# Chapter 12: Beyond REST

REST over HTTP and JSON is the default for public APIs, but not the only option. This chapter introduces the main alternatives, each with a working example in the code folder: **GraphQL** for flexible queries, **gRPC** for fast service-to-service calls, **webhooks** for notifying other systems, and **server-sent events** and **WebSockets** for live updates. It ends with a guide to choosing between them.

## GraphQL

GraphQL, created at Facebook and open-sourced in 2015, exposes a single endpoint and a typed **schema**. Instead of the server deciding the shape of each response, the client sends a **query** describing exactly the data it wants.

<figure class="diagram">
<svg viewBox="0 0 720 280" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Fetching related data. With REST, showing authors and their books takes one request for the authors and one more per author, and each response has fields the screen does not need. With GraphQL the client sends one query naming exactly the fields it wants and gets them in one response." xmlns="http://www.w3.org/2000/svg">
<style>
.a12a{ font-family:var(--sans),sans-serif; }
.a12a .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a12a .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a12a .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a12a .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a12a .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a12a .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a12a .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a12a .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a12a .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a12a .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a12a .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a12a .s{ fill:var(--text-dim); font-size:13px; }
.a12a .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a12a .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a12a .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a12a .c{ fill:var(--text-faint); font-size:12.5px; }
.a12a .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a12a .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a12a .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a12a .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a12a-a); }
.a12a .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a12a-a); marker-start:url(#a12a-s); }
.a12a .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a12a-g); }
.a12a .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a12a-a); }
.a12a .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a12a .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a12a .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a12a .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a12a .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a12a .ks-blue{ fill:#185FA5; font-size:13px; }
.a12a .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a12a .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12a .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a12a .kb-blue, :root[data-theme="dark"] .a12a .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a12a .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a12a .kh-blue{ fill:#85B7EB; }
.a12a .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a12a-blue); }
.a12a .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12a-blue); }
.a12a .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a12a .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a12a .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a12a .ks-purple{ fill:#534AB7; font-size:13px; }
.a12a .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a12a .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12a .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a12a .kb-purple, :root[data-theme="dark"] .a12a .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a12a .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a12a .kh-purple{ fill:#AFA9EC; }
.a12a .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a12a-purple); }
.a12a .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12a-purple); }
.a12a .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a12a .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a12a .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a12a .ks-green{ fill:#3B6D11; font-size:13px; }
.a12a .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a12a .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12a .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a12a .kb-green, :root[data-theme="dark"] .a12a .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a12a .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a12a .kh-green{ fill:#97C459; }
.a12a .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a12a-green); }
.a12a .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12a-green); }
.a12a .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a12a .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a12a .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a12a .ks-red{ fill:#A32D2D; font-size:13px; }
.a12a .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a12a .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12a .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a12a .kb-red, :root[data-theme="dark"] .a12a .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a12a .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a12a .kh-red{ fill:#F09595; }
.a12a .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a12a-red); }
.a12a .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12a-red); }
.a12a .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
</style>
<defs><marker id="a12a-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a12a-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a12a-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a12a-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a12a-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a12a-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a12a-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker></defs>
<g class="a12a">
<text x="20" y="24" text-anchor="start" class="kh-blue">REST: several round trips, fixed shapes</text>
<rect x="20" y="36" width="220" height="34" rx="5" class="k-blue"/>
<text x="130.0" y="57.5" text-anchor="middle" class="km-blue">GET /authors</text>
<line x1="242" y1="53" x2="300" y2="53" class="ar"/>
<rect x="302" y="36" width="80" height="34" rx="5" class="pnl"/>
<text x="342.0" y="57.5" text-anchor="middle" class="c">all fields</text>
<rect x="20" y="78" width="220" height="34" rx="5" class="k-blue"/>
<text x="130.0" y="99.5" text-anchor="middle" class="km-blue">GET /authors/1/books</text>
<line x1="242" y1="95" x2="300" y2="95" class="ar"/>
<rect x="302" y="78" width="80" height="34" rx="5" class="pnl"/>
<text x="342.0" y="99.5" text-anchor="middle" class="c">all fields</text>
<rect x="20" y="120" width="220" height="34" rx="5" class="k-blue"/>
<text x="130.0" y="141.5" text-anchor="middle" class="km-blue">GET /authors/2/books</text>
<line x1="242" y1="137" x2="300" y2="137" class="ar"/>
<rect x="302" y="120" width="80" height="34" rx="5" class="pnl"/>
<text x="342.0" y="141.5" text-anchor="middle" class="c">all fields</text>
<text x="420" y="24" text-anchor="start" class="kh-purple">GraphQL: one round trip, chosen fields</text>
<rect x="420" y="36" width="280" height="118" rx="8" class="k-purple"/>
<text x="436" y="62" text-anchor="start" class="m">{ authors {</text>
<text x="466.0" y="86" text-anchor="start" class="m">name</text>
<text x="466.0" y="110" text-anchor="start" class="m">books { title year }</text>
<text x="436" y="134" text-anchor="start" class="m">} }</text>
<line x1="560" y1="156" x2="560" y2="186" class="ar-purple"/>
<rect x="420" y="188" width="280" height="40" rx="7" class="k-green"/>
<text x="560.0" y="212.5" text-anchor="middle" class="kb-green">exactly that shape back</text>
<rect x="20" y="188" width="362" height="40" rx="7" class="k-red"/>
<text x="201.0" y="212.5" text-anchor="middle" class="kb-red">over-fetching and under-fetching</text>
<text x="360" y="262" text-anchor="middle" class="c">the GraphQL server resolves each field, possibly from several services</text>
</g>
</svg>
<figcaption>GraphQL moves the choice of data shape from the server to the client.</figcaption>
</figure>

`graphql_app.py` uses the Strawberry library. Types are Python classes; fields that need work, such as following a book to its author, are resolver methods:

```python
@strawberry.type
class Book:
    id: int
    title: str
    year: int | None
    author_id: strawberry.Private[int]

    @strawberry.field
    def author(self) -> Author:
        return Author(id=self.author_id, name=AUTHORS[self.author_id])


@strawberry.type
class Query:
    @strawberry.field
    def books(self, year_after: int | None = None) -> list[Book]:
        return [to_book(b) for b in BOOKS if year_after is None or (b["year"] or 0) > year_after]
```

Run `fastapi dev graphql_app.py` and open **http://127.0.0.1:8000/graphql** for GraphiQL, an in-browser editor with autocompletion driven by the schema. Or use curl; every GraphQL request is a `POST` with the query in JSON:

```bash
curl -s http://127.0.0.1:8000/graphql -H "Content-Type: application/json" \
     -d '{"query": "{ authors { name books { title year } } }"}'
```

```json
{"data":{"authors":[{"name":"Jane Austen","books":[{"title":"Pride and Prejudice","year":1813},{"title":"Emma","year":1815}]},
                    {"name":"Frank Herbert","books":[{"title":"Dune","year":1965}]}]}}
```

Changes are **mutations**:

```bash
curl -s http://127.0.0.1:8000/graphql -H "Content-Type: application/json" \
     -d '{"query": "mutation { addBook(title: \"Persuasion\", authorId: 1, year: 1817) { id title author { name } } }"}'
```

```json
{"data":{"addBook":{"id":4,"title":"Persuasion","author":{"name":"Jane Austen"}}}}
```

Asking for a field that does not exist is caught by the schema before any resolver runs. Note that the status is still `200`; GraphQL reports errors in an `errors` array:

```json
{"data":null,"errors":[{"message":"Cannot query field 'isbn' on type 'Book'.","locations":[{"line":1,"column":23}]}]}
```

GraphQL's strengths are flexible fetching, one round trip for nested data, and a strongly typed, self-describing schema. Its costs: HTTP caching does not apply to `POST` queries, every resolver needs its own authorization check, the N+1 problem returns unless resolvers batch their database calls (the "DataLoader" pattern), and a deeply nested query can be very expensive, so production servers limit **query depth and complexity** (OWASP API4 again).

## gRPC

**gRPC**, from Google (2015), is a remote procedure call framework. Its contract is a `.proto` file in the **Protocol Buffers** language:

```protobuf
syntax = "proto3";

package library.v1;

message Book {
  int32 id = 1;
  string title = 2;
  string author = 3;
  int32 year = 4;
}

service Library {
  rpc GetBook(GetBookRequest) returns (Book);                 // unary: one request, one reply
  rpc ListBooks(ListBooksRequest) returns (stream Book);      // server streaming: one request, many replies
}
```

<figure class="diagram">
<svg viewBox="0 0 720 250" style="width:100%;height:auto;max-width:720px" role="img" aria-label="How gRPC works: a .proto file defines messages and services; the protoc compiler generates client stubs and server base classes for each language; client and server exchange compact Protocol Buffers messages over HTTP/2, with deadlines, streaming, and standard status codes." xmlns="http://www.w3.org/2000/svg">
<style>
.a12b{ font-family:var(--sans),sans-serif; }
.a12b .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a12b .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a12b .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a12b .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a12b .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a12b .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a12b .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a12b .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a12b .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a12b .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a12b .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a12b .s{ fill:var(--text-dim); font-size:13px; }
.a12b .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a12b .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a12b .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a12b .c{ fill:var(--text-faint); font-size:12.5px; }
.a12b .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a12b .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a12b .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a12b .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a12b-a); }
.a12b .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a12b-a); marker-start:url(#a12b-s); }
.a12b .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a12b-g); }
.a12b .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a12b-a); }
.a12b .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a12b .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a12b .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a12b .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a12b .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a12b .ks-blue{ fill:#185FA5; font-size:13px; }
.a12b .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a12b .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12b .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a12b .kb-blue, :root[data-theme="dark"] .a12b .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a12b .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a12b .kh-blue{ fill:#85B7EB; }
.a12b .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a12b-blue); }
.a12b .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12b-blue); }
.a12b .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a12b .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a12b .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a12b .ks-teal{ fill:#0F6E56; font-size:13px; }
.a12b .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a12b .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12b .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a12b .kb-teal, :root[data-theme="dark"] .a12b .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a12b .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a12b .kh-teal{ fill:#5DCAA5; }
.a12b .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a12b-teal); }
.a12b .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12b-teal); }
.a12b .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a12b .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a12b .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a12b .ks-amber{ fill:#854F0B; font-size:13px; }
.a12b .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a12b .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12b .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a12b .kb-amber, :root[data-theme="dark"] .a12b .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a12b .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a12b .kh-amber{ fill:#EF9F27; }
.a12b .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a12b-amber); }
.a12b .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12b-amber); }
.a12b .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a12b .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a12b .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a12b .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a12b .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a12b .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12b .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a12b .kb-gray, :root[data-theme="dark"] .a12b .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a12b .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a12b .kh-gray{ fill:#B4B2A9; }
.a12b .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a12b-gray); }
.a12b .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12b-gray); }
.a12b .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a12b-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a12b-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a12b-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a12b-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a12b-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a12b-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a12b-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a12b">
<rect x="20" y="90" width="150" height="60" rx="7" class="k-amber"/>
<text x="95.0" y="115.5" text-anchor="middle" class="kb-amber">library.proto</text>
<text x="95.0" y="133.5" text-anchor="middle" class="ks-amber">the contract</text>
<rect x="220" y="90" width="130" height="60" rx="7" class="k-gray"/>
<text x="285.0" y="115.5" text-anchor="middle" class="kb-gray">protoc</text>
<text x="285.0" y="133.5" text-anchor="middle" class="ks-gray">code generator</text>
<line x1="172" y1="120" x2="218" y2="120" class="ar"/>
<rect x="400" y="30" width="130" height="56" rx="7" class="k-blue"/>
<text x="465.0" y="53.5" text-anchor="middle" class="kb-blue">client stub</text>
<text x="465.0" y="71.5" text-anchor="middle" class="ks-blue">Python, Go...</text>
<rect x="400" y="154" width="130" height="56" rx="7" class="k-teal"/>
<text x="465.0" y="177.5" text-anchor="middle" class="kb-teal">server base</text>
<text x="465.0" y="195.5" text-anchor="middle" class="ks-teal">any language</text>
<line x1="352" y1="110" x2="398" y2="60" class="ar"/>
<line x1="352" y1="130" x2="398" y2="182" class="ar"/>
<rect x="580" y="30" width="120" height="180" rx="7" class="pnl"/>
<text x="640.0" y="80.5" text-anchor="middle" class="b">HTTP/2</text>
<text x="640.0" y="102.5" text-anchor="middle" class="c">binary</text>
<text x="640.0" y="124.5" text-anchor="middle" class="c">protobuf</text>
<text x="640.0" y="146.5" text-anchor="middle" class="kb-teal">26 bytes</text>
<text x="640.0" y="168.5" text-anchor="middle" class="c">vs 67 in JSON</text>
<line x1="532" y1="58" x2="578" y2="58" class="ar-blue"/>
<line x1="578" y1="182" x2="532" y2="182" class="ar-teal"/>
</g>
</svg>
<figcaption>Strong contracts and small, fast messages: well suited to calls between services, less so to browsers.</figcaption>
</figure>

The numbers after each field are **field tags**: on the wire, messages carry tags instead of names, which makes them compact. Never reuse or change a tag; that is how protobuf stays backward compatible. Generate the Python code, then run the server and client from the `grpc_demo` folder:

```bash
cd grpc_demo
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. library.proto
python server.py          # in one terminal
python client.py          # in another
```

The client calls methods on a generated **stub** as if they were local functions, always with a deadline:

```python
book = stub.GetBook(library_pb2.GetBookRequest(id=3), timeout=2)    # always set a deadline
for b in stub.ListBooks(library_pb2.ListBooksRequest(author="Jane Austen"), timeout=2):
    print("streamed:", b.title)
```

```text
unary: Dune 1965
streamed: Pride and Prejudice
streamed: Emma
error: NOT_FOUND - Book 99 does not exist
wire size of one Book message: 26 bytes
```

The same book as JSON is 67 bytes. gRPC has its own status codes, such as `NOT_FOUND`, `INVALID_ARGUMENT`, `UNAUTHENTICATED`, and `DEADLINE_EXCEEDED`.

<figure class="diagram">
<svg viewBox="0 0 720 262" style="width:100%;height:auto;max-width:720px" role="img" aria-label="The four kinds of gRPC call: unary, one request and one response; server streaming, one request and a stream of responses; client streaming, a stream of requests and one response; and bidirectional streaming, both sides streaming independently." xmlns="http://www.w3.org/2000/svg">
<style>
.a12c{ font-family:var(--sans),sans-serif; }
.a12c .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a12c .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a12c .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a12c .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a12c .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a12c .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a12c .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a12c .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a12c .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a12c .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a12c .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a12c .s{ fill:var(--text-dim); font-size:13px; }
.a12c .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a12c .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a12c .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a12c .c{ fill:var(--text-faint); font-size:12.5px; }
.a12c .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a12c .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a12c .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a12c .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a12c-a); }
.a12c .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a12c-a); marker-start:url(#a12c-s); }
.a12c .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a12c-g); }
.a12c .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a12c-a); }
.a12c .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a12c .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a12c .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a12c .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a12c .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a12c .ks-blue{ fill:#185FA5; font-size:13px; }
.a12c .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a12c .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12c .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a12c .kb-blue, :root[data-theme="dark"] .a12c .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a12c .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a12c .kh-blue{ fill:#85B7EB; }
.a12c .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a12c-blue); }
.a12c .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12c-blue); }
.a12c .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a12c .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a12c .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a12c .ks-teal{ fill:#0F6E56; font-size:13px; }
.a12c .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a12c .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12c .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a12c .kb-teal, :root[data-theme="dark"] .a12c .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a12c .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a12c .kh-teal{ fill:#5DCAA5; }
.a12c .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a12c-teal); }
.a12c .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12c-teal); }
.a12c .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a12c .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a12c .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a12c .ks-purple{ fill:#534AB7; font-size:13px; }
.a12c .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a12c .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12c .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a12c .kb-purple, :root[data-theme="dark"] .a12c .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a12c .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a12c .kh-purple{ fill:#AFA9EC; }
.a12c .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a12c-purple); }
.a12c .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12c-purple); }
.a12c .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
</style>
<defs><marker id="a12c-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a12c-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a12c-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a12c-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a12c-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a12c-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker></defs>
<g class="a12c">
<rect x="20" y="16" width="160" height="36" rx="7" class="k-teal"/>
<text x="100.0" y="38.5" text-anchor="middle" class="kb-teal">unary</text>
<text x="60" y="76" text-anchor="middle" class="s">client</text>
<text x="140" y="76" text-anchor="middle" class="s">server</text>
<line x1="60" y1="96" x2="138" y2="96" class="ar-blue"/>
<line x1="140" y1="130" x2="62" y2="130" class="ar-teal"/>
<rect x="192" y="16" width="160" height="36" rx="7" class="k-purple"/>
<text x="272.0" y="38.5" text-anchor="middle" class="kb-purple">server streaming</text>
<text x="232" y="76" text-anchor="middle" class="s">client</text>
<text x="312" y="76" text-anchor="middle" class="s">server</text>
<line x1="232" y1="96" x2="310" y2="96" class="ar-blue"/>
<line x1="312" y1="130" x2="234" y2="130" class="ar-teal"/>
<line x1="312" y1="152" x2="234" y2="152" class="ar-teal"/>
<line x1="312" y1="174" x2="234" y2="174" class="ar-teal"/>
<rect x="364" y="16" width="160" height="36" rx="7" class="k-purple"/>
<text x="444.0" y="38.5" text-anchor="middle" class="kb-purple">client streaming</text>
<text x="404" y="76" text-anchor="middle" class="s">client</text>
<text x="484" y="76" text-anchor="middle" class="s">server</text>
<line x1="404" y1="96" x2="482" y2="96" class="ar-blue"/>
<line x1="404" y1="118" x2="482" y2="118" class="ar-blue"/>
<line x1="404" y1="140" x2="482" y2="140" class="ar-blue"/>
<line x1="484" y1="174" x2="406" y2="174" class="ar-teal"/>
<rect x="536" y="16" width="160" height="36" rx="7" class="k-purple"/>
<text x="616.0" y="38.5" text-anchor="middle" class="kb-purple">bidirectional</text>
<text x="576" y="76" text-anchor="middle" class="s">client</text>
<text x="656" y="76" text-anchor="middle" class="s">server</text>
<line x1="576" y1="96" x2="654" y2="96" class="ar-blue"/>
<line x1="576" y1="118" x2="654" y2="118" class="ar-blue"/>
<line x1="576" y1="140" x2="654" y2="140" class="ar-blue"/>
<line x1="656" y1="174" x2="578" y2="174" class="ar-teal"/>
<line x1="656" y1="196" x2="578" y2="196" class="ar-teal"/>
<line x1="656" y1="218" x2="578" y2="218" class="ar-teal"/>
<text x="360" y="252" text-anchor="middle" class="c">the lab implements GetBook (unary) and ListBooks (server streaming)</text>
</g>
</svg>
<figcaption>Streaming is built in, because HTTP/2 can carry many messages in both directions on one connection.</figcaption>
</figure>

gRPC runs over **HTTP/2**, which multiplexes many calls on one connection and supports streaming in both directions. It is excellent between internal services: fast, strictly typed, with generated clients in many languages. It is less suited to browsers, which cannot speak raw gRPC (gRPC-Web and the Connect protocol bridge the gap), and binary messages are harder to inspect with everyday tools such as curl, though `grpcurl` helps.

## Webhooks

Sometimes your system needs to know when something happens in another one: a payment succeeds, a pull request is opened. Asking repeatedly ("polling") is wasteful and slow. A **webhook** reverses the direction: you register a URL, and the provider calls it.

<figure class="diagram">
<svg viewBox="0 0 720 270" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Polling versus webhooks. With polling, the client asks again and again whether anything happened, and most answers are no. With a webhook, the client registers a URL once, and the provider sends an HTTP POST to it when an event happens, signed so the receiver can verify it came from the provider." xmlns="http://www.w3.org/2000/svg">
<style>
.a12d{ font-family:var(--sans),sans-serif; }
.a12d .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a12d .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a12d .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a12d .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a12d .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a12d .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a12d .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a12d .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a12d .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a12d .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a12d .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a12d .s{ fill:var(--text-dim); font-size:13px; }
.a12d .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a12d .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a12d .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a12d .c{ fill:var(--text-faint); font-size:12.5px; }
.a12d .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a12d .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a12d .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a12d .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a12d-a); }
.a12d .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a12d-a); marker-start:url(#a12d-s); }
.a12d .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a12d-g); }
.a12d .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a12d-a); }
.a12d .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a12d .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a12d .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a12d .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a12d .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a12d .ks-blue{ fill:#185FA5; font-size:13px; }
.a12d .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a12d .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12d .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a12d .kb-blue, :root[data-theme="dark"] .a12d .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a12d .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a12d .kh-blue{ fill:#85B7EB; }
.a12d .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a12d-blue); }
.a12d .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12d-blue); }
.a12d .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a12d .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a12d .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a12d .ks-teal{ fill:#0F6E56; font-size:13px; }
.a12d .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a12d .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12d .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a12d .kb-teal, :root[data-theme="dark"] .a12d .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a12d .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a12d .kh-teal{ fill:#5DCAA5; }
.a12d .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a12d-teal); }
.a12d .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12d-teal); }
.a12d .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a12d .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a12d .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a12d .ks-amber{ fill:#854F0B; font-size:13px; }
.a12d .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a12d .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12d .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a12d .kb-amber, :root[data-theme="dark"] .a12d .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a12d .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a12d .kh-amber{ fill:#EF9F27; }
.a12d .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a12d-amber); }
.a12d .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12d-amber); }
.a12d .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a12d .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a12d .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a12d .ks-green{ fill:#3B6D11; font-size:13px; }
.a12d .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a12d .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12d .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a12d .kb-green, :root[data-theme="dark"] .a12d .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a12d .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a12d .kh-green{ fill:#97C459; }
.a12d .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a12d-green); }
.a12d .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12d-green); }
.a12d .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a12d .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a12d .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a12d .ks-red{ fill:#A32D2D; font-size:13px; }
.a12d .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a12d .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12d .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a12d .kb-red, :root[data-theme="dark"] .a12d .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a12d .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a12d .kh-red{ fill:#F09595; }
.a12d .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a12d-red); }
.a12d .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12d-red); }
.a12d .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
</style>
<defs><marker id="a12d-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a12d-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a12d-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a12d-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a12d-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a12d-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a12d-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a12d-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker></defs>
<g class="a12d">
<text x="20" y="24" text-anchor="start" class="kh-blue">polling</text>
<line x1="30" y1="40" x2="30" y2="70" class="ar-blue"/>
<text x="30" y="90" text-anchor="middle" class="kh-red">no</text>
<line x1="94" y1="40" x2="94" y2="70" class="ar-blue"/>
<text x="94" y="90" text-anchor="middle" class="kh-red">no</text>
<line x1="158" y1="40" x2="158" y2="70" class="ar-blue"/>
<text x="158" y="90" text-anchor="middle" class="kh-red">no</text>
<line x1="222" y1="40" x2="222" y2="70" class="ar-blue"/>
<text x="222" y="90" text-anchor="middle" class="kh-red">no</text>
<line x1="286" y1="40" x2="286" y2="70" class="ar-blue"/>
<text x="286" y="90" text-anchor="middle" class="kh-green">yes!</text>
<text x="370" y="24" text-anchor="start" class="kh-teal">webhook</text>
<rect x="370" y="36" width="150" height="50" rx="7" class="k-teal"/>
<text x="445.0" y="65.5" text-anchor="middle" class="kb-teal">provider</text>
<rect x="550" y="36" width="150" height="50" rx="7" class="k-blue"/>
<text x="625.0" y="65.5" text-anchor="middle" class="kb-blue">your endpoint</text>
<line x1="522" y1="61" x2="548" y2="61" class="ar-teal"/>
<rect x="20" y="130" width="680" height="50" rx="7" class="k-amber"/>
<text x="360.0" y="150.5" text-anchor="middle" class="km-amber">POST /webhooks/orders</text>
<text x="360.0" y="168.5" text-anchor="middle" class="km-amber">Webhook-Signature: t=1794725300,v1=5f0c...</text>
<rect x="20" y="200" width="160" height="54" rx="6" class="pnl"/>
<text x="100.0" y="222.5" text-anchor="middle" class="c">verify HMAC</text>
<text x="100.0" y="240.5" text-anchor="middle" class="c">over the raw body</text>
<rect x="192" y="200" width="160" height="54" rx="6" class="pnl"/>
<text x="272.0" y="222.5" text-anchor="middle" class="c">reject old</text>
<text x="272.0" y="240.5" text-anchor="middle" class="c">timestamps</text>
<rect x="364" y="200" width="160" height="54" rx="6" class="pnl"/>
<text x="444.0" y="222.5" text-anchor="middle" class="c">ignore repeated</text>
<text x="444.0" y="240.5" text-anchor="middle" class="c">event ids</text>
<rect x="536" y="200" width="160" height="54" rx="6" class="pnl"/>
<text x="616.0" y="222.5" text-anchor="middle" class="c">answer fast,</text>
<text x="616.0" y="240.5" text-anchor="middle" class="c">process later</text>
</g>
</svg>
<figcaption>Webhooks are reversed APIs: the provider becomes the client. Treat every delivery as untrusted until verified.</figcaption>
</figure>

Because a webhook endpoint is a public URL that anyone can call, the receiver must check every delivery. `webhooks.py` shows the common scheme, used in similar forms by Stripe, GitHub, and the Standard Webhooks specification: an HMAC-SHA256 signature over a timestamp and the raw body, with a secret shared in advance:

```python
def sign(timestamp: int, body: bytes) -> str:
    mac = hmac.new(SECRET, f"{timestamp}.".encode() + body, hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={mac}"


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
```

The `verify` function rejects timestamps more than five minutes old, which defeats replaying a captured delivery, and compares signatures with `hmac.compare_digest`. Run the receiver with `fastapi dev webhooks.py`, then `python webhooks.py` sends a signed `order.paid` event; it prints `delivered: 204`, and the receiver logs `processing order.paid {'order_id': 42, 'total': 19.5}`.

Providers retry failed deliveries, so receivers must be **idempotent** (deduplicate on the event ID) and should answer quickly, queueing the real work. For sending events between your own services at scale, a **message broker** such as Kafka, RabbitMQ, or NATS is usually a better fit than webhooks; AsyncAPI documents those interfaces.

## Server-sent events and WebSockets

<figure class="diagram">
<svg viewBox="0 0 720 240" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Server-sent events versus WebSockets. Server-sent events use one ordinary HTTP response that stays open and carries a stream of text events from server to client, with automatic reconnection. WebSockets upgrade the connection to a full-duplex channel where both sides send messages at any time." xmlns="http://www.w3.org/2000/svg">
<style>
.a12e{ font-family:var(--sans),sans-serif; }
.a12e .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a12e .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a12e .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a12e .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a12e .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a12e .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a12e .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a12e .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a12e .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a12e .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a12e .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a12e .s{ fill:var(--text-dim); font-size:13px; }
.a12e .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a12e .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a12e .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a12e .c{ fill:var(--text-faint); font-size:12.5px; }
.a12e .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a12e .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a12e .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a12e .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a12e-a); }
.a12e .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a12e-a); marker-start:url(#a12e-s); }
.a12e .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a12e-g); }
.a12e .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a12e-a); }
.a12e .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a12e .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a12e .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a12e .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a12e .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a12e .ks-blue{ fill:#185FA5; font-size:13px; }
.a12e .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a12e .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12e .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a12e .kb-blue, :root[data-theme="dark"] .a12e .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a12e .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a12e .kh-blue{ fill:#85B7EB; }
.a12e .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a12e-blue); }
.a12e .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12e-blue); }
.a12e .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a12e .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a12e .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a12e .ks-teal{ fill:#0F6E56; font-size:13px; }
.a12e .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a12e .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12e .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a12e .kb-teal, :root[data-theme="dark"] .a12e .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a12e .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a12e .kh-teal{ fill:#5DCAA5; }
.a12e .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a12e-teal); }
.a12e .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12e-teal); }
.a12e .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a12e .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a12e .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a12e .ks-purple{ fill:#534AB7; font-size:13px; }
.a12e .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a12e .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12e .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a12e .kb-purple, :root[data-theme="dark"] .a12e .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a12e .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a12e .kh-purple{ fill:#AFA9EC; }
.a12e .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a12e-purple); }
.a12e .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12e-purple); }
.a12e .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
</style>
<defs><marker id="a12e-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a12e-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a12e-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a12e-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a12e-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a12e-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker></defs>
<g class="a12e">
<text x="20" y="24" text-anchor="start" class="kh-teal">server-sent events (SSE)</text>
<rect x="20" y="36" width="120" height="44" rx="7" class="k-blue"/>
<text x="80.0" y="62.5" text-anchor="middle" class="kb-blue">browser</text>
<rect x="240" y="36" width="120" height="44" rx="7" class="k-teal"/>
<text x="300.0" y="62.5" text-anchor="middle" class="kb-teal">server</text>
<line x1="238" y1="46" x2="142" y2="46" class="ar-teal"/>
<line x1="238" y1="58" x2="142" y2="58" class="ar-teal"/>
<line x1="238" y1="70" x2="142" y2="70" class="ar-teal"/>
<text x="20" y="104" text-anchor="start" class="s">plain HTTP, text/event-stream</text>
<text x="20" y="124" text-anchor="start" class="s">one way, auto-reconnect</text>
<text x="380" y="24" text-anchor="start" class="kh-purple">WebSocket</text>
<rect x="380" y="36" width="120" height="44" rx="7" class="k-blue"/>
<text x="440.0" y="62.5" text-anchor="middle" class="kb-blue">browser</text>
<rect x="580" y="36" width="120" height="44" rx="7" class="k-teal"/>
<text x="640.0" y="62.5" text-anchor="middle" class="kb-teal">server</text>
<line x1="502" y1="48" x2="578" y2="48" class="ar-blue"/>
<line x1="578" y1="60" x2="502" y2="60" class="ar-teal"/>
<line x1="502" y1="72" x2="578" y2="72" class="ar-blue"/>
<text x="380" y="104" text-anchor="start" class="s">upgrade from HTTP to ws://, wss://</text>
<text x="380" y="124" text-anchor="start" class="s">both ways, any time</text>
<rect x="20" y="156" width="340" height="64" rx="7" class="k-teal"/>
<text x="190.0" y="183.5" text-anchor="middle" class="ks-teal">notifications, progress, live feeds,</text>
<text x="190.0" y="201.5" text-anchor="middle" class="ks-teal">streaming AI responses</text>
<rect x="380" y="156" width="320" height="64" rx="7" class="k-purple"/>
<text x="540.0" y="183.5" text-anchor="middle" class="ks-purple">chat, games, collaborative</text>
<text x="540.0" y="201.5" text-anchor="middle" class="ks-purple">editing</text>
</g>
</svg>
<figcaption>If only the server needs to push, SSE is simpler. If both sides talk continuously, use WebSockets.</figcaption>
</figure>

**Server-sent events** (SSE) stream updates from server to browser over an ordinary HTTP response with the media type `text/event-stream`. Each event is a few lines of text ending with a blank line. `sse_app.py` streams stock levels:

```python
async def ticker(count: int):
    for i in range(1, count + 1):
        data = {"seq": i, "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "stock": {"Dune": 10 - i}}
        yield f"id: {i}\nevent: stock\ndata: {json.dumps(data)}\n\n"
        await asyncio.sleep(1)
```

```bash
curl -N http://127.0.0.1:8000/events
```

```text
id: 1
event: stock
data: {"seq": 1, "time": "2026-11-15T06:53:22+00:00", "stock": {"Dune": 9}}

id: 2
event: stock
data: {"seq": 2, "time": "2026-11-15T06:53:23+00:00", "stock": {"Dune": 8}}
```

In a browser, `new EventSource("/events")` receives these, and reconnects automatically, sending the last `id` it saw so the server can resume. SSE is also how many AI model APIs stream their responses token by token.

**WebSockets** (RFC 6455) upgrade an HTTP connection into a two-way channel where either side can send messages at any time. They suit chat, multiplayer games, and collaborative editing. FastAPI supports them with `@app.websocket`. They need more care than SSE: authentication happens at the upgrade, connections are long-lived and stateful, and load balancers must support them.

## Choosing a style

<figure class="diagram">
<svg viewBox="0 0 720 300" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Choosing an API style. Public or web-facing resource APIs: REST. Clients with varied data needs, such as several frontends over one backend: GraphQL. Internal service-to-service calls needing speed and strict contracts: gRPC. Telling another system that something happened: webhooks or a message broker. Live updates to a browser: SSE or WebSockets." xmlns="http://www.w3.org/2000/svg">
<style>
.a12f{ font-family:var(--sans),sans-serif; }
.a12f .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a12f .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a12f .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a12f .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a12f .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a12f .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a12f .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a12f .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a12f .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a12f .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a12f .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a12f .s{ fill:var(--text-dim); font-size:13px; }
.a12f .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a12f .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a12f .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a12f .c{ fill:var(--text-faint); font-size:12.5px; }
.a12f .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a12f .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a12f .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a12f .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a12f-a); }
.a12f .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a12f-a); marker-start:url(#a12f-s); }
.a12f .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a12f-g); }
.a12f .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a12f-a); }
.a12f .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a12f .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a12f .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a12f .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a12f .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a12f .ks-blue{ fill:#185FA5; font-size:13px; }
.a12f .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a12f .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12f .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a12f .kb-blue, :root[data-theme="dark"] .a12f .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a12f .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a12f .kh-blue{ fill:#85B7EB; }
.a12f .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a12f-blue); }
.a12f .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12f-blue); }
.a12f .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a12f .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a12f .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a12f .ks-teal{ fill:#0F6E56; font-size:13px; }
.a12f .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a12f .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12f .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a12f .kb-teal, :root[data-theme="dark"] .a12f .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a12f .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a12f .kh-teal{ fill:#5DCAA5; }
.a12f .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a12f-teal); }
.a12f .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12f-teal); }
.a12f .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a12f .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a12f .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a12f .ks-amber{ fill:#854F0B; font-size:13px; }
.a12f .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a12f .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12f .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a12f .kb-amber, :root[data-theme="dark"] .a12f .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a12f .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a12f .kh-amber{ fill:#EF9F27; }
.a12f .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a12f-amber); }
.a12f .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12f-amber); }
.a12f .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a12f .k-coral{ fill:#FAECE7; stroke:#D85A30; stroke-width:1.6; }
.a12f .kb-coral{ fill:#712B13; font-size:13px; font-weight:700; }
.a12f .ks-coral{ fill:#993C1D; font-size:13px; }
.a12f .km-coral{ fill:#712B13; font-size:12.5px; font-family:var(--mono),monospace; }
.a12f .kh-coral{ fill:#993C1D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12f .k-coral{ fill:#712B13; stroke:#F0997B; }
:root[data-theme="dark"] .a12f .kb-coral, :root[data-theme="dark"] .a12f .km-coral{ fill:#FAECE7; }
:root[data-theme="dark"] .a12f .ks-coral{ fill:#F5C4B3; }
:root[data-theme="dark"] .a12f .kh-coral{ fill:#F0997B; }
.a12f .ar-coral{ stroke:#D85A30; stroke-width:2; fill:none; marker-end:url(#a12f-coral); }
.a12f .ad-coral{ stroke:#D85A30; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12f-coral); }
.a12f .ln-coral{ stroke:#D85A30; stroke-width:2; fill:none; }
.a12f .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a12f .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a12f .ks-purple{ fill:#534AB7; font-size:13px; }
.a12f .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a12f .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a12f .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a12f .kb-purple, :root[data-theme="dark"] .a12f .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a12f .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a12f .kh-purple{ fill:#AFA9EC; }
.a12f .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a12f-purple); }
.a12f .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a12f-purple); }
.a12f .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
</style>
<defs><marker id="a12f-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a12f-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a12f-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a12f-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a12f-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a12f-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a12f-coral" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#D85A30"/></marker><marker id="a12f-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker></defs>
<g class="a12f">
<rect x="20" y="16" width="420" height="44" rx="6" class="pnl"/>
<text x="230.0" y="42.5" text-anchor="middle" class="s">public API, broad audience, cacheable</text>
<line x1="442" y1="38" x2="476" y2="38" class="ar"/>
<rect x="480" y="16" width="220" height="44" rx="7" class="k-teal"/>
<text x="590.0" y="42.5" text-anchor="middle" class="kb-teal">REST + OpenAPI</text>
<rect x="20" y="72" width="420" height="44" rx="6" class="pnl"/>
<text x="230.0" y="98.5" text-anchor="middle" class="s">many clients needing different data shapes</text>
<line x1="442" y1="94" x2="476" y2="94" class="ar"/>
<rect x="480" y="72" width="220" height="44" rx="7" class="k-purple"/>
<text x="590.0" y="98.5" text-anchor="middle" class="kb-purple">GraphQL</text>
<rect x="20" y="128" width="420" height="44" rx="6" class="pnl"/>
<text x="230.0" y="154.5" text-anchor="middle" class="s">internal services, low latency, strict types</text>
<line x1="442" y1="150" x2="476" y2="150" class="ar"/>
<rect x="480" y="128" width="220" height="44" rx="7" class="k-amber"/>
<text x="590.0" y="154.5" text-anchor="middle" class="kb-amber">gRPC</text>
<rect x="20" y="184" width="420" height="44" rx="6" class="pnl"/>
<text x="230.0" y="210.5" text-anchor="middle" class="s">notify another system that something happened</text>
<line x1="442" y1="206" x2="476" y2="206" class="ar"/>
<rect x="480" y="184" width="220" height="44" rx="7" class="k-coral"/>
<text x="590.0" y="210.5" text-anchor="middle" class="kb-coral">webhooks, message broker</text>
<rect x="20" y="240" width="420" height="44" rx="6" class="pnl"/>
<text x="230.0" y="266.5" text-anchor="middle" class="s">live updates to a browser</text>
<line x1="442" y1="262" x2="476" y2="262" class="ar"/>
<rect x="480" y="240" width="220" height="44" rx="7" class="k-blue"/>
<text x="590.0" y="266.5" text-anchor="middle" class="kb-blue">SSE or WebSocket</text>
</g>
</svg>
<figcaption>Most systems use several: REST at the edge, gRPC inside, webhooks between organisations.</figcaption>
</figure>

| | REST | GraphQL | gRPC | Webhooks | SSE / WebSocket |
|---|---|---|---|---|---|
| Transport | HTTP | HTTP `POST` | HTTP/2 | HTTP `POST`, reversed | HTTP stream / upgraded TCP |
| Format | JSON (usually) | JSON | Protobuf (binary) | JSON | Text / any |
| Contract | OpenAPI | GraphQL schema | `.proto` | Provider's docs, AsyncAPI | Ad hoc, AsyncAPI |
| Caching | Built in | Hard | None | Not applicable | Not applicable |
| Browser support | Native | Native | Needs a bridge | Not applicable | Native |
| Best for | Public resource APIs | Varied client needs | Internal services | Event notification | Live updates |

## Summary

- **GraphQL**: one endpoint, a typed schema, and client-chosen response shapes; mind authorization per resolver, N+1, and query cost.
- **gRPC**: protobuf contracts, generated stubs, HTTP/2 streaming, compact messages; ideal between services.
- **Webhooks**: the provider calls you; **verify signatures**, reject stale timestamps, and **deduplicate** events.
- **SSE** pushes events from server to browser over plain HTTP; **WebSockets** give full two-way messaging.
- Real systems mix styles: REST at the edge, gRPC inside, events between systems.
