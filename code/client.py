"""Chapter 6: calling the Library API from Python with requests.

Start the server first:   fastapi dev library.py
Then run:                 python client.py
"""
import requests

BASE = "http://127.0.0.1:8000"
session = requests.Session()               # reuses the TCP connection between calls
session.headers["Accept"] = "application/json"


def show(resp: requests.Response) -> None:
    print(resp.request.method, resp.request.url, "->", resp.status_code)


# Create
resp = session.post(f"{BASE}/books", json={"title": "Kindred", "author": "Octavia E. Butler", "year": 1979},
                    timeout=5)
show(resp)
resp.raise_for_status()
location = resp.headers["Location"]
book = resp.json()
print("  created", book, "at", location)

# Read it back, using the Location header the server gave us
resp = session.get(BASE + location, timeout=5)
show(resp)

# Partial update
resp = session.patch(f"{BASE}/books/{book['id']}", json={"year": 1980}, timeout=5)
show(resp)
print("  now", resp.json())

# List with a filter, and follow the pagination links
url = f"{BASE}/books?limit=2"
while url:
    resp = session.get(url, timeout=5)
    show(resp)
    print("  titles:", [b["title"] for b in resp.json()["items"]])
    url = resp.links.get("next", {}).get("url")    # requests parses the Link header for us

# Errors come back as problem details
resp = session.get(f"{BASE}/books/9999", timeout=5)
show(resp)
print("  content type:", resp.headers["Content-Type"])
print("  problem:", resp.json())

# Delete
resp = session.delete(f"{BASE}/books/{book['id']}", timeout=5)
show(resp)
