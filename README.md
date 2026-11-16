# Concise Book on APIs

A concise, diagram-rich guide to web APIs, from HTTP and JSON to designing, building, documenting, securing, and operating REST APIs with Python and FastAPI, and on to GraphQL, gRPC, webhooks, and server-sent events.

**Read it online:** https://khaledmahmudkm.github.io/conciseapi/

## Code

The [`code/`](code/) folder holds every example in the book: small FastAPI applications, Python clients, and 30 pytest tests. See [`code/README.md`](code/README.md) to set it up and run it.

## How this repository works

* `chapters/` holds one Markdown file per chapter, with diagrams embedded as SVG, and `chapters.json` for the table of contents.
* `book.json` holds the title, author and palette (`clay`).
* `index.html` loads the shared reader, [bookengine](https://github.com/khaledmahmudkm/bookengine) 1.0.6, from jsDelivr. When opened from a local web server, it uses `../bookengine-git/` instead if that folder exists.

To preview locally, serve the parent folder (the one containing both `conciseapi-git` and `bookengine-git`):

```bash
python3 -m http.server 8000
# then open http://localhost:8000/conciseapi-git/
```

© 2026 Khaled Mahmud
