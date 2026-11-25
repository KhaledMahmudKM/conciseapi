# Chapter 6: Building a REST API

This chapter implements the Library API designed in Chapter 5, in a single file, `library.py`, of about 150 lines. Along the way it covers the details that separate a demo from a usable API: separate input and output models, strict validation, proper status codes and headers, a standard error format, and pagination. It ends with a Python client.

## Models: one resource, several shapes

<figure class="diagram">
<svg viewBox="0 0 720 260" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Three Pydantic models for one resource: BookIn is what a client sends to create or replace a book; BookPatch has every field optional for partial updates; Book is what the server returns, adding the server-assigned id." xmlns="http://www.w3.org/2000/svg">
<style>
.a6a{ font-family:var(--sans),sans-serif; }
.a6a .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a6a .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a6a .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a6a .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a6a .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a6a .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a6a .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a6a .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a6a .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a6a .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a6a .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a6a .s{ fill:var(--text-dim); font-size:13px; }
.a6a .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a6a .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a6a .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a6a .c{ fill:var(--text-faint); font-size:12.5px; }
.a6a .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a6a .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a6a .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a6a .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a6a-a); }
.a6a .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a6a-a); marker-start:url(#a6a-s); }
.a6a .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a6a-g); }
.a6a .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a6a-a); }
.a6a .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a6a .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a6a .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a6a .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a6a .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a6a .ks-blue{ fill:#185FA5; font-size:13px; }
.a6a .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a6a .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a6a .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a6a .kb-blue, :root[data-theme="dark"] .a6a .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a6a .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a6a .kh-blue{ fill:#85B7EB; }
.a6a .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a6a-blue); }
.a6a .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a6a-blue); }
.a6a .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a6a .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a6a .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a6a .ks-teal{ fill:#0F6E56; font-size:13px; }
.a6a .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a6a .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a6a .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a6a .kb-teal, :root[data-theme="dark"] .a6a .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a6a .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a6a .kh-teal{ fill:#5DCAA5; }
.a6a .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a6a-teal); }
.a6a .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a6a-teal); }
.a6a .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a6a .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a6a .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a6a .ks-amber{ fill:#854F0B; font-size:13px; }
.a6a .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a6a .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a6a .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a6a .kb-amber, :root[data-theme="dark"] .a6a .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a6a .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a6a .kh-amber{ fill:#EF9F27; }
.a6a .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a6a-amber); }
.a6a .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a6a-amber); }
.a6a .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
</style>
<defs><marker id="a6a-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a6a-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a6a-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a6a-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a6a-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a6a-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker></defs>
<g class="a6a">
<rect x="20" y="20" width="216" height="50" rx="7" class="k-blue"/>
<text x="128.0" y="40.5" text-anchor="middle" class="kb-blue">BookIn</text>
<text x="128.0" y="58.5" text-anchor="middle" class="ks-blue">client sends (POST, PUT)</text>
<rect x="20" y="76" width="216" height="150" rx="6" class="pnl"/>
<text x="36" y="104" text-anchor="start" class="m">title: str</text>
<text x="36" y="134" text-anchor="start" class="m">author: str</text>
<text x="36" y="164" text-anchor="start" class="m">year: int | None</text>
<text x="36" y="194" text-anchor="start" class="m">isbn: str | None</text>
<rect x="252" y="20" width="216" height="50" rx="7" class="k-amber"/>
<text x="360.0" y="40.5" text-anchor="middle" class="kb-amber">BookPatch</text>
<text x="360.0" y="58.5" text-anchor="middle" class="ks-amber">client sends (PATCH)</text>
<rect x="252" y="76" width="216" height="150" rx="6" class="pnl"/>
<text x="268" y="104" text-anchor="start" class="m">title: str | None</text>
<text x="268" y="134" text-anchor="start" class="m">author: str | None</text>
<text x="268" y="164" text-anchor="start" class="m">year: int | None</text>
<text x="268" y="194" text-anchor="start" class="m">isbn: str | None</text>
<rect x="484" y="20" width="216" height="50" rx="7" class="k-teal"/>
<text x="592.0" y="40.5" text-anchor="middle" class="kb-teal">Book</text>
<text x="592.0" y="58.5" text-anchor="middle" class="ks-teal">server returns</text>
<rect x="484" y="76" width="216" height="150" rx="6" class="pnl"/>
<text x="500" y="104" text-anchor="start" class="kb-teal">id: int</text>
<text x="500" y="134" text-anchor="start" class="m">title: str</text>
<text x="500" y="164" text-anchor="start" class="m">author: str</text>
<text x="500" y="194" text-anchor="start" class="m">year, isbn</text>
<text x="360" y="250" text-anchor="middle" class="c">separate input and output models: clients can never set id, and new output fields never become inputs</text>
</g>
</svg>
<figcaption>One resource, several shapes. Keeping them separate is a correctness and a security decision.</figcaption>
</figure>

A book looks different depending on who is sending it:

```python
class BookIn(BaseModel):
    """What a client sends to create or replace a book."""
    model_config = ConfigDict(extra="forbid")       # reject unknown fields

    title: str = Field(min_length=1, max_length=200, examples=["Dune"])
    author: str = Field(min_length=1, max_length=100, examples=["Frank Herbert"])
    year: int | None = Field(default=None, ge=0, le=2100, examples=[1965])
    isbn: str | None = Field(default=None, pattern=r"^\d{13}$", examples=["9780441013593"])


class BookPatch(BaseModel):
    """A partial update: every field is optional."""
    model_config = ConfigDict(extra="forbid")
    title: str | None = Field(default=None, min_length=1, max_length=200)
    # ... author, year, isbn, all optional


class Book(BaseModel):
    """What the server returns: a server-assigned id plus the book's fields."""
    id: int
    title: str
    author: str
    year: int | None = None
    isbn: str | None = None
```

Three decisions are worth noticing:

- **Clients never send `id`.** The server assigns it. Because `BookIn` has no `id` field and forbids extra fields, a client cannot choose or overwrite one.
- **`extra="forbid"`** rejects unknown fields instead of silently ignoring them. A client that sends `"titel"` gets an error instead of a book without a title, and an attacker cannot slip in fields such as `"role": "admin"` (Chapter 9).
- **Every field has limits.** Maximum lengths and ranges protect storage, and examples appear in the generated documentation.

## Endpoints

Each endpoint is a short function. Reading and creating:

```python
@app.get("/books/{book_id}", response_model=Book, tags=["books"], summary="Get one book",
         responses={404: {"description": "No such book"}})
def get_book(book_id: int):
    return get_or_404(book_id)


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED, tags=["books"],
          summary="Create a book")
def create_book(data: BookIn, response: Response):
    book = add(data)
    response.headers["Location"] = f"/books/{book.id}"
    return book
```

- `book_id: int` in the path means `/books/abc` is rejected with `422` before your code runs.
- `data: BookIn` tells FastAPI to read the JSON body, validate it against `BookIn`, and pass you a typed object.
- `response_model=Book` filters the response to exactly the fields of `Book`, whatever the function returns. This is a safety net against leaking internal fields.
- `status_code=201` and the `Location` header follow the design.

<figure class="diagram">
<svg viewBox="0 0 720 300" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Creating a book: the client sends POST /books with JSON; FastAPI validates it against BookIn; the handler stores it and assigns id 6; the server responds 201 Created with a Location header /books/6 and the stored book; the client can then GET /books/6." xmlns="http://www.w3.org/2000/svg">
<style>
.a6b{ font-family:var(--sans),sans-serif; }
.a6b .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a6b .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a6b .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a6b .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a6b .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a6b .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a6b .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a6b .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a6b .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a6b .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a6b .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a6b .s{ fill:var(--text-dim); font-size:13px; }
.a6b .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a6b .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a6b .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a6b .c{ fill:var(--text-faint); font-size:12.5px; }
.a6b .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a6b .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a6b .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a6b .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a6b-a); }
.a6b .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a6b-a); marker-start:url(#a6b-s); }
.a6b .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a6b-g); }
.a6b .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a6b-a); }
.a6b .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a6b .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a6b .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a6b .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a6b .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a6b .ks-blue{ fill:#185FA5; font-size:13px; }
.a6b .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a6b .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a6b .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a6b .kb-blue, :root[data-theme="dark"] .a6b .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a6b .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a6b .kh-blue{ fill:#85B7EB; }
.a6b .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a6b-blue); }
.a6b .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a6b-blue); }
.a6b .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a6b .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a6b .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a6b .ks-teal{ fill:#0F6E56; font-size:13px; }
.a6b .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a6b .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a6b .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a6b .kb-teal, :root[data-theme="dark"] .a6b .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a6b .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a6b .kh-teal{ fill:#5DCAA5; }
.a6b .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a6b-teal); }
.a6b .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a6b-teal); }
.a6b .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a6b .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a6b .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a6b .ks-purple{ fill:#534AB7; font-size:13px; }
.a6b .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a6b .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a6b .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a6b .kb-purple, :root[data-theme="dark"] .a6b .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a6b .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a6b .kh-purple{ fill:#AFA9EC; }
.a6b .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a6b-purple); }
.a6b .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a6b-purple); }
.a6b .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
</style>
<defs><marker id="a6b-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a6b-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a6b-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a6b-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a6b-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a6b-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker></defs>
<g class="a6b">
<rect x="30" y="16" width="140" height="40" rx="7" class="k-blue"/>
<text x="100.0" y="40.5" text-anchor="middle" class="kb-blue">client</text>
<rect x="290" y="16" width="140" height="40" rx="7" class="k-teal"/>
<text x="360.0" y="40.5" text-anchor="middle" class="kb-teal">FastAPI</text>
<rect x="550" y="16" width="140" height="40" rx="7" class="k-purple"/>
<text x="620.0" y="40.5" text-anchor="middle" class="kb-purple">storage</text>
<line x1="100" y1="56" x2="100" y2="290" class="gd"/>
<line x1="360" y1="56" x2="360" y2="290" class="gd"/>
<line x1="620" y1="56" x2="620" y2="290" class="gd"/>
<line x1="102" y1="86" x2="358" y2="86" class="ar-blue"/>
<text x="230.0" y="79" text-anchor="middle" class="s">POST /books  {title, author}</text>
<line x1="362" y1="124" x2="618" y2="124" class="ar-teal"/>
<text x="490.0" y="117" text-anchor="middle" class="s">validate, then store</text>
<line x1="618" y1="162" x2="362" y2="162" class="ar-purple"/>
<text x="490.0" y="155" text-anchor="middle" class="s">id = 6</text>
<line x1="358" y1="200" x2="102" y2="200" class="ar-teal"/>
<text x="230.0" y="193" text-anchor="middle" class="s">201 Created, Location: /books/6</text>
<line x1="102" y1="244" x2="358" y2="244" class="ar-blue"/>
<text x="230.0" y="237" text-anchor="middle" class="s">GET /books/6</text>
<line x1="358" y1="276" x2="102" y2="276" class="ar-teal"/>
<text x="230.0" y="269" text-anchor="middle" class="s">200 OK  {id: 6, ...}</text>
</g>
</svg>
<figcaption>201 plus a Location header tells the client exactly where its new resource lives.</figcaption>
</figure>

Updating with `PATCH` relies on knowing which fields the client actually sent:

```python
@app.patch("/books/{book_id}", response_model=Book, tags=["books"], summary="Update some fields")
def update_book(book_id: int, changes: BookPatch):
    book = get_or_404(book_id)
    updated = book.model_copy(update=changes.model_dump(exclude_unset=True))
    books[book_id] = Book.model_validate(updated.model_dump())
    return books[book_id]
```

`exclude_unset=True` returns only the fields present in the request, so `{"year": 1966}` changes the year and nothing else, while `{"year": null}` explicitly clears it. That is the "absent versus null" distinction from Chapter 4, implemented.

Deleting returns `204 No Content` and no body:

```python
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["books"])
def delete_book(book_id: int):
    get_or_404(book_id)
    del books[book_id]
```

The example keeps books in a dictionary so that it runs anywhere with no database. A real service would use a database through an ORM or a query library; the endpoints would barely change, which is the point of separating the contract from the implementation.

## Errors: problem details

Errors deserve as much design as successes. **RFC 9457, Problem Details for HTTP APIs**, standardises an error body with the content type `application/problem+json`:

<figure class="diagram">
<svg viewBox="0 0 720 270" style="width:100%;height:auto;max-width:720px" role="img" aria-label="An RFC 9457 problem details response for a validation error: status 422 with content type application/problem+json and a body with type, title, status, detail and instance members, plus an extension member errors listing each invalid field and its message." xmlns="http://www.w3.org/2000/svg">
<style>
.a6c{ font-family:var(--sans),sans-serif; }
.a6c .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a6c .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a6c .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a6c .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a6c .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a6c .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a6c .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a6c .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a6c .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a6c .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a6c .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a6c .s{ fill:var(--text-dim); font-size:13px; }
.a6c .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a6c .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a6c .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a6c .c{ fill:var(--text-faint); font-size:12.5px; }
.a6c .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a6c .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a6c .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a6c .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a6c-a); }
.a6c .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a6c-a); marker-start:url(#a6c-s); }
.a6c .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a6c-g); }
.a6c .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a6c-a); }
.a6c .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a6c .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a6c .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a6c .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a6c .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a6c .ks-amber{ fill:#854F0B; font-size:13px; }
.a6c .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a6c .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a6c .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a6c .kb-amber, :root[data-theme="dark"] .a6c .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a6c .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a6c .kh-amber{ fill:#EF9F27; }
.a6c .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a6c-amber); }
.a6c .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a6c-amber); }
.a6c .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
</style>
<defs><marker id="a6c-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a6c-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a6c-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a6c-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker></defs>
<g class="a6c">
<rect x="20" y="20" width="300" height="40" rx="5" class="k-amber"/>
<text x="170.0" y="44.5" text-anchor="middle" class="km-amber">HTTP/1.1 422 Unprocessable Content</text>
<rect x="340" y="20" width="360" height="40" rx="5" class="k-amber"/>
<text x="520.0" y="44.5" text-anchor="middle" class="km-amber">Content-Type: application/problem+json</text>
<rect x="20" y="70" width="680" height="184" rx="6" class="pnl"/>
<text x="36" y="94" text-anchor="start" class="m">{</text>
<text x="51.0" y="115" text-anchor="start" class="m">"type": "about:blank",</text>
<text x="51.0" y="136" text-anchor="start" class="m">"title": "Validation failed",</text>
<text x="51.0" y="157" text-anchor="start" class="m">"status": 422,</text>
<text x="51.0" y="178" text-anchor="start" class="m">"detail": "The request body or parameters are invalid.",</text>
<text x="51.0" y="199" text-anchor="start" class="m">"instance": "/books",</text>
<text x="51.0" y="220" text-anchor="start" class="m">"errors": [{"field": "title", "message": "String should have at least 1 character"}]</text>
<text x="36" y="241" text-anchor="start" class="m">}</text>
</g>
</svg>
<figcaption>One error format for the whole API, standardised by RFC 9457, with room for extension members such as the list of invalid fields.</figcaption>
</figure>

| Member | Meaning |
|---|---|
| `type` | A URI identifying the kind of problem; `about:blank` when the status code says enough |
| `title` | A short, human-readable summary of the problem type |
| `status` | The HTTP status code, repeated for convenience |
| `detail` | An explanation of this specific occurrence |
| `instance` | A URI for this occurrence, here the request path |

APIs may add extension members, such as the `errors` list of invalid fields. In `library.py`, two exception handlers convert all of FastAPI's errors to this format:

```python
def problem(status_code, title, detail, request, **extra):
    body = {"type": "about:blank", "title": title, "status": status_code,
            "detail": detail, "instance": request.url.path, **extra}
    return JSONResponse(body, status_code=status_code, media_type="application/problem+json")


@app.exception_handler(RequestValidationError)
async def validation_error(request, exc):
    errors = [{"field": ".".join(str(p) for p in e["loc"][1:]), "message": e["msg"]} for e in exc.errors()]
    return problem(422, "Validation failed", "The request body or parameters are invalid.", request,
                   errors=errors)
```

A good error message tells the client **what** went wrong and **how to fix it**, without exposing internals. Never return stack traces, SQL errors, or server paths to clients; log them on the server instead.

## Filtering, sorting, and pagination

The list endpoint takes its controls from the query string, each validated:

```python
@app.get("/books", response_model=BookPage, tags=["books"], summary="List books")
def list_books(request: Request, response: Response,
               author: str | None = Query(default=None, description="Filter: author contains this text"),
               year: int | None = Query(default=None),
               sort: str = Query(default="id", pattern=r"^-?(id|title|year)$"),
               limit: int = Query(default=10, ge=1, le=100),
               offset: int = Query(default=0, ge=0)):
    ...
    if offset + limit < len(items):          # tell the client where the next page is
        nxt = request.url.include_query_params(offset=offset + limit, limit=limit)
        response.headers["Link"] = f'<{nxt}>; rel="next"'
    return BookPage(items=page, total=len(items), limit=limit, offset=offset)
```

- `limit` has a **maximum of 100**: no client can ask for a million rows.
- `sort` must match a pattern, so only known fields can be sorted on. Never pass client input directly into a database `ORDER BY` clause.
- The `Link` header (RFC 8288) holds the next page's URL.

<figure class="diagram">
<svg viewBox="0 0 720 230" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Following pagination links: the client requests the first page, reads the Link header with rel next, requests that URL, and repeats until a response has no next link." xmlns="http://www.w3.org/2000/svg">
<style>
.a6d{ font-family:var(--sans),sans-serif; }
.a6d .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a6d .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a6d .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a6d .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a6d .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a6d .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a6d .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a6d .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a6d .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a6d .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a6d .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a6d .s{ fill:var(--text-dim); font-size:13px; }
.a6d .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a6d .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a6d .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a6d .c{ fill:var(--text-faint); font-size:12.5px; }
.a6d .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a6d .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a6d .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a6d .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a6d-a); }
.a6d .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a6d-a); marker-start:url(#a6d-s); }
.a6d .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a6d-g); }
.a6d .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a6d-a); }
.a6d .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a6d .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a6d .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a6d .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a6d .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a6d .ks-blue{ fill:#185FA5; font-size:13px; }
.a6d .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a6d .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a6d .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a6d .kb-blue, :root[data-theme="dark"] .a6d .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a6d .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a6d .kh-blue{ fill:#85B7EB; }
.a6d .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a6d-blue); }
.a6d .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a6d-blue); }
.a6d .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a6d .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a6d .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a6d .ks-teal{ fill:#0F6E56; font-size:13px; }
.a6d .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a6d .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a6d .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a6d .kb-teal, :root[data-theme="dark"] .a6d .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a6d .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a6d .kh-teal{ fill:#5DCAA5; }
.a6d .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a6d-teal); }
.a6d .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a6d-teal); }
.a6d .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a6d .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a6d .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a6d .ks-green{ fill:#3B6D11; font-size:13px; }
.a6d .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a6d .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a6d .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a6d .kb-green, :root[data-theme="dark"] .a6d .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a6d .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a6d .kh-green{ fill:#97C459; }
.a6d .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a6d-green); }
.a6d .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a6d-green); }
.a6d .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
</style>
<defs><marker id="a6d-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a6d-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a6d-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a6d-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a6d-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a6d-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker></defs>
<g class="a6d">
<rect x="20" y="40" width="200" height="44" rx="5" class="k-blue"/>
<text x="120.0" y="66.5" text-anchor="middle" class="km-blue">GET /books?limit=2</text>
<rect x="20" y="110" width="200" height="44" rx="5" class="k-teal"/>
<text x="120.0" y="136.5" text-anchor="middle" class="km-teal">Link: next offset=2</text>
<line x1="120" y1="86" x2="120" y2="108" class="ar"/>
<path d="M222 132 C 245 132, 245 62, 258 62" class="ar"/>
<rect x="260" y="40" width="200" height="44" rx="5" class="k-blue"/>
<text x="360.0" y="66.5" text-anchor="middle" class="km-blue">GET ...offset=2</text>
<rect x="260" y="110" width="200" height="44" rx="5" class="k-teal"/>
<text x="360.0" y="136.5" text-anchor="middle" class="km-teal">Link: next offset=4</text>
<line x1="360" y1="86" x2="360" y2="108" class="ar"/>
<path d="M462 132 C 485 132, 485 62, 498 62" class="ar"/>
<rect x="500" y="40" width="200" height="44" rx="5" class="k-blue"/>
<text x="600.0" y="66.5" text-anchor="middle" class="km-blue">GET ...offset=4</text>
<rect x="500" y="110" width="200" height="44" rx="5" class="k-green"/>
<text x="600.0" y="136.5" text-anchor="middle" class="km-green">no Link: done</text>
<line x1="600" y1="86" x2="600" y2="108" class="ar"/>
<text x="360" y="196" text-anchor="middle" class="c">the client never builds page URLs itself: the server says where to go next</text>
</g>
</svg>
<figcaption>Links in responses let the server change its pagination scheme without breaking clients.</figcaption>
</figure>

## Hands on: run and explore

```bash
fastapi dev library.py
```

Work through the API with curl. Each command shows a different part of the design:

```bash
curl -s "http://127.0.0.1:8000/books?author=austen&sort=-year"
curl -i "http://127.0.0.1:8000/books?limit=2"                    # note the Link header
curl -i -X POST http://127.0.0.1:8000/books \
     -H "Content-Type: application/json" \
     -d '{"title": "Kindred", "author": "Octavia E. Butler", "year": 1979}'   # 201 and Location
curl -s -X PATCH http://127.0.0.1:8000/books/6 \
     -H "Content-Type: application/json" -d '{"year": 1980}'
curl -i http://127.0.0.1:8000/books/999                            # 404 problem details
curl -s -X POST http://127.0.0.1:8000/books \
     -H "Content-Type: application/json" -d '{"title": "", "author": "X", "role": "admin"}'
```

The last request fails validation twice, and the response lists both problems:

```json
{"type": "about:blank", "title": "Validation failed", "status": 422,
 "detail": "The request body or parameters are invalid.", "instance": "/books",
 "errors": [{"field": "title", "message": "String should have at least 1 character"},
            {"field": "role", "message": "Extra inputs are not permitted"}]}
```

Data is kept in memory, so restarting the server restores the five starting books.

## A Python client

`client.py` uses the **requests** library to do the same things from code:

```python
session = requests.Session()               # reuses the TCP connection between calls
session.headers["Accept"] = "application/json"

resp = session.post(f"{BASE}/books", json={"title": "Kindred", "author": "Octavia E. Butler", "year": 1979},
                    timeout=5)
resp.raise_for_status()                    # turn 4xx and 5xx into exceptions
location = resp.headers["Location"]

url = f"{BASE}/books?limit=2"
while url:                                  # follow pagination links until there are none
    resp = session.get(url, timeout=5)
    print([b["title"] for b in resp.json()["items"]])
    url = resp.links.get("next", {}).get("url")
```

With the server running, `python client.py` prints:

```text
POST http://127.0.0.1:8000/books -> 201
  created {'id': 6, 'title': 'Kindred', 'author': 'Octavia E. Butler', 'year': 1979, 'isbn': None} at /books/6
GET http://127.0.0.1:8000/books/6 -> 200
PATCH http://127.0.0.1:8000/books/6 -> 200
  now {'id': 6, 'title': 'Kindred', 'author': 'Octavia E. Butler', 'year': 1980, 'isbn': None}
GET http://127.0.0.1:8000/books?limit=2 -> 200
  titles: ['Pride and Prejudice', 'Emma']
GET http://127.0.0.1:8000/books?offset=2&limit=2 -> 200
  titles: ['Dune', 'Neuromancer']
GET http://127.0.0.1:8000/books?offset=4&limit=2 -> 200
  titles: ['The Left Hand of Darkness', 'Kindred']
GET http://127.0.0.1:8000/books/9999 -> 404
  content type: application/problem+json
  problem: {'type': 'about:blank', 'title': 'Not Found', 'status': 404, 'detail': 'Book 9999 does not exist.', 'instance': '/books/9999'}
DELETE http://127.0.0.1:8000/books/6 -> 204
```

Three habits from this client apply to every API client you write:

- **Always set a timeout.** Without one, a request to a server that never answers waits forever. requests has no default timeout.
- **Check the status code** (`raise_for_status()` or an explicit check) before using the body.
- **Follow the links the server provides** instead of building URLs yourself.

## Summary

- Use **separate models** for input, partial updates, and output; **forbid unknown fields**; set **limits** on every field.
- Return **201 with Location** on create, **204** on delete; use `exclude_unset` for correct **PATCH** semantics.
- Report every error as **problem details** (RFC 9457), without leaking internals.
- **Validate** query parameters, enforce a **maximum page size**, and provide the next page in a **Link** header.
- Clients should set **timeouts**, check **status codes**, and **follow links**.

## Check your understanding

Choose the best answer for each question, then check your answers in [Answers to Chapter Questions](answers.md#chapter-6-building-a-rest-api).

**1. Why use separate models for create input, partial update and output?**

- A. To have more code
- B. Pydantic requires it
- C. To speed up JSON
- D. Each shape has different rules: clients never send id, updates are partial, output includes server fields

**2. What does extra="forbid" do on an input model?**

- A. Allows any fields
- B. Rejects requests that contain unknown fields
- C. Hides fields from output
- D. Makes all fields optional

**3. What should a successful create return?**

- A. 200 with no body
- B. 204 No Content
- C. 302 Found
- D. 201 Created with a Location header

**4. What should a successful DELETE return?**

- A. 204 No Content
- B. 200 with the deleted item, always
- C. 404
- D. 201

**5. Why use exclude_unset when applying a PATCH?**

- A. To speed up saving
- B. To remove the id
- C. So only fields the client actually sent are changed, not fields that defaulted to None
- D. To validate the body

**6. Which standard defines the problem details error format used in the book?**

- A. RFC 6749
- B. RFC 7519
- C. RFC 9457
- D. RFC 2616

**7. Where does the book's API put the URL of the next page?**

- A. In a cookie
- B. In a Link header
- C. In the request body
- D. Nowhere; clients compute it

**8. Which client practice does the chapter insist on?**

- A. Never check status codes
- B. Retry forever
- C. Always set a timeout
- D. Disable TLS verification
