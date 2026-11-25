# Chapter 11: Evolving and Operating APIs

Publishing an API is a promise. Clients you have never met write code against it, and they cannot all upgrade the day you change something. This chapter covers how to change an API without breaking those clients, how to retire old versions politely, and how to run, observe, and test an API in production. The examples are in `library_ops.py`.

## Breaking and non-breaking changes

<figure class="diagram">
<svg viewBox="0 0 720 284" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Non-breaking changes that old clients tolerate: adding an endpoint, adding an optional request field, adding a response field, and adding an enum value only if clients were told to expect new ones. Breaking changes: removing or renaming a field, changing a type, making an optional field required, changing a URL, or changing error codes or behaviour." xmlns="http://www.w3.org/2000/svg">
<style>
.a11a{ font-family:var(--sans),sans-serif; }
.a11a .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a11a .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a11a .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a11a .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a11a .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a11a .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a11a .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a11a .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a11a .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a11a .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a11a .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a11a .s{ fill:var(--text-dim); font-size:13px; }
.a11a .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a11a .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a11a .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a11a .c{ fill:var(--text-faint); font-size:12.5px; }
.a11a .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a11a .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a11a .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a11a .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a11a-a); }
.a11a .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a11a-a); marker-start:url(#a11a-s); }
.a11a .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a11a-g); }
.a11a .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a11a-a); }
.a11a .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a11a .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a11a .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a11a .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a11a .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a11a .ks-green{ fill:#3B6D11; font-size:13px; }
.a11a .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a11a .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11a .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a11a .kb-green, :root[data-theme="dark"] .a11a .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a11a .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a11a .kh-green{ fill:#97C459; }
.a11a .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a11a-green); }
.a11a .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11a-green); }
.a11a .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a11a .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a11a .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a11a .ks-red{ fill:#A32D2D; font-size:13px; }
.a11a .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a11a .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11a .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a11a .kb-red, :root[data-theme="dark"] .a11a .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a11a .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a11a .kh-red{ fill:#F09595; }
.a11a .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a11a-red); }
.a11a .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11a-red); }
.a11a .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
</style>
<defs><marker id="a11a-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a11a-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a11a-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a11a-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a11a-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker></defs>
<g class="a11a">
<rect x="20" y="16" width="330" height="40" rx="7" class="k-green"/>
<text x="185.0" y="40.5" text-anchor="middle" class="kb-green">safe: additive</text>
<rect x="370" y="16" width="330" height="40" rx="7" class="k-red"/>
<text x="535.0" y="40.5" text-anchor="middle" class="kb-red">breaking</text>
<rect x="20" y="70" width="330" height="36" rx="5" class="pnl"/>
<text x="185.0" y="92.5" text-anchor="middle" class="s">add an endpoint</text>
<rect x="370" y="70" width="330" height="36" rx="5" class="pnl"/>
<text x="535.0" y="92.5" text-anchor="middle" class="s">remove or rename a field</text>
<rect x="20" y="114" width="330" height="36" rx="5" class="pnl"/>
<text x="185.0" y="136.5" text-anchor="middle" class="s">add an optional request field</text>
<rect x="370" y="114" width="330" height="36" rx="5" class="pnl"/>
<text x="535.0" y="136.5" text-anchor="middle" class="s">change a type: string to list</text>
<rect x="20" y="158" width="330" height="36" rx="5" class="pnl"/>
<text x="185.0" y="180.5" text-anchor="middle" class="s">add a response field</text>
<rect x="370" y="158" width="330" height="36" rx="5" class="pnl"/>
<text x="535.0" y="180.5" text-anchor="middle" class="s">make an optional field required</text>
<rect x="20" y="202" width="330" height="36" rx="5" class="pnl"/>
<text x="185.0" y="224.5" text-anchor="middle" class="s">add a new optional header</text>
<rect x="370" y="202" width="330" height="36" rx="5" class="pnl"/>
<text x="535.0" y="224.5" text-anchor="middle" class="s">change URLs, status codes, meaning</text>
<text x="360" y="270" text-anchor="middle" class="c">v1 to v2 in library_ops.py: "author": "X, Y" became "authors": ["X", "Y"], a breaking change</text>
</g>
</svg>
<figcaption>Additive changes need no new version, provided clients ignore fields they do not know. Teach your clients that rule.</figcaption>
</figure>

The key question for any change is whether an existing, correctly written client will still work. **Additive** changes are safe, as long as clients follow one rule: **ignore fields you do not recognise** (sometimes called the tolerant reader principle). Everything else is breaking and needs a new version or, better, a different design that stays additive. For example, instead of changing `author` from a string to a list, the API could have kept `author` and added a new `authors` field.

Watch for subtle breaks: changing the default page size or sort order, tightening validation, returning a different status code, or changing what an error means. To the client, behaviour is part of the contract too.

## Versioning

<figure class="diagram">
<svg viewBox="0 0 720 220" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Three places to put an API version: in the URL path such as /v2/books, which is visible and easy to route; in a custom request header such as API-Version: 2; or in the media type of the Accept header such as application/vnd.library.v2+json. A date-based version header is a variant used by some large APIs." xmlns="http://www.w3.org/2000/svg">
<style>
.a11b{ font-family:var(--sans),sans-serif; }
.a11b .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a11b .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a11b .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a11b .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a11b .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a11b .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a11b .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a11b .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a11b .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a11b .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a11b .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a11b .s{ fill:var(--text-dim); font-size:13px; }
.a11b .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a11b .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a11b .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a11b .c{ fill:var(--text-faint); font-size:12.5px; }
.a11b .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a11b .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a11b .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a11b .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a11b-a); }
.a11b .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a11b-a); marker-start:url(#a11b-s); }
.a11b .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a11b-g); }
.a11b .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a11b-a); }
.a11b .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a11b .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a11b .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a11b .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a11b .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a11b .ks-teal{ fill:#0F6E56; font-size:13px; }
.a11b .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a11b .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11b .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a11b .kb-teal, :root[data-theme="dark"] .a11b .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a11b .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a11b .kh-teal{ fill:#5DCAA5; }
.a11b .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a11b-teal); }
.a11b .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11b-teal); }
.a11b .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a11b .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a11b .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a11b .ks-amber{ fill:#854F0B; font-size:13px; }
.a11b .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a11b .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11b .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a11b .kb-amber, :root[data-theme="dark"] .a11b .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a11b .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a11b .kh-amber{ fill:#EF9F27; }
.a11b .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a11b-amber); }
.a11b .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11b-amber); }
.a11b .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a11b .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a11b .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a11b .ks-purple{ fill:#534AB7; font-size:13px; }
.a11b .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a11b .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11b .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a11b .kb-purple, :root[data-theme="dark"] .a11b .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a11b .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a11b .kh-purple{ fill:#AFA9EC; }
.a11b .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a11b-purple); }
.a11b .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11b-purple); }
.a11b .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
</style>
<defs><marker id="a11b-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a11b-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a11b-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a11b-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a11b-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a11b-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker></defs>
<g class="a11b">
<rect x="20" y="16" width="120" height="54" rx="7" class="k-teal"/>
<text x="80.0" y="47.5" text-anchor="middle" class="kb-teal">URL path</text>
<rect x="152" y="16" width="330" height="54" rx="6" class="pnl"/>
<text x="317.0" y="47.5" text-anchor="middle" class="m">GET /v2/books/1</text>
<text x="494" y="48" text-anchor="start" class="kh-teal">visible, easy to route</text>
<rect x="20" y="82" width="120" height="54" rx="7" class="k-amber"/>
<text x="80.0" y="113.5" text-anchor="middle" class="kb-amber">header</text>
<rect x="152" y="82" width="330" height="54" rx="6" class="pnl"/>
<text x="317.0" y="113.5" text-anchor="middle" class="m">API-Version: 2026-09-01</text>
<text x="494" y="114" text-anchor="start" class="kh-amber">clean URLs, easy to miss</text>
<rect x="20" y="148" width="120" height="54" rx="7" class="k-purple"/>
<text x="80.0" y="179.5" text-anchor="middle" class="kb-purple">media type</text>
<rect x="152" y="148" width="330" height="54" rx="6" class="pnl"/>
<text x="317.0" y="179.5" text-anchor="middle" class="m">Accept: application/vnd.library.v2+json</text>
<text x="494" y="180" text-anchor="start" class="kh-purple">purist, awkward to test</text>
</g>
</svg>
<figcaption>URL versioning is the most common and the one used in this book. Pick one scheme and use it everywhere.</figcaption>
</figure>

When a breaking change is unavoidable, publish a new **major version** alongside the old one. `library_ops.py` serves both, with FastAPI routers:

```python
v1 = APIRouter(prefix="/v1", tags=["v1 (deprecated)"], deprecated=True)

@v1.get("/books/{book_id}")
def get_book_v1(book_id: int, response: Response):
    b = find(book_id)
    response.headers["Deprecation"] = f"@{int(DEPRECATED_AT.timestamp())}"       # RFC 9745
    response.headers["Sunset"] = SUNSET_AT.strftime("%a, %d %b %Y %H:%M:%S GMT")  # RFC 8594
    response.headers["Link"] = f'</v2/books/{book_id}>; rel="successor-version"'
    return {"id": b["id"], "title": b["title"], "author": ", ".join(b["authors"]), "year": b["year"]}

v2 = APIRouter(prefix="/v2", tags=["v2"])

@v2.get("/books/{book_id}")
def get_book_v2(book_id: int):
    return find(book_id)
```

Both versions read the same data; only the representation differs. Keep the number of live versions small, because each one must be maintained, secured, and tested. Version only for breaking changes: `v2`, `v3`, not `v2.1.4`. The detailed version number belongs in the OpenAPI document's `info.version`.

## Deprecation and sunset

<figure class="diagram">
<svg viewBox="0 0 720 220" style="width:100%;height:auto;max-width:720px" role="img" aria-label="The lifecycle of an old version on a timeline: v2 is released; v1 is marked deprecated with a Deprecation header pointing to the date; clients migrate during a grace period while v1 responses carry Deprecation, Sunset and a successor link; at the sunset date v1 is removed and returns 410 Gone." xmlns="http://www.w3.org/2000/svg">
<style>
.a11c{ font-family:var(--sans),sans-serif; }
.a11c .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a11c .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a11c .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a11c .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a11c .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a11c .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a11c .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a11c .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a11c .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a11c .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a11c .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a11c .s{ fill:var(--text-dim); font-size:13px; }
.a11c .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a11c .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a11c .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a11c .c{ fill:var(--text-faint); font-size:12.5px; }
.a11c .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a11c .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a11c .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a11c .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a11c-a); }
.a11c .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a11c-a); marker-start:url(#a11c-s); }
.a11c .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a11c-g); }
.a11c .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a11c-a); }
.a11c .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a11c .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a11c .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a11c .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a11c .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a11c .ks-teal{ fill:#0F6E56; font-size:13px; }
.a11c .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a11c .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11c .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a11c .kb-teal, :root[data-theme="dark"] .a11c .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a11c .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a11c .kh-teal{ fill:#5DCAA5; }
.a11c .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a11c-teal); }
.a11c .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11c-teal); }
.a11c .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a11c .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a11c .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a11c .ks-amber{ fill:#854F0B; font-size:13px; }
.a11c .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a11c .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11c .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a11c .kb-amber, :root[data-theme="dark"] .a11c .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a11c .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a11c .kh-amber{ fill:#EF9F27; }
.a11c .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a11c-amber); }
.a11c .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11c-amber); }
.a11c .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a11c .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a11c .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a11c .ks-red{ fill:#A32D2D; font-size:13px; }
.a11c .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a11c .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11c .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a11c .kb-red, :root[data-theme="dark"] .a11c .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a11c .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a11c .kh-red{ fill:#F09595; }
.a11c .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a11c-red); }
.a11c .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11c-red); }
.a11c .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
</style>
<defs><marker id="a11c-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a11c-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a11c-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a11c-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a11c-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a11c-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker></defs>
<g class="a11c">
<line x1="40" y1="100" x2="680" y2="100" class="ar"/>
<circle cx="60" cy="100" r="9" class="k-teal"/>
<text x="60" y="76" text-anchor="middle" class="kh-teal">v2 released</text>
<circle cx="220" cy="100" r="9" class="k-amber"/>
<text x="220" y="76" text-anchor="middle" class="kh-amber">v1 deprecated</text>
<circle cx="560" cy="100" r="9" class="k-red"/>
<text x="560" y="76" text-anchor="middle" class="kh-red">v1 sunset</text>
<text x="220" y="128" text-anchor="middle" class="m">Deprecation: @1788220800</text>
<text x="560" y="128" text-anchor="middle" class="m">Sunset: 01 Mar 2027</text>
<rect x="230" y="150" width="320" height="30" rx="5" class="k-amber"/>
<text x="390" y="170" text-anchor="middle" class="kh-amber">grace period: clients migrate</text>
<text x="630" y="170" text-anchor="middle" class="kh-red">then 410 Gone</text>
</g>
</svg>
<figcaption>Announce, signal in every response, give people time, watch who still calls v1, then switch it off.</figcaption>
</figure>

Retiring a version is a process, not an event. Two standard headers let you signal it in every response, where client developers and their tools can see it:

- **Deprecation** (RFC 9745, 2025): the resource is deprecated, as of the given date, expressed as `@` followed by a Unix timestamp.
- **Sunset** (RFC 8594): the date after which it may stop working, as an HTTP date. It must not be earlier than the deprecation date.

A `Link` with `rel="successor-version"` points to the replacement. Run `fastapi dev library_ops.py`:

```bash
curl -i http://127.0.0.1:8000/v1/books/1
```

```text
HTTP/1.1 200 OK
content-type: application/json
deprecation: @1788220800
sunset: Mon, 01 Mar 2027 00:00:00 GMT
link: </v2/books/1>; rel="successor-version"
x-request-id: eb4afe57cfce41cb9bafad9e0a635199
server-timing: app;dur=2.6

{"id":1,"title":"Good Omens","author":"Terry Pratchett, Neil Gaiman","year":1990}
```

The timestamp 1788220800 is 1 September 2026. Version 2 returns `"authors": ["Terry Pratchett", "Neil Gaiman"]`. The OpenAPI document also marks every v1 operation `deprecated: true`, which Swagger UI shows struck through. Alongside the headers: announce the timeline, email the owners of API keys that still call v1, and watch the logs. After the sunset date, return **410 Gone** with a problem details body pointing to v2.

## API gateways

<figure class="diagram">
<svg viewBox="0 0 720 280" style="width:100%;height:auto;max-width:720px" role="img" aria-label="An API gateway sits between clients and backend services. It terminates TLS, authenticates requests, applies rate limits, routes by path and version, transforms and caches responses, and collects logs and metrics, so that each service does not have to." xmlns="http://www.w3.org/2000/svg">
<style>
.a11d{ font-family:var(--sans),sans-serif; }
.a11d .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a11d .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a11d .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a11d .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a11d .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a11d .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a11d .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a11d .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a11d .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a11d .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a11d .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a11d .s{ fill:var(--text-dim); font-size:13px; }
.a11d .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a11d .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a11d .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a11d .c{ fill:var(--text-faint); font-size:12.5px; }
.a11d .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a11d .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a11d .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a11d .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a11d-a); }
.a11d .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a11d-a); marker-start:url(#a11d-s); }
.a11d .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a11d-g); }
.a11d .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a11d-a); }
.a11d .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a11d .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a11d .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a11d .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a11d .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a11d .ks-blue{ fill:#185FA5; font-size:13px; }
.a11d .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a11d .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11d .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a11d .kb-blue, :root[data-theme="dark"] .a11d .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a11d .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a11d .kh-blue{ fill:#85B7EB; }
.a11d .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a11d-blue); }
.a11d .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11d-blue); }
.a11d .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a11d .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a11d .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a11d .ks-teal{ fill:#0F6E56; font-size:13px; }
.a11d .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a11d .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11d .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a11d .kb-teal, :root[data-theme="dark"] .a11d .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a11d .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a11d .kh-teal{ fill:#5DCAA5; }
.a11d .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a11d-teal); }
.a11d .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11d-teal); }
.a11d .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a11d .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a11d .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a11d .ks-amber{ fill:#854F0B; font-size:13px; }
.a11d .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a11d .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11d .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a11d .kb-amber, :root[data-theme="dark"] .a11d .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a11d .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a11d .kh-amber{ fill:#EF9F27; }
.a11d .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a11d-amber); }
.a11d .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11d-amber); }
.a11d .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a11d .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a11d .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a11d .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a11d .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a11d .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11d .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a11d .kb-gray, :root[data-theme="dark"] .a11d .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a11d .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a11d .kh-gray{ fill:#B4B2A9; }
.a11d .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a11d-gray); }
.a11d .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11d-gray); }
.a11d .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a11d-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a11d-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a11d-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a11d-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a11d-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a11d-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a11d-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a11d">
<rect x="20" y="30" width="120" height="50" rx="7" class="k-blue"/>
<text x="80.0" y="59.5" text-anchor="middle" class="kb-blue">web app</text>
<line x1="142" y1="55" x2="228" y2="140" class="ar"/>
<rect x="20" y="110" width="120" height="50" rx="7" class="k-blue"/>
<text x="80.0" y="139.5" text-anchor="middle" class="kb-blue">mobile app</text>
<line x1="142" y1="135" x2="228" y2="140" class="ar"/>
<rect x="20" y="190" width="120" height="50" rx="7" class="k-blue"/>
<text x="80.0" y="219.5" text-anchor="middle" class="kb-blue">partner</text>
<line x1="142" y1="215" x2="228" y2="140" class="ar"/>
<rect x="230" y="20" width="230" height="240" rx="10" class="k-amber"/>
<text x="345" y="46" text-anchor="middle" class="kh-amber">API gateway</text>
<rect x="250" y="60" width="190" height="26" rx="4" class="pnl"/>
<text x="345.0" y="77.5" text-anchor="middle" class="c">TLS termination</text>
<rect x="250" y="92" width="190" height="26" rx="4" class="pnl"/>
<text x="345.0" y="109.5" text-anchor="middle" class="c">authentication</text>
<rect x="250" y="124" width="190" height="26" rx="4" class="pnl"/>
<text x="345.0" y="141.5" text-anchor="middle" class="c">rate limits, quotas</text>
<rect x="250" y="156" width="190" height="26" rx="4" class="pnl"/>
<text x="345.0" y="173.5" text-anchor="middle" class="c">routing: /v1, /v2</text>
<rect x="250" y="188" width="190" height="26" rx="4" class="pnl"/>
<text x="345.0" y="205.5" text-anchor="middle" class="c">caching, transforms</text>
<rect x="250" y="220" width="190" height="26" rx="4" class="pnl"/>
<text x="345.0" y="237.5" text-anchor="middle" class="c">logs, metrics</text>
<rect x="540" y="30" width="160" height="50" rx="7" class="k-teal"/>
<text x="620.0" y="59.5" text-anchor="middle" class="kb-teal">books service v2</text>
<line x1="462" y1="140" x2="538" y2="55" class="ar"/>
<rect x="540" y="110" width="160" height="50" rx="7" class="k-gray"/>
<text x="620.0" y="139.5" text-anchor="middle" class="kb-gray">books service v1</text>
<line x1="462" y1="140" x2="538" y2="135" class="ar"/>
<rect x="540" y="190" width="160" height="50" rx="7" class="k-teal"/>
<text x="620.0" y="219.5" text-anchor="middle" class="kb-teal">orders service</text>
<line x1="462" y1="140" x2="538" y2="215" class="ar"/>
</g>
</svg>
<figcaption>Kong, NGINX, Envoy, Traefik and the cloud providers' API gateways all offer these functions.</figcaption>
</figure>

As the number of APIs and services grows, cross-cutting concerns move into an **API gateway**: a reverse proxy that every request passes through. It terminates TLS, validates tokens, enforces rate limits and quotas, routes `/v1` and `/v2` to different backends, and records metrics, so each service can focus on its own logic. Popular choices include Kong, NGINX, Envoy, Traefik, and the managed gateways of AWS, Azure, and Google Cloud. Many can import an OpenAPI document and reject requests that do not match it. An **inventory** of everything the gateway exposes also addresses OWASP API9: forgotten endpoints are where attackers look.

## Observability

When something goes wrong in production, you need to answer "what happened to this request?" quickly. Observability rests on three kinds of data:

- **Logs**: one structured record per event;
- **Metrics**: numbers over time, such as request rate, error rate, and latency percentiles;
- **Traces**: the path of one request through every service it touched.

<figure class="diagram">
<svg viewBox="0 0 720 270" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Observability with a request ID. The gateway assigns X-Request-ID demo-123; the books service and the database call both log it; the response returns it to the client. Logs, metrics and traces can then all be joined on that one ID." xmlns="http://www.w3.org/2000/svg">
<style>
.a11e{ font-family:var(--sans),sans-serif; }
.a11e .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a11e .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a11e .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a11e .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a11e .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a11e .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a11e .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a11e .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a11e .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a11e .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a11e .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a11e .s{ fill:var(--text-dim); font-size:13px; }
.a11e .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a11e .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a11e .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a11e .c{ fill:var(--text-faint); font-size:12.5px; }
.a11e .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a11e .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a11e .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a11e .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a11e-a); }
.a11e .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a11e-a); marker-start:url(#a11e-s); }
.a11e .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a11e-g); }
.a11e .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a11e-a); }
.a11e .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a11e .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a11e .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a11e .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a11e .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a11e .ks-blue{ fill:#185FA5; font-size:13px; }
.a11e .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a11e .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11e .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a11e .kb-blue, :root[data-theme="dark"] .a11e .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a11e .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a11e .kh-blue{ fill:#85B7EB; }
.a11e .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a11e-blue); }
.a11e .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11e-blue); }
.a11e .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a11e .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a11e .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a11e .ks-teal{ fill:#0F6E56; font-size:13px; }
.a11e .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a11e .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11e .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a11e .kb-teal, :root[data-theme="dark"] .a11e .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a11e .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a11e .kh-teal{ fill:#5DCAA5; }
.a11e .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a11e-teal); }
.a11e .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11e-teal); }
.a11e .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a11e .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a11e .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a11e .ks-amber{ fill:#854F0B; font-size:13px; }
.a11e .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a11e .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11e .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a11e .kb-amber, :root[data-theme="dark"] .a11e .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a11e .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a11e .kh-amber{ fill:#EF9F27; }
.a11e .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a11e-amber); }
.a11e .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11e-amber); }
.a11e .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a11e .k-coral{ fill:#FAECE7; stroke:#D85A30; stroke-width:1.6; }
.a11e .kb-coral{ fill:#712B13; font-size:13px; font-weight:700; }
.a11e .ks-coral{ fill:#993C1D; font-size:13px; }
.a11e .km-coral{ fill:#712B13; font-size:12.5px; font-family:var(--mono),monospace; }
.a11e .kh-coral{ fill:#993C1D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11e .k-coral{ fill:#712B13; stroke:#F0997B; }
:root[data-theme="dark"] .a11e .kb-coral, :root[data-theme="dark"] .a11e .km-coral{ fill:#FAECE7; }
:root[data-theme="dark"] .a11e .ks-coral{ fill:#F5C4B3; }
:root[data-theme="dark"] .a11e .kh-coral{ fill:#F0997B; }
.a11e .ar-coral{ stroke:#D85A30; stroke-width:2; fill:none; marker-end:url(#a11e-coral); }
.a11e .ad-coral{ stroke:#D85A30; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11e-coral); }
.a11e .ln-coral{ stroke:#D85A30; stroke-width:2; fill:none; }
.a11e .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a11e .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a11e .ks-purple{ fill:#534AB7; font-size:13px; }
.a11e .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a11e .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11e .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a11e .kb-purple, :root[data-theme="dark"] .a11e .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a11e .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a11e .kh-purple{ fill:#AFA9EC; }
.a11e .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a11e-purple); }
.a11e .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11e-purple); }
.a11e .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
</style>
<defs><marker id="a11e-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a11e-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a11e-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a11e-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a11e-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a11e-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a11e-coral" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#D85A30"/></marker><marker id="a11e-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker></defs>
<g class="a11e">
<rect x="20" y="30" width="152" height="50" rx="7" class="k-blue"/>
<text x="96.0" y="59.5" text-anchor="middle" class="kb-blue">client</text>
<rect x="196" y="30" width="152" height="50" rx="7" class="k-amber"/>
<text x="272.0" y="59.5" text-anchor="middle" class="kb-amber">gateway</text>
<line x1="174" y1="55" x2="194" y2="55" class="ar"/>
<rect x="372" y="30" width="152" height="50" rx="7" class="k-teal"/>
<text x="448.0" y="59.5" text-anchor="middle" class="kb-teal">books service</text>
<line x1="350" y1="55" x2="370" y2="55" class="ar"/>
<rect x="548" y="30" width="152" height="50" rx="7" class="k-purple"/>
<text x="624.0" y="59.5" text-anchor="middle" class="kb-purple">database</text>
<line x1="526" y1="55" x2="546" y2="55" class="ar"/>
<text x="360" y="104" text-anchor="middle" class="kh-amber">X-Request-ID: demo-123 travels with the request and comes back in the response</text>
<rect x="20" y="130" width="216" height="60" rx="7" class="k-teal"/>
<text x="128.0" y="155.5" text-anchor="middle" class="kb-teal">logs</text>
<text x="128.0" y="173.5" text-anchor="middle" class="ks-teal">JSON lines with request_id</text>
<rect x="252" y="130" width="216" height="60" rx="7" class="k-coral"/>
<text x="360.0" y="155.5" text-anchor="middle" class="kb-coral">metrics</text>
<text x="360.0" y="173.5" text-anchor="middle" class="ks-coral">rate, errors, p95 latency</text>
<rect x="484" y="130" width="216" height="60" rx="7" class="k-purple"/>
<text x="592.0" y="155.5" text-anchor="middle" class="kb-purple">traces</text>
<text x="592.0" y="173.5" text-anchor="middle" class="ks-purple">one span per hop, same trace id</text>
<rect x="20" y="210" width="680" height="44" rx="7" class="pnl"/>
<text x="360.0" y="236.5" text-anchor="middle" class="s">OpenTelemetry standardises all three; W3C traceparent carries the trace across services</text>
</g>
</svg>
<figcaption>When a user reports a failure, the request ID in their error message leads straight to the right log lines.</figcaption>
</figure>

The thread connecting them is a **request ID**. `library_ops.py` adds one in middleware, reusing the client's `X-Request-ID` if it sent one, returning it in the response, and including it in a JSON log line:

```python
@app.middleware("http")
async def observe(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    start = time.perf_counter()
    response = await call_next(request)
    ms = (time.perf_counter() - start) * 1000
    response.headers["X-Request-ID"] = request_id          # the client can quote it in a support ticket
    response.headers["Server-Timing"] = f"app;dur={ms:.1f}"
    log.info(json.dumps({"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                         "request_id": request_id, "method": request.method,
                         "path": request.url.path, "status": response.status_code,
                         "duration_ms": round(ms, 1)}))
    return response
```

```bash
curl -i http://127.0.0.1:8000/v2/books/1 -H "X-Request-ID: demo-123"
```

The server's log shows:

```text
{"ts": "2026-11-15T06:53:04+00:00", "request_id": "demo-123", "method": "GET", "path": "/v2/books/1", "status": 200, "duration_ms": 1.2}
```

JSON logs can be searched and aggregated by tools such as the Elastic stack, Grafana Loki, or a cloud logging service. **Never log secrets**: no passwords, tokens, API keys, or full card numbers. **OpenTelemetry** is the vendor-neutral standard for collecting logs, metrics, and traces; its instrumentation for FastAPI and requests propagates a W3C `traceparent` header between services automatically. Finally, provide a cheap **health endpoint** (`GET /health`) for load balancers and orchestrators such as Kubernetes to probe.

## Testing APIs

<figure class="diagram">
<svg viewBox="0 0 720 270" style="width:100%;height:auto;max-width:720px" role="img" aria-label="A testing pyramid for APIs: many fast unit tests of functions and models at the bottom; API tests that call endpoints in process with TestClient in the middle; contract tests against the OpenAPI document; and a few end-to-end tests against a deployed environment at the top." xmlns="http://www.w3.org/2000/svg">
<style>
.a11f{ font-family:var(--sans),sans-serif; }
.a11f .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a11f .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a11f .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a11f .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a11f .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a11f .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a11f .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a11f .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a11f .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a11f .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a11f .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a11f .s{ fill:var(--text-dim); font-size:13px; }
.a11f .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a11f .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a11f .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a11f .c{ fill:var(--text-faint); font-size:12.5px; }
.a11f .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a11f .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a11f .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a11f .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a11f-a); }
.a11f .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a11f-a); marker-start:url(#a11f-s); }
.a11f .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a11f-g); }
.a11f .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a11f-a); }
.a11f .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a11f .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a11f .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a11f .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a11f .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a11f .ks-teal{ fill:#0F6E56; font-size:13px; }
.a11f .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a11f .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11f .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a11f .kb-teal, :root[data-theme="dark"] .a11f .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a11f .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a11f .kh-teal{ fill:#5DCAA5; }
.a11f .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a11f-teal); }
.a11f .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11f-teal); }
.a11f .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a11f .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a11f .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a11f .ks-purple{ fill:#534AB7; font-size:13px; }
.a11f .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a11f .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11f .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a11f .kb-purple, :root[data-theme="dark"] .a11f .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a11f .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a11f .kh-purple{ fill:#AFA9EC; }
.a11f .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a11f-purple); }
.a11f .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11f-purple); }
.a11f .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a11f .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a11f .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a11f .ks-green{ fill:#3B6D11; font-size:13px; }
.a11f .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a11f .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11f .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a11f .kb-green, :root[data-theme="dark"] .a11f .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a11f .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a11f .kh-green{ fill:#97C459; }
.a11f .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a11f-green); }
.a11f .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11f-green); }
.a11f .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a11f .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a11f .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a11f .ks-red{ fill:#A32D2D; font-size:13px; }
.a11f .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a11f .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a11f .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a11f .kb-red, :root[data-theme="dark"] .a11f .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a11f .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a11f .kh-red{ fill:#F09595; }
.a11f .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a11f-red); }
.a11f .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a11f-red); }
.a11f .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
</style>
<defs><marker id="a11f-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a11f-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a11f-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a11f-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a11f-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a11f-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a11f-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker></defs>
<g class="a11f">
<rect x="260.0" y="20" width="200" height="48" rx="7" class="k-red"/>
<text x="360.0" y="48.5" text-anchor="middle" class="kb-red">end-to-end: few</text>
<rect x="200.0" y="78" width="320" height="48" rx="7" class="k-purple"/>
<text x="360.0" y="106.5" text-anchor="middle" class="kb-purple">contract: responses match OpenAPI</text>
<rect x="130.0" y="136" width="460" height="48" rx="7" class="k-teal"/>
<text x="360.0" y="164.5" text-anchor="middle" class="kb-teal">API tests: TestClient, every endpoint</text>
<rect x="60.0" y="194" width="600" height="48" rx="7" class="k-green"/>
<text x="360.0" y="222.5" text-anchor="middle" class="kb-green">unit: models, functions, many</text>
</g>
</svg>
<figcaption>The labs' 30 tests sit in the middle layer: each one calls the API through FastAPI's TestClient, in milliseconds.</figcaption>
</figure>

FastAPI's `TestClient` calls the application directly, without a network or a running server, so API tests are fast enough to run on every change. From `tests/test_perf_ops.py`:

```python
def test_versions_and_deprecation():
    o = TestClient(ops.app)
    v1 = o.get("/v1/books/1")
    assert v1.json()["author"] == "Terry Pratchett, Neil Gaiman"
    assert v1.headers["Deprecation"].startswith("@") and v1.headers["Sunset"].endswith("GMT")
    assert 'rel="successor-version"' in v1.headers["Link"]
    v2 = o.get("/v2/books/1", headers={"X-Request-ID": "trace-42"})
    assert v2.json()["authors"] == ["Terry Pratchett", "Neil Gaiman"]
    assert v2.headers["X-Request-ID"] == "trace-42" and "Deprecation" not in v2.headers
```

The code folder has 30 such tests covering every chapter. Run them all:

```bash
cd code
pytest -q
```

```text
..............................                                           [100%]
30 passed in 5.28s
```

Beyond these, **contract tests** (Schemathesis, from Chapter 7) check every response against the OpenAPI document, **security tests** (Chapter 9) prove each authorization rule, and **load tests** with tools such as Locust or k6 show how the API behaves under realistic traffic. Run them all automatically in continuous integration, so a breaking change fails a build instead of a client.

## Summary

- **Additive** changes are safe if clients **ignore unknown fields**; anything else is **breaking**.
- Version only for breaking changes, most commonly in the **URL path**; keep few versions alive.
- Signal retirement with **Deprecation** (RFC 9745), **Sunset** (RFC 8594), and a **successor-version** link; then return **410 Gone**.
- **Gateways** centralise TLS, authentication, rate limits, routing, and inventory.
- **Request IDs** tie together **logs, metrics, and traces**; use structured logs and **OpenTelemetry**; never log secrets.
- Test at every level, and automate it.

## Check your understanding

Choose the best answer for each question, then check your answers in [Answers to Chapter Questions](answers.md#chapter-11-evolving-and-operating-apis).

**1. Which change is usually non-breaking?**

- A. Adding a new optional field to a response
- B. Renaming a field
- C. Removing an endpoint
- D. Changing a field's type

**2. Where do most APIs put the version?**

- A. In the request body
- B. In a cookie
- C. In the URL path, such as /v2/
- D. In the domain's TLS certificate

**3. Which header announces when an endpoint will stop working?**

- A. Deprecation
- B. Retry-After
- C. Expires
- D. Sunset

**4. What should a retired endpoint return?**

- A. 404 Not Found
- B. 410 Gone
- C. 301 always
- D. 500

**5. Which is a typical job of an API gateway?**

- A. Running the database
- B. Writing business logic
- C. Centralising TLS, authentication, rate limits, routing and inventory
- D. Compiling code

**6. What ties together the logs, metrics and traces of one request across services?**

- A. A request ID
- B. The client's IP address
- C. The timestamp
- D. The HTTP method

**7. What must never appear in logs?**

- A. Secrets, such as tokens and passwords
- B. Request IDs
- C. Status codes
- D. Latencies

**8. What is OpenTelemetry?**

- A. A rate limiter
- B. An API gateway
- C. A vendor-neutral standard and toolkit for traces, metrics and logs
- D. A test framework
