"""Chapter 4: JSON in Python, and where it surprises people.

Run:   python json_demo.py
"""
import json
from datetime import datetime, timezone

from pydantic import BaseModel, Field

# 1. Python objects to JSON text and back
book = {"id": 1, "title": "Dune", "tags": ["sf", "classic"], "in_stock": True, "rating": None}
text = json.dumps(book)
print("serialized:", text)
print("parsed back:", json.loads(text))

# 2. JSON has no date type: you must choose a string format (ISO 8601 is the norm)
try:
    json.dumps({"when": datetime.now(timezone.utc)})
except TypeError as e:
    print("datetime fails:", e)
print("ISO 8601 works:", json.dumps({"when": datetime(2026, 11, 15, 9, 30, tzinfo=timezone.utc).isoformat()}))

# 3. Large integers lose precision in JavaScript clients; send big IDs as strings
big = 2**53 + 1
print("big int as number:", json.dumps({"id": big}), " as string:", json.dumps({"id": str(big)}))


# 4. A schema describes valid JSON; Pydantic generates JSON Schema for you
class Book(BaseModel):
    id: int
    title: str = Field(min_length=1, max_length=200)
    year: int | None = Field(default=None, ge=0, le=2100)
    tags: list[str] = []


print("JSON Schema:", json.dumps(Book.model_json_schema(), indent=2))
print("validated:", Book.model_validate_json('{"id": 7, "title": "Emma", "year": 1815}'))
try:
    Book.model_validate_json('{"id": "seven", "title": ""}')
except Exception as e:
    print("invalid:", e.errors()[0]["loc"], e.errors()[0]["msg"])
