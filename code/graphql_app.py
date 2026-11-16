"""Chapter 12: the library as a GraphQL API.

Run:   fastapi dev graphql_app.py
Open:  http://127.0.0.1:8000/graphql   (GraphiQL, an in-browser query editor)
Try:   curl -s http://127.0.0.1:8000/graphql -H "Content-Type: application/json" \
         -d '{"query": "{ books { title author { name } } }"}'
"""
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

AUTHORS = {1: "Jane Austen", 2: "Frank Herbert"}
BOOKS = [
    {"id": 1, "title": "Pride and Prejudice", "year": 1813, "author_id": 1},
    {"id": 2, "title": "Emma", "year": 1815, "author_id": 1},
    {"id": 3, "title": "Dune", "year": 1965, "author_id": 2},
]


@strawberry.type
class Author:
    id: int
    name: str

    @strawberry.field
    def books(self) -> list["Book"]:
        return [to_book(b) for b in BOOKS if b["author_id"] == self.id]


@strawberry.type
class Book:
    id: int
    title: str
    year: int | None
    author_id: strawberry.Private[int]

    @strawberry.field
    def author(self) -> Author:
        return Author(id=self.author_id, name=AUTHORS[self.author_id])


def to_book(b: dict) -> Book:
    return Book(id=b["id"], title=b["title"], year=b["year"], author_id=b["author_id"])


@strawberry.type
class Query:
    @strawberry.field
    def books(self, year_after: int | None = None) -> list[Book]:
        return [to_book(b) for b in BOOKS if year_after is None or (b["year"] or 0) > year_after]

    @strawberry.field
    def book(self, id: int) -> Book | None:
        return next((to_book(b) for b in BOOKS if b["id"] == id), None)

    @strawberry.field
    def authors(self) -> list[Author]:
        return [Author(id=i, name=n) for i, n in AUTHORS.items()]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, author_id: int, year: int | None = None) -> Book:
        if author_id not in AUTHORS:
            raise ValueError(f"No author {author_id}")
        new = {"id": len(BOOKS) + 1, "title": title, "year": year, "author_id": author_id}
        BOOKS.append(new)
        return to_book(new)


schema = strawberry.Schema(query=Query, mutation=Mutation)
app = FastAPI(title="Library GraphQL")
app.include_router(GraphQLRouter(schema), prefix="/graphql")
