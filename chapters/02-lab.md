# Chapter 2: The Lab

Every example in this book runs on your own computer. You need Python, a terminal, and a browser. This chapter installs the tools, explains what each one does, and builds a first working API in a dozen lines.

## The tools

<figure class="diagram">
<svg viewBox="0 0 720 260" style="width:100%;height:auto;max-width:720px" role="img" aria-label="The lab on your own computer: a terminal running curl and Python clients, a browser showing the interactive docs, and a FastAPI application served by uvicorn on 127.0.0.1 port 8000, all inside a Python virtual environment." xmlns="http://www.w3.org/2000/svg">
<style>
.a2a{ font-family:var(--sans),sans-serif; }
.a2a .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a2a .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a2a .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a2a .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a2a .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a2a .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a2a .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a2a .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a2a .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a2a .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a2a .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a2a .s{ fill:var(--text-dim); font-size:13px; }
.a2a .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a2a .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a2a .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a2a .c{ fill:var(--text-faint); font-size:12.5px; }
.a2a .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a2a .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a2a .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a2a .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a2a-a); }
.a2a .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a2a-a); marker-start:url(#a2a-s); }
.a2a .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a2a-g); }
.a2a .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a2a-a); }
.a2a .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a2a .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a2a .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a2a .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a2a .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a2a .ks-blue{ fill:#185FA5; font-size:13px; }
.a2a .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a2a .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a2a .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a2a .kb-blue, :root[data-theme="dark"] .a2a .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a2a .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a2a .kh-blue{ fill:#85B7EB; }
.a2a .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a2a-blue); }
.a2a .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a2a-blue); }
.a2a .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a2a .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a2a .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a2a .ks-teal{ fill:#0F6E56; font-size:13px; }
.a2a .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a2a .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a2a .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a2a .kb-teal, :root[data-theme="dark"] .a2a .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a2a .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a2a .kh-teal{ fill:#5DCAA5; }
.a2a .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a2a-teal); }
.a2a .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a2a-teal); }
.a2a .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a2a .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a2a .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a2a .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a2a .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a2a .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a2a .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a2a .kb-gray, :root[data-theme="dark"] .a2a .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a2a .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a2a .kh-gray{ fill:#B4B2A9; }
.a2a .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a2a-gray); }
.a2a .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a2a-gray); }
.a2a .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a2a-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a2a-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a2a-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a2a-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a2a-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a2a-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a2a">
<rect x="20" y="20" width="680" height="220" rx="10" class="zone"/>
<text x="40" y="44" text-anchor="start" class="c">your computer</text>
<rect x="40" y="70" width="190" height="60" rx="7" class="k-blue"/>
<text x="135.0" y="95.5" text-anchor="middle" class="kb-blue">terminal</text>
<text x="135.0" y="113.5" text-anchor="middle" class="ks-blue">curl, python client.py</text>
<rect x="40" y="154" width="190" height="60" rx="7" class="k-blue"/>
<text x="135.0" y="179.5" text-anchor="middle" class="kb-blue">browser</text>
<text x="135.0" y="197.5" text-anchor="middle" class="ks-blue">/docs (Swagger UI)</text>
<rect x="300" y="60" width="380" height="164" rx="8" class="tint"/>
<text x="490" y="82" text-anchor="middle" class="c">Python virtual environment (.venv)</text>
<rect x="320" y="100" width="150" height="60" rx="7" class="k-gray"/>
<text x="395.0" y="125.5" text-anchor="middle" class="kb-gray">uvicorn</text>
<text x="395.0" y="143.5" text-anchor="middle" class="km-gray">127.0.0.1:8000</text>
<rect x="510" y="100" width="150" height="60" rx="7" class="k-teal"/>
<text x="585.0" y="125.5" text-anchor="middle" class="kb-teal">FastAPI app</text>
<text x="585.0" y="143.5" text-anchor="middle" class="km-teal">library.py</text>
<line x1="232" y1="100" x2="318" y2="120" class="ar-blue"/>
<line x1="232" y1="184" x2="318" y2="144" class="ar-blue"/>
<line x1="472" y1="130" x2="508" y2="130" class="ar-gray"/>
<text x="490" y="200" text-anchor="middle" class="c">fastapi dev library.py starts both</text>
</g>
</svg>
<figcaption>Everything runs locally. The server listens on 127.0.0.1, so only your own machine can reach it.</figcaption>
</figure>

- **Python 3.12 or newer.** The examples use modern type hints.
- **FastAPI**, a Python framework for building APIs. You write ordinary functions with type hints, and FastAPI turns them into HTTP endpoints, validates input, and generates documentation.
- **uvicorn**, the server that actually listens on a network port and speaks HTTP. FastAPI applications follow the **ASGI** standard, and uvicorn is an ASGI server.
- **curl**, a command-line HTTP client. It shows you exactly what goes over the wire, which makes it the best tool for learning HTTP. It is preinstalled on Linux, macOS, and Windows 10 and later (in Git Bash, PowerShell, or Command Prompt).
- **requests**, the most popular Python HTTP client library, for writing API clients in code.
- **pytest**, for the automated tests that come with every example.

## Setting up

Download the book's code folder, then create a **virtual environment**, a private set of Python packages for this project, and install the dependencies:

```bash
cd code
python -m venv .venv
source .venv/bin/activate            # Windows Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt
```

Your prompt now starts with `(.venv)`. Run the tests once to check that everything works:

```bash
pytest -q
```

All tests should pass. The examples are pinned to FastAPI 0.163 and the other versions listed in `requirements.txt`, which were current when this book was written.

## Your first API

Here is `hello.py`, the complete program:

```python
from fastapi import FastAPI

app = FastAPI(title="Hello API")


@app.get("/")
def root():
    return {"message": "Hello, API"}


@app.get("/hello/{name}")
def greet(name: str, excited: bool = False):
    text = f"Hello, {name}"
    return {"greeting": text + ("!" if excited else ".")}
```

- `app = FastAPI()` creates the application.
- `@app.get("/hello/{name}")` says: when an HTTP `GET` request arrives for a path like `/hello/Ada`, call this function. `{name}` is a **path parameter**.
- `excited: bool = False` is not in the path, so FastAPI treats it as a **query parameter**: `/hello/Ada?excited=true`. The type hint means FastAPI converts the text `true` into a Python `True`, and rejects values it cannot convert.
- The function returns a dictionary; FastAPI converts it to JSON.

Start it in development mode, which restarts the server whenever you save a file:

```bash
fastapi dev hello.py
```

In a second terminal, call it:

```bash
curl http://127.0.0.1:8000/hello/Ada
{"greeting":"Hello, Ada."}

curl "http://127.0.0.1:8000/hello/Ada?excited=true"
{"greeting":"Hello, Ada!"}

curl "http://127.0.0.1:8000/hello/Ada?excited=maybe"
{"detail":[{"type":"bool_parsing","loc":["query","excited"],"msg":"Input should be a valid boolean, unable to interpret input","input":"maybe"}]}
```

The last call shows validation for free: `maybe` is not a boolean, so FastAPI answers with an error before your function runs. Put URLs with `?` or `&` in quotes, or your shell will try to interpret them.

## What happens to a request

<figure class="diagram">
<svg viewBox="0 0 720 220" style="width:100%;height:auto;max-width:720px" role="img" aria-label="What happens to a request inside the lab server: uvicorn receives the HTTP request, FastAPI matches the path to a Python function, Pydantic validates and converts the inputs, the function runs, and its return value is converted to a JSON response." xmlns="http://www.w3.org/2000/svg">
<style>
.a2b{ font-family:var(--sans),sans-serif; }
.a2b .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a2b .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a2b .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a2b .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a2b .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a2b .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a2b .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a2b .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a2b .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a2b .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a2b .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a2b .s{ fill:var(--text-dim); font-size:13px; }
.a2b .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a2b .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a2b .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a2b .c{ fill:var(--text-faint); font-size:12.5px; }
.a2b .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a2b .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a2b .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a2b .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a2b-a); }
.a2b .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a2b-a); marker-start:url(#a2b-s); }
.a2b .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a2b-g); }
.a2b .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a2b-a); }
.a2b .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a2b .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a2b .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a2b .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a2b .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a2b .ks-teal{ fill:#0F6E56; font-size:13px; }
.a2b .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a2b .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a2b .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a2b .kb-teal, :root[data-theme="dark"] .a2b .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a2b .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a2b .kh-teal{ fill:#5DCAA5; }
.a2b .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a2b-teal); }
.a2b .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a2b-teal); }
.a2b .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a2b .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a2b .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a2b .ks-amber{ fill:#854F0B; font-size:13px; }
.a2b .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a2b .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a2b .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a2b .kb-amber, :root[data-theme="dark"] .a2b .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a2b .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a2b .kh-amber{ fill:#EF9F27; }
.a2b .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a2b-amber); }
.a2b .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a2b-amber); }
.a2b .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a2b .k-coral{ fill:#FAECE7; stroke:#D85A30; stroke-width:1.6; }
.a2b .kb-coral{ fill:#712B13; font-size:13px; font-weight:700; }
.a2b .ks-coral{ fill:#993C1D; font-size:13px; }
.a2b .km-coral{ fill:#712B13; font-size:12.5px; font-family:var(--mono),monospace; }
.a2b .kh-coral{ fill:#993C1D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a2b .k-coral{ fill:#712B13; stroke:#F0997B; }
:root[data-theme="dark"] .a2b .kb-coral, :root[data-theme="dark"] .a2b .km-coral{ fill:#FAECE7; }
:root[data-theme="dark"] .a2b .ks-coral{ fill:#F5C4B3; }
:root[data-theme="dark"] .a2b .kh-coral{ fill:#F0997B; }
.a2b .ar-coral{ stroke:#D85A30; stroke-width:2; fill:none; marker-end:url(#a2b-coral); }
.a2b .ad-coral{ stroke:#D85A30; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a2b-coral); }
.a2b .ln-coral{ stroke:#D85A30; stroke-width:2; fill:none; }
.a2b .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a2b .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a2b .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a2b .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a2b .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a2b .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a2b .kb-gray, :root[data-theme="dark"] .a2b .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a2b .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a2b .kh-gray{ fill:#B4B2A9; }
.a2b .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a2b-gray); }
.a2b .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a2b-gray); }
.a2b .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a2b-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a2b-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a2b-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a2b-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a2b-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a2b-coral" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#D85A30"/></marker><marker id="a2b-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a2b">
<rect x="14" y="50" width="104" height="50" rx="7" class="k-amber"/>
<text x="66.0" y="79.5" text-anchor="middle" class="kb-amber">HTTP request</text>
<rect x="132" y="50" width="104" height="50" rx="7" class="k-gray"/>
<text x="184.0" y="79.5" text-anchor="middle" class="kb-gray">uvicorn</text>
<line x1="120" y1="75" x2="130" y2="75" class="ar"/>
<rect x="250" y="50" width="104" height="50" rx="7" class="k-teal"/>
<text x="302.0" y="79.5" text-anchor="middle" class="kb-teal">routing</text>
<line x1="238" y1="75" x2="248" y2="75" class="ar"/>
<rect x="368" y="50" width="104" height="50" rx="7" class="k-teal"/>
<text x="420.0" y="79.5" text-anchor="middle" class="kb-teal">validation</text>
<line x1="356" y1="75" x2="366" y2="75" class="ar"/>
<rect x="486" y="50" width="104" height="50" rx="7" class="k-teal"/>
<text x="538.0" y="79.5" text-anchor="middle" class="kb-teal">your function</text>
<line x1="474" y1="75" x2="484" y2="75" class="ar"/>
<rect x="604" y="50" width="104" height="50" rx="7" class="k-amber"/>
<text x="656.0" y="79.5" text-anchor="middle" class="kb-amber">JSON response</text>
<line x1="592" y1="75" x2="602" y2="75" class="ar"/>
<text x="150" y="132" text-anchor="middle" class="c">ASGI server</text>
<text x="368" y="132" text-anchor="middle" class="c">FastAPI: path, query, body</text>
<rect x="250" y="156" width="340" height="40" rx="7" class="k-coral"/>
<text x="420.0" y="180.5" text-anchor="middle" class="ks-coral">bad input never reaches your function: 422</text>
</g>
</svg>
<figcaption>FastAPI does the HTTP plumbing so the code you write is an ordinary Python function with typed parameters.</figcaption>
</figure>

1. **uvicorn** accepts the TCP connection and parses the HTTP request.
2. **FastAPI** matches the method and path against the routes you declared.
3. It **extracts and validates** parameters: path, query string, headers, and body, using your type hints.
4. It calls **your function** with the converted values.
5. It **serialises** the return value to JSON and builds the HTTP response.

If step 3 fails, the client receives a `422` error and your function never runs. That is a security benefit as much as a convenience: your code only ever sees well-formed input.

## Interactive documentation

Open **http://127.0.0.1:8000/docs** in a browser. FastAPI generated a page listing every endpoint, with a **Try it out** button that sends real requests. The page is built from an **OpenAPI** description of your API, available at `/openapi.json`. Chapter 7 is about OpenAPI; for now, the docs page is a convenient way to explore each example.

## The code folder

| File | Chapter | What it is |
|---|---|---|
| `hello.py` | 2 | The first API |
| `echo.py` | 3 | Shows requests from the server's side |
| `json_demo.py` | 4 | JSON in Python, and its pitfalls |
| `library.py`, `client.py` | 5 to 7 | The full Library API and a Python client |
| `library_auth.py` | 8 | API keys and JWT bearer tokens |
| `shop_insecure.py`, `shop_secure.py` | 9 | A vulnerable API and its fixed twin |
| `library_perf.py`, `retry_client.py` | 10 | Caching, rate limits, idempotency, async jobs |
| `library_ops.py` | 11 | Versions, deprecation, request IDs, logs |
| `graphql_app.py`, `grpc_demo/`, `webhooks.py`, `sse_app.py` | 12 | Beyond REST |
| `tests/` | all | Automated tests for every example |

Run any API with `fastapi dev <file>.py`. Only one can listen on port 8000 at a time; stop the previous one with Ctrl+C, or add `--port 8001`.

### Using Docker instead

If you prefer not to install Python packages locally, any example runs in the official Python image:

```bash
docker run --rm -it -p 8000:8000 -v "$PWD":/code -w /code python:3.13 \
  bash -c "pip install -r requirements.txt && fastapi run hello.py --host 0.0.0.0"
```

`fastapi run` is the production mode (no auto-reload); `--host 0.0.0.0` makes the server reachable from outside the container.

## Summary

- The lab uses **Python**, **FastAPI** (framework), **uvicorn** (server), **curl** and **requests** (clients), and **pytest** (tests).
- A FastAPI endpoint is a **decorated function**; type hints define **path** and **query parameters** and their validation.
- Invalid input is rejected with **422** before your code runs.
- `/docs` shows **interactive documentation** generated from the API's OpenAPI description.
