"""Chapters 5 to 7: a complete REST API for a small library.

Run:   fastapi dev library.py
Docs:  http://127.0.0.1:8000/docs  (Swagger UI)   http://127.0.0.1:8000/openapi.json
Try:   curl -i http://127.0.0.1:8000/books?author=Austen
"""
from fastapi import FastAPI, HTTPException, Query, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(
    title="Library API",
    version="1.0.0",
    description="A small REST API used throughout the Concise Book on APIs.",
    openapi_tags=[{"name": "books", "description": "Create, read, update and delete books."}],
)


# ---------------------------------------------------------------- models
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
    author: str | None = Field(default=None, min_length=1, max_length=100)
    year: int | None = Field(default=None, ge=0, le=2100)
    isbn: str | None = Field(default=None, pattern=r"^\d{13}$")


class Book(BaseModel):
    """What the server returns: a server-assigned id plus the book's fields."""
    id: int
    title: str
    author: str
    year: int | None = None
    isbn: str | None = None


class BookPage(BaseModel):
    items: list[Book]
    total: int
    limit: int
    offset: int


# ---------------------------------------------------------------- storage
SEED = [
    ("Pride and Prejudice", "Jane Austen", 1813, "9780141439518"),
    ("Emma", "Jane Austen", 1815, None),
    ("Dune", "Frank Herbert", 1965, "9780441013593"),
    ("Neuromancer", "William Gibson", 1984, None),
    ("The Left Hand of Darkness", "Ursula K. Le Guin", 1969, None),
]
books: dict[int, Book] = {}
next_id = 1


def reset() -> None:
    """Restore the seed data (used by the tests)."""
    global next_id
    books.clear()
    next_id = 1
    for title, author, year, isbn in SEED:
        add(BookIn(title=title, author=author, year=year, isbn=isbn))


def add(data: BookIn) -> Book:
    global next_id
    book = Book(id=next_id, **data.model_dump())
    books[next_id] = book
    next_id += 1
    return book


reset()


# ---------------------------------------------------------------- errors as RFC 9457 problem details
def problem(status_code: int, title: str, detail: str, request: Request, **extra) -> JSONResponse:
    body = {"type": "about:blank", "title": title, "status": status_code,
            "detail": detail, "instance": request.url.path, **extra}
    return JSONResponse(body, status_code=status_code, media_type="application/problem+json")


@app.exception_handler(StarletteHTTPException)
async def http_error(request: Request, exc: StarletteHTTPException):
    titles = {404: "Not Found", 405: "Method Not Allowed", 409: "Conflict"}
    return problem(exc.status_code, titles.get(exc.status_code, "Error"), str(exc.detail), request)


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    errors = [{"field": ".".join(str(p) for p in e["loc"][1:]), "message": e["msg"]} for e in exc.errors()]
    return problem(422, "Validation failed", "The request body or parameters are invalid.", request,
                   errors=errors)


def get_or_404(book_id: int) -> Book:
    if book_id not in books:
        raise HTTPException(status_code=404, detail=f"Book {book_id} does not exist.")
    return books[book_id]


# ---------------------------------------------------------------- endpoints
@app.get("/books", response_model=BookPage, tags=["books"], summary="List books")
def list_books(
    request: Request,
    response: Response,
    author: str | None = Query(default=None, description="Filter: author contains this text"),
    year: int | None = Query(default=None, description="Filter: exact publication year"),
    sort: str = Query(default="id", pattern=r"^-?(id|title|year)$", description="Sort field; prefix - for descending"),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    items = list(books.values())
    if author:
        items = [b for b in items if author.lower() in b.author.lower()]
    if year is not None:
        items = [b for b in items if b.year == year]
    field = sort.lstrip("-")

    def sort_key(book: Book):
        value = getattr(book, field)
        return (value is None, value if value is not None else 0)   # books without a year sort last

    items.sort(key=sort_key, reverse=sort.startswith("-"))
    page = items[offset: offset + limit]
    if offset + limit < len(items):          # tell the client where the next page is
        nxt = request.url.include_query_params(offset=offset + limit, limit=limit)
        response.headers["Link"] = f'<{nxt}>; rel="next"'
    return BookPage(items=page, total=len(items), limit=limit, offset=offset)


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


@app.put("/books/{book_id}", response_model=Book, tags=["books"], summary="Replace a book")
def replace_book(book_id: int, data: BookIn):
    get_or_404(book_id)
    books[book_id] = Book(id=book_id, **data.model_dump())
    return books[book_id]


@app.patch("/books/{book_id}", response_model=Book, tags=["books"], summary="Update some fields")
def update_book(book_id: int, changes: BookPatch):
    book = get_or_404(book_id)
    updated = book.model_copy(update=changes.model_dump(exclude_unset=True))
    books[book_id] = Book.model_validate(updated.model_dump())
    return books[book_id]


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["books"],
            summary="Delete a book")
def delete_book(book_id: int):
    get_or_404(book_id)
    del books[book_id]
