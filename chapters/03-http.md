# Chapter 3: HTTP for APIs

Almost every web API is built on **HTTP**, the Hypertext Transfer Protocol. It was designed for web pages, but its simple model of requests, responses, methods, and status codes turned out to fit APIs remarkably well. You cannot design or debug an API well without understanding HTTP, so this chapter takes it apart.

## Requests and responses

HTTP is a **request and response** protocol. The client sends a request; the server sends back exactly one response. In HTTP/1.1 both are plain text.

<figure class="diagram">
<svg viewBox="0 0 720 320" style="width:100%;height:auto;max-width:720px" role="img" aria-label="An HTTP request and its response as text. The request has a request line with method, path and version, header lines, a blank line, and an optional body. The response has a status line with version, status code and reason, header lines, a blank line, and the body." xmlns="http://www.w3.org/2000/svg">
<style>
.a3a{ font-family:var(--sans),sans-serif; }
.a3a .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a3a .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a3a .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a3a .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a3a .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a3a .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a3a .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a3a .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a3a .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a3a .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a3a .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a3a .s{ fill:var(--text-dim); font-size:13px; }
.a3a .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a3a .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a3a .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a3a .c{ fill:var(--text-faint); font-size:12.5px; }
.a3a .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a3a .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a3a .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a3a .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a3a-a); }
.a3a .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a3a-a); marker-start:url(#a3a-s); }
.a3a .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a3a-g); }
.a3a .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a3a-a); }
.a3a .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a3a .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a3a .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a3a .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a3a .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a3a .ks-blue{ fill:#185FA5; font-size:13px; }
.a3a .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a3a .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3a .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a3a .kb-blue, :root[data-theme="dark"] .a3a .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a3a .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a3a .kh-blue{ fill:#85B7EB; }
.a3a .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a3a-blue); }
.a3a .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3a-blue); }
.a3a .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a3a .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a3a .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a3a .ks-teal{ fill:#0F6E56; font-size:13px; }
.a3a .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a3a .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3a .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a3a .kb-teal, :root[data-theme="dark"] .a3a .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a3a .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a3a .kh-teal{ fill:#5DCAA5; }
.a3a .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a3a-teal); }
.a3a .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3a-teal); }
.a3a .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
</style>
<defs><marker id="a3a-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a3a-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a3a-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a3a-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a3a-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker></defs>
<g class="a3a">
<text x="20" y="26" text-anchor="start" class="kh-blue">request (client to server)</text>
<rect x="20" y="36" width="330" height="270" rx="8" class="k-blue"/>
<text x="34" y="64" text-anchor="start" class="kb-blue">POST /books HTTP/1.1</text>
<text x="34" y="90" text-anchor="start" class="km-blue">Host: 127.0.0.1:8000</text>
<text x="34" y="116" text-anchor="start" class="km-blue">Content-Type: application/json</text>
<text x="34" y="142" text-anchor="start" class="km-blue">Accept: application/json</text>
<text x="34" y="168" text-anchor="start" class="km-blue">Content-Length: 41</text>
<text x="34" y="194" text-anchor="start" class="km-blue"></text>
<text x="34" y="220" text-anchor="start" class="km-blue">{"title": "Emma",</text>
<text x="41.5" y="246" text-anchor="start" class="km-blue">"author": "Jane Austen"}</text>
<text x="370" y="26" text-anchor="start" class="kh-teal">response (server to client)</text>
<rect x="370" y="36" width="330" height="270" rx="8" class="k-teal"/>
<text x="384" y="64" text-anchor="start" class="kb-teal">HTTP/1.1 201 Created</text>
<text x="384" y="90" text-anchor="start" class="km-teal">Content-Type: application/json</text>
<text x="384" y="116" text-anchor="start" class="km-teal">Location: /books/6</text>
<text x="384" y="142" text-anchor="start" class="km-teal">Content-Length: 62</text>
<text x="384" y="168" text-anchor="start" class="km-teal"></text>
<text x="384" y="194" text-anchor="start" class="km-teal">{"id": 6, "title": "Emma",</text>
<text x="391.5" y="220" text-anchor="start" class="km-teal">"author": "Jane Austen"}</text>
<text x="330" y="194" text-anchor="end" class="c">blank line</text>
<text x="680" y="168" text-anchor="end" class="c">blank line</text>
</g>
</svg>
<figcaption>HTTP/1.1 messages are plain text: a start line, headers, a blank line, then the body. HTTP/2 and HTTP/3 encode the same parts in binary.</figcaption>
</figure>

A **request** has four parts:

1. The **request line**: a **method** (`POST`), a **path** (`/books`), and the protocol version.
2. **Headers**: `Name: value` lines with metadata. `Host` says which site the request is for; `Content-Type` describes the body; `Accept` says what the client wants back.
3. A **blank line**, which ends the headers.
4. An optional **body**: the data being sent.

A **response** has the same shape, except that the first line is a **status line** with a three-digit **status code** (`201`) and a reason phrase (`Created`).

See it for yourself with `curl -v` (verbose), which prints the request lines with `>` and the response lines with `<`. Start the echo server (`fastapi dev echo.py`) and send a request:

```bash
curl -v -X POST http://127.0.0.1:8000/echo -H "Content-Type: application/json" -d '{"a": 1}'
```

```text
> POST /echo HTTP/1.1
> Host: 127.0.0.1:8000
> User-Agent: curl/8.5.0
> Accept: */*
> Content-Type: application/json
> Content-Length: 8
>
< HTTP/1.1 200 OK
< date: Sun, 15 Nov 2026 06:42:29 GMT
< server: uvicorn
< content-length: 195
< content-type: application/json
<
{"method":"POST","path":"/echo","query":{},"headers":{"host":"127.0.0.1:8000","user-agent":"curl/8.5.0",
"accept":"*/*","content-type":"application/json","content-length":"8"},"body":"{\"a\": 1}"}
```

The echo server returns the request exactly as it saw it, which is a good way to understand what your client really sends.

## URLs

<figure class="diagram">
<svg viewBox="0 0 720 190" style="width:100%;height:auto;max-width:720px" role="img" aria-label="The parts of a URL: scheme https, host api.library.example, port 443, path /v1/books/42, query string ?fields=title&amp;lang=en, and fragment #reviews, which is never sent to the server." xmlns="http://www.w3.org/2000/svg">
<style>
.a3b{ font-family:var(--sans),sans-serif; }
.a3b .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a3b .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a3b .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a3b .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a3b .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a3b .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a3b .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a3b .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a3b .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a3b .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a3b .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a3b .s{ fill:var(--text-dim); font-size:13px; }
.a3b .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a3b .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a3b .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a3b .c{ fill:var(--text-faint); font-size:12.5px; }
.a3b .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a3b .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a3b .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a3b .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a3b-a); }
.a3b .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a3b-a); marker-start:url(#a3b-s); }
.a3b .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a3b-g); }
.a3b .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a3b-a); }
.a3b .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a3b .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a3b .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a3b .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a3b .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a3b .ks-blue{ fill:#185FA5; font-size:13px; }
.a3b .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a3b .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3b .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a3b .kb-blue, :root[data-theme="dark"] .a3b .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a3b .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a3b .kh-blue{ fill:#85B7EB; }
.a3b .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a3b-blue); }
.a3b .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3b-blue); }
.a3b .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a3b .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a3b .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a3b .ks-teal{ fill:#0F6E56; font-size:13px; }
.a3b .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a3b .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3b .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a3b .kb-teal, :root[data-theme="dark"] .a3b .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a3b .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a3b .kh-teal{ fill:#5DCAA5; }
.a3b .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a3b-teal); }
.a3b .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3b-teal); }
.a3b .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a3b .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a3b .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a3b .ks-amber{ fill:#854F0B; font-size:13px; }
.a3b .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a3b .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3b .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a3b .kb-amber, :root[data-theme="dark"] .a3b .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a3b .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a3b .kh-amber{ fill:#EF9F27; }
.a3b .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a3b-amber); }
.a3b .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3b-amber); }
.a3b .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a3b .k-pink{ fill:#FBEAF0; stroke:#D4537E; stroke-width:1.6; }
.a3b .kb-pink{ fill:#72243E; font-size:13px; font-weight:700; }
.a3b .ks-pink{ fill:#993556; font-size:13px; }
.a3b .km-pink{ fill:#72243E; font-size:12.5px; font-family:var(--mono),monospace; }
.a3b .kh-pink{ fill:#993556; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3b .k-pink{ fill:#72243E; stroke:#ED93B1; }
:root[data-theme="dark"] .a3b .kb-pink, :root[data-theme="dark"] .a3b .km-pink{ fill:#FBEAF0; }
:root[data-theme="dark"] .a3b .ks-pink{ fill:#F4C0D1; }
:root[data-theme="dark"] .a3b .kh-pink{ fill:#ED93B1; }
.a3b .ar-pink{ stroke:#D4537E; stroke-width:2; fill:none; marker-end:url(#a3b-pink); }
.a3b .ad-pink{ stroke:#D4537E; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3b-pink); }
.a3b .ln-pink{ stroke:#D4537E; stroke-width:2; fill:none; }
.a3b .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a3b .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a3b .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a3b .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a3b .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3b .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a3b .kb-gray, :root[data-theme="dark"] .a3b .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a3b .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a3b .kh-gray{ fill:#B4B2A9; }
.a3b .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a3b-gray); }
.a3b .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3b-gray); }
.a3b .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a3b-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a3b-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a3b-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a3b-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a3b-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a3b-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a3b-pink" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#D4537E"/></marker><marker id="a3b-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a3b">
<rect x="20" y="50" width="90" height="40" rx="4" class="k-gray"/>
<text x="65.0" y="74.5" text-anchor="middle" class="km-gray">https://</text>
<text x="65.0" y="116" text-anchor="middle" class="s">scheme</text>
<rect x="110" y="50" width="180" height="40" rx="4" class="k-blue"/>
<text x="200.0" y="74.5" text-anchor="middle" class="km-blue">api.library.example</text>
<text x="200.0" y="116" text-anchor="middle" class="s">host</text>
<rect x="290" y="50" width="50" height="40" rx="4" class="k-gray"/>
<text x="315.0" y="74.5" text-anchor="middle" class="km-gray">:443</text>
<text x="315.0" y="116" text-anchor="middle" class="s">port</text>
<rect x="340" y="50" width="120" height="40" rx="4" class="k-teal"/>
<text x="400.0" y="74.5" text-anchor="middle" class="km-teal">/v1/books/42</text>
<text x="400.0" y="116" text-anchor="middle" class="s">path</text>
<rect x="460" y="50" width="120" height="40" rx="4" class="k-amber"/>
<text x="520.0" y="74.5" text-anchor="middle" class="km-amber">?fields=title</text>
<text x="520.0" y="116" text-anchor="middle" class="s">query</text>
<rect x="580" y="50" width="90" height="40" rx="4" class="k-pink"/>
<text x="625.0" y="74.5" text-anchor="middle" class="km-pink">#reviews</text>
<text x="625.0" y="116" text-anchor="middle" class="s">fragment</text>
<text x="110" y="36" text-anchor="middle" class="c">how</text>
<text x="200" y="36" text-anchor="middle" class="c">which machine</text>
<text x="405" y="36" text-anchor="middle" class="c">which resource</text>
<text x="525" y="36" text-anchor="middle" class="c">options</text>
<text x="360" y="158" text-anchor="middle" class="c">the fragment stays in the browser; the server never sees it</text>
</g>
</svg>
<figcaption>A URL names a resource. In API design, the path identifies the thing and the query string refines how you want it.</figcaption>
</figure>

The **path** identifies the resource; the **query string** (after `?`) carries options such as filters, sorting, and pagination, as `name=value` pairs joined with `&`. Characters with special meaning, such as spaces, `&`, or `/` inside a value, must be **percent-encoded**: a space becomes `%20`. Libraries such as requests do this for you when you pass `params={"q": "jane austen"}`.

## Methods

The method says what the client wants to do with the resource.

| Method | Purpose | Body? | Safe | Idempotent |
|---|---|---|---|---|
| `GET` | Read a resource | No | Yes | Yes |
| `HEAD` | Like `GET`, headers only | No | Yes | Yes |
| `POST` | Create a resource, or trigger an action | Yes | No | No |
| `PUT` | Replace a resource completely | Yes | No | Yes |
| `PATCH` | Change part of a resource | Yes | No | No |
| `DELETE` | Remove a resource | No | No | Yes |
| `OPTIONS` | Ask which methods are allowed (used by CORS) | No | Yes | Yes |

Two properties in the table matter enormously for APIs:

- A **safe** method does not change anything on the server. Clients, caches, and web crawlers may send safe requests freely. Never make a `GET` endpoint that deletes or changes data.
- An **idempotent** method has the same effect whether it is sent once or many times.

<figure class="diagram">
<svg viewBox="0 0 720 250" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Idempotency: sending PUT /books/6 with the same body twice leaves one book in the same state, so a client can safely retry it. Sending POST /books twice creates two books, so blind retries of POST are dangerous." xmlns="http://www.w3.org/2000/svg">
<style>
.a3d{ font-family:var(--sans),sans-serif; }
.a3d .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a3d .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a3d .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a3d .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a3d .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a3d .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a3d .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a3d .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a3d .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a3d .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a3d .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a3d .s{ fill:var(--text-dim); font-size:13px; }
.a3d .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a3d .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a3d .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a3d .c{ fill:var(--text-faint); font-size:12.5px; }
.a3d .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a3d .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a3d .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a3d .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a3d-a); }
.a3d .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a3d-a); marker-start:url(#a3d-s); }
.a3d .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a3d-g); }
.a3d .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a3d-a); }
.a3d .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a3d .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a3d .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a3d .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a3d .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a3d .ks-blue{ fill:#185FA5; font-size:13px; }
.a3d .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a3d .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3d .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a3d .kb-blue, :root[data-theme="dark"] .a3d .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a3d .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a3d .kh-blue{ fill:#85B7EB; }
.a3d .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a3d-blue); }
.a3d .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3d-blue); }
.a3d .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a3d .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a3d .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a3d .ks-teal{ fill:#0F6E56; font-size:13px; }
.a3d .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a3d .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3d .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a3d .kb-teal, :root[data-theme="dark"] .a3d .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a3d .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a3d .kh-teal{ fill:#5DCAA5; }
.a3d .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a3d-teal); }
.a3d .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3d-teal); }
.a3d .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a3d .k-coral{ fill:#FAECE7; stroke:#D85A30; stroke-width:1.6; }
.a3d .kb-coral{ fill:#712B13; font-size:13px; font-weight:700; }
.a3d .ks-coral{ fill:#993C1D; font-size:13px; }
.a3d .km-coral{ fill:#712B13; font-size:12.5px; font-family:var(--mono),monospace; }
.a3d .kh-coral{ fill:#993C1D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3d .k-coral{ fill:#712B13; stroke:#F0997B; }
:root[data-theme="dark"] .a3d .kb-coral, :root[data-theme="dark"] .a3d .km-coral{ fill:#FAECE7; }
:root[data-theme="dark"] .a3d .ks-coral{ fill:#F5C4B3; }
:root[data-theme="dark"] .a3d .kh-coral{ fill:#F0997B; }
.a3d .ar-coral{ stroke:#D85A30; stroke-width:2; fill:none; marker-end:url(#a3d-coral); }
.a3d .ad-coral{ stroke:#D85A30; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3d-coral); }
.a3d .ln-coral{ stroke:#D85A30; stroke-width:2; fill:none; }
.a3d .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a3d .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a3d .ks-purple{ fill:#534AB7; font-size:13px; }
.a3d .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a3d .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3d .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a3d .kb-purple, :root[data-theme="dark"] .a3d .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a3d .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a3d .kh-purple{ fill:#AFA9EC; }
.a3d .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a3d-purple); }
.a3d .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3d-purple); }
.a3d .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a3d .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a3d .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a3d .ks-green{ fill:#3B6D11; font-size:13px; }
.a3d .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a3d .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3d .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a3d .kb-green, :root[data-theme="dark"] .a3d .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a3d .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a3d .kh-green{ fill:#97C459; }
.a3d .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a3d-green); }
.a3d .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3d-green); }
.a3d .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
</style>
<defs><marker id="a3d-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a3d-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a3d-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a3d-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a3d-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a3d-coral" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#D85A30"/></marker><marker id="a3d-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a3d-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker></defs>
<g class="a3d">
<text x="20" y="28" text-anchor="start" class="kh-teal">PUT /books/6 sent twice</text>
<rect x="20" y="42" width="150" height="40" rx="5" class="k-blue"/>
<text x="95.0" y="66.5" text-anchor="middle" class="km-blue">PUT title=Emma</text>
<rect x="20" y="92" width="150" height="40" rx="5" class="k-blue"/>
<text x="95.0" y="116.5" text-anchor="middle" class="km-blue">PUT title=Emma</text>
<line x1="172" y1="62" x2="238" y2="87" class="ar"/>
<line x1="172" y1="112" x2="238" y2="92" class="ar"/>
<rect x="240" y="64" width="110" height="48" rx="7" class="k-purple"/>
<text x="295.0" y="83.5" text-anchor="middle" class="kb-purple">book 6</text>
<text x="295.0" y="101.5" text-anchor="middle" class="ks-purple">title Emma</text>
<text x="195" y="156" text-anchor="middle" class="kh-green">same final state: safe to retry</text>
<text x="390" y="28" text-anchor="start" class="kh-coral">POST /books sent twice</text>
<rect x="390" y="42" width="150" height="40" rx="5" class="k-blue"/>
<text x="465.0" y="66.5" text-anchor="middle" class="km-blue">POST title=Emma</text>
<rect x="390" y="92" width="150" height="40" rx="5" class="k-blue"/>
<text x="465.0" y="116.5" text-anchor="middle" class="km-blue">POST title=Emma</text>
<line x1="542" y1="62" x2="588" y2="62" class="ar"/>
<line x1="542" y1="112" x2="588" y2="112" class="ar"/>
<rect x="590" y="40" width="110" height="44" rx="7" class="k-purple"/>
<text x="645.0" y="66.5" text-anchor="middle" class="kb-purple">book 7</text>
<rect x="590" y="90" width="110" height="44" rx="7" class="k-purple"/>
<text x="645.0" y="116.5" text-anchor="middle" class="kb-purple">book 8</text>
<text x="545" y="156" text-anchor="middle" class="kh-coral">duplicate created: retry with care</text>
<rect x="20" y="186" width="680" height="44" rx="7" class="pnl"/>
<text x="360.0" y="212.5" text-anchor="middle" class="s">GET, HEAD, PUT, DELETE are idempotent. POST and PATCH are not, unless the API adds an idempotency key.</text>
</g>
</svg>
<figcaption>Networks lose responses. Idempotent methods let a client retry without asking whether the first attempt worked.</figcaption>
</figure>

Idempotency matters because networks fail. If a client sends a request and the connection drops before the response arrives, it cannot know whether the server processed it. For idempotent methods the answer does not matter: just send it again. For `POST`, a blind retry might charge a credit card twice. Chapter 10 shows how **idempotency keys** make `POST` safe to retry.

## Status codes

<figure class="diagram">
<svg viewBox="0 0 720 290" style="width:100%;height:auto;max-width:720px" role="img" aria-label="HTTP status code classes: 1xx informational, 2xx success such as 200 OK, 201 Created and 204 No Content, 3xx redirection such as 301 and 304 Not Modified, 4xx client errors such as 400, 401, 403, 404, 409, 422 and 429, and 5xx server errors such as 500, 502, 503 and 504." xmlns="http://www.w3.org/2000/svg">
<style>
.a3c{ font-family:var(--sans),sans-serif; }
.a3c .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a3c .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a3c .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a3c .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a3c .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a3c .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a3c .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a3c .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a3c .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a3c .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a3c .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a3c .s{ fill:var(--text-dim); font-size:13px; }
.a3c .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a3c .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a3c .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a3c .c{ fill:var(--text-faint); font-size:12.5px; }
.a3c .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a3c .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a3c .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a3c .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a3c-a); }
.a3c .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a3c-a); marker-start:url(#a3c-s); }
.a3c .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a3c-g); }
.a3c .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a3c-a); }
.a3c .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a3c .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a3c .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a3c .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a3c .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a3c .ks-blue{ fill:#185FA5; font-size:13px; }
.a3c .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a3c .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3c .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a3c .kb-blue, :root[data-theme="dark"] .a3c .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a3c .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a3c .kh-blue{ fill:#85B7EB; }
.a3c .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a3c-blue); }
.a3c .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3c-blue); }
.a3c .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a3c .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a3c .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a3c .ks-amber{ fill:#854F0B; font-size:13px; }
.a3c .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a3c .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3c .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a3c .kb-amber, :root[data-theme="dark"] .a3c .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a3c .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a3c .kh-amber{ fill:#EF9F27; }
.a3c .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a3c-amber); }
.a3c .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3c-amber); }
.a3c .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a3c .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a3c .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a3c .ks-green{ fill:#3B6D11; font-size:13px; }
.a3c .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a3c .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3c .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a3c .kb-green, :root[data-theme="dark"] .a3c .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a3c .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a3c .kh-green{ fill:#97C459; }
.a3c .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a3c-green); }
.a3c .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3c-green); }
.a3c .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a3c .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a3c .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a3c .ks-red{ fill:#A32D2D; font-size:13px; }
.a3c .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a3c .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3c .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a3c .kb-red, :root[data-theme="dark"] .a3c .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a3c .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a3c .kh-red{ fill:#F09595; }
.a3c .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a3c-red); }
.a3c .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3c-red); }
.a3c .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
.a3c .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a3c .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a3c .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a3c .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a3c .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3c .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a3c .kb-gray, :root[data-theme="dark"] .a3c .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a3c .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a3c .kh-gray{ fill:#B4B2A9; }
.a3c .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a3c-gray); }
.a3c .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3c-gray); }
.a3c .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a3c-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a3c-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a3c-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a3c-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a3c-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a3c-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a3c-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker><marker id="a3c-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a3c">
<rect x="20" y="16" width="80" height="44" rx="7" class="k-gray"/>
<text x="60.0" y="42.5" text-anchor="middle" class="kb-gray">1xx</text>
<text x="120" y="36" text-anchor="start" class="b">informational</text>
<text x="120" y="54" text-anchor="start" class="c">100 Continue, 101 Switching Protocols</text>
<rect x="20" y="70" width="80" height="44" rx="7" class="k-green"/>
<text x="60.0" y="96.5" text-anchor="middle" class="kb-green">2xx</text>
<text x="120" y="90" text-anchor="start" class="b">success</text>
<text x="120" y="108" text-anchor="start" class="c">200 OK, 201 Created, 202 Accepted, 204 No Content</text>
<rect x="20" y="124" width="80" height="44" rx="7" class="k-blue"/>
<text x="60.0" y="150.5" text-anchor="middle" class="kb-blue">3xx</text>
<text x="120" y="144" text-anchor="start" class="b">redirection</text>
<text x="120" y="162" text-anchor="start" class="c">301 Moved Permanently, 304 Not Modified</text>
<rect x="20" y="178" width="80" height="44" rx="7" class="k-amber"/>
<text x="60.0" y="204.5" text-anchor="middle" class="kb-amber">4xx</text>
<text x="120" y="198" text-anchor="start" class="b">client error: fix the request</text>
<text x="120" y="216" text-anchor="start" class="c">400, 401, 403, 404, 409, 422, 429</text>
<rect x="20" y="232" width="80" height="44" rx="7" class="k-red"/>
<text x="60.0" y="258.5" text-anchor="middle" class="kb-red">5xx</text>
<text x="120" y="252" text-anchor="start" class="b">server error: not your fault</text>
<text x="120" y="270" text-anchor="start" class="c">500, 502, 503, 504</text>
</g>
</svg>
<figcaption>The first digit is the most important. Clients must handle every class, including codes they have never seen.</figcaption>
</figure>

The status code is the server's verdict, and clients use it to decide what to do next. The codes you will use most:

| Code | Meaning | Typical use |
|---|---|---|
| `200 OK` | Success | `GET`, `PUT`, `PATCH` with a body in the response |
| `201 Created` | A resource was created | `POST`; include a `Location` header with its URL |
| `202 Accepted` | Accepted, will be processed later | Long-running jobs (Chapter 10) |
| `204 No Content` | Success, no body | `DELETE` |
| `304 Not Modified` | Your cached copy is still valid | Conditional `GET` (Chapter 10) |
| `400 Bad Request` | The request is malformed | Unparseable JSON |
| `401 Unauthorized` | Not authenticated: who are you? | Missing or invalid credentials |
| `403 Forbidden` | Authenticated but not allowed | Missing permission |
| `404 Not Found` | No such resource | Unknown ID |
| `409 Conflict` | Conflicts with current state | Duplicate username |
| `422 Unprocessable Content` | Well-formed but invalid | Validation errors |
| `429 Too Many Requests` | Rate limit exceeded | Include `Retry-After` |
| `500 Internal Server Error` | The server failed | A bug |
| `502`, `503`, `504` | A gateway or upstream problem, or overload | Often temporary: retry later |

The names `401 Unauthorized` and `403 Forbidden` are historically confusing: 401 really means **unauthenticated**, and 403 means **unauthorized**. Chapter 8 returns to the difference.

Try a few with the echo server: `curl -i http://127.0.0.1:8000/status/404`. The `-i` flag prints the response headers.

## Headers

Headers carry everything about a message except its content. A few appear in nearly every API:

| Header | Direction | Purpose |
|---|---|---|
| `Content-Type` | Both | Format of the body: `application/json` |
| `Accept` | Request | Formats the client can handle |
| `Authorization` | Request | Credentials: `Bearer eyJhbGci...` |
| `Location` | Response | URL of a newly created resource |
| `Cache-Control`, `ETag` | Response | Caching rules and version tags (Chapter 10) |
| `Retry-After` | Response | When to try again after `429` or `503` |
| `User-Agent` | Request | Which client software is calling |

Header names are case-insensitive: `content-type` and `Content-Type` are the same header. You can define your own, conventionally without the old `X-` prefix in new designs, although many existing APIs still use names like `X-Request-ID`.

### Content negotiation

A client can ask for a particular format with `Accept`, and the server answers with `Content-Type`. If the server cannot produce any acceptable format, it responds with `406 Not Acceptable`. If the client sends a body in a format the server does not understand, the answer is `415 Unsupported Media Type`. In practice almost all web APIs speak JSON only, but the mechanism is part of HTTP and appears in versioning schemes (Chapter 11).

## Under HTTP: TCP, TLS, and HTTP versions

<figure class="diagram">
<svg viewBox="0 0 720 270" style="width:100%;height:auto;max-width:720px" role="img" aria-label="The protocols under an API call. HTTP/1.1 and HTTP/2 run over TLS over TCP over IP. HTTP/3 runs over QUIC, which includes TLS 1.3 and runs over UDP over IP. All three versions carry the same methods, headers and status codes." xmlns="http://www.w3.org/2000/svg">
<style>
.a3e{ font-family:var(--sans),sans-serif; }
.a3e .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a3e .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a3e .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a3e .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a3e .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a3e .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a3e .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a3e .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a3e .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a3e .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a3e .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a3e .s{ fill:var(--text-dim); font-size:13px; }
.a3e .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a3e .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a3e .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a3e .c{ fill:var(--text-faint); font-size:12.5px; }
.a3e .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a3e .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a3e .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a3e .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a3e-a); }
.a3e .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a3e-a); marker-start:url(#a3e-s); }
.a3e .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a3e-g); }
.a3e .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a3e-a); }
.a3e .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a3e .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a3e .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a3e .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a3e .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a3e .ks-amber{ fill:#854F0B; font-size:13px; }
.a3e .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a3e .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3e .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a3e .kb-amber, :root[data-theme="dark"] .a3e .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a3e .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a3e .kh-amber{ fill:#EF9F27; }
.a3e .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a3e-amber); }
.a3e .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3e-amber); }
.a3e .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a3e .k-coral{ fill:#FAECE7; stroke:#D85A30; stroke-width:1.6; }
.a3e .kb-coral{ fill:#712B13; font-size:13px; font-weight:700; }
.a3e .ks-coral{ fill:#993C1D; font-size:13px; }
.a3e .km-coral{ fill:#712B13; font-size:12.5px; font-family:var(--mono),monospace; }
.a3e .kh-coral{ fill:#993C1D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3e .k-coral{ fill:#712B13; stroke:#F0997B; }
:root[data-theme="dark"] .a3e .kb-coral, :root[data-theme="dark"] .a3e .km-coral{ fill:#FAECE7; }
:root[data-theme="dark"] .a3e .ks-coral{ fill:#F5C4B3; }
:root[data-theme="dark"] .a3e .kh-coral{ fill:#F0997B; }
.a3e .ar-coral{ stroke:#D85A30; stroke-width:2; fill:none; marker-end:url(#a3e-coral); }
.a3e .ad-coral{ stroke:#D85A30; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3e-coral); }
.a3e .ln-coral{ stroke:#D85A30; stroke-width:2; fill:none; }
.a3e .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a3e .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a3e .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a3e .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a3e .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3e .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a3e .kb-gray, :root[data-theme="dark"] .a3e .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a3e .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a3e .kh-gray{ fill:#B4B2A9; }
.a3e .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a3e-gray); }
.a3e .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3e-gray); }
.a3e .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a3e-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a3e-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a3e-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a3e-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a3e-coral" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#D85A30"/></marker><marker id="a3e-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a3e">
<rect x="20" y="20" width="200" height="40" rx="7" class="k-amber"/>
<text x="120.0" y="44.5" text-anchor="middle" class="kb-amber">HTTP/1.1</text>
<rect x="260" y="20" width="200" height="40" rx="7" class="k-amber"/>
<text x="360.0" y="44.5" text-anchor="middle" class="kb-amber">HTTP/2</text>
<rect x="500" y="20" width="200" height="40" rx="7" class="k-amber"/>
<text x="600.0" y="44.5" text-anchor="middle" class="kb-amber">HTTP/3</text>
<rect x="20" y="70" width="440" height="40" rx="7" class="k-coral"/>
<text x="240.0" y="94.5" text-anchor="middle" class="kb-coral">TLS (encryption, server identity)</text>
<rect x="20" y="120" width="440" height="40" rx="7" class="k-gray"/>
<text x="240.0" y="144.5" text-anchor="middle" class="kb-gray">TCP (reliable byte stream)</text>
<rect x="500" y="70" width="200" height="90" rx="7" class="k-coral"/>
<text x="600.0" y="101.5" text-anchor="middle" class="kb-coral">QUIC</text>
<text x="600.0" y="119.5" text-anchor="middle" class="ks-coral">TLS 1.3 built in</text>
<text x="600.0" y="137.5" text-anchor="middle" class="ks-coral">streams, fast setup</text>
<rect x="20" y="170" width="440" height="36" rx="7" class="k-gray"/>
<text x="240.0" y="192.5" text-anchor="middle" class="kb-gray">IP</text>
<rect x="500" y="170" width="200" height="36" rx="7" class="k-gray"/>
<text x="600.0" y="192.5" text-anchor="middle" class="kb-gray">UDP over IP</text>
<text x="360" y="238" text-anchor="middle" class="c">every version keeps the same semantics: methods, headers, status codes</text>
</g>
</svg>
<figcaption>For API design the HTTP version rarely matters; the semantics are identical. It matters for performance and for gRPC, which needs HTTP/2.</figcaption>
</figure>

- **HTTP/1.1** sends one request at a time per TCP connection. Clients open several connections to work in parallel.
- **HTTP/2** encodes messages in binary and **multiplexes** many requests over one connection. gRPC requires it.
- **HTTP/3** runs over **QUIC**, which uses UDP and builds encryption in, avoiding delays when packets are lost.

All three versions carry the same methods, headers, and status codes, so API design is the same on each.

**TLS** encrypts the connection and proves the server's identity with a certificate. An API reached with `https://` uses TLS; one reached with `http://` sends everything, including passwords and tokens, in clear text. Every API on a real network must use HTTPS. The lab uses plain HTTP only because it never leaves your own machine.

## Statelessness

HTTP is **stateless**: each request stands alone, and the server keeps no memory of earlier requests from the same client.

<figure class="diagram">
<svg viewBox="0 0 720 260" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Statelessness: each request carries everything the server needs, including the access token, so any of several identical servers behind a load balancer can answer it. No server remembers the client between requests." xmlns="http://www.w3.org/2000/svg">
<style>
.a3f{ font-family:var(--sans),sans-serif; }
.a3f .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a3f .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a3f .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a3f .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a3f .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a3f .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a3f .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a3f .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a3f .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a3f .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a3f .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a3f .s{ fill:var(--text-dim); font-size:13px; }
.a3f .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a3f .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a3f .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a3f .c{ fill:var(--text-faint); font-size:12.5px; }
.a3f .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a3f .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a3f .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a3f .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a3f-a); }
.a3f .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a3f-a); marker-start:url(#a3f-s); }
.a3f .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a3f-g); }
.a3f .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a3f-a); }
.a3f .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a3f .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a3f .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a3f .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a3f .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a3f .ks-blue{ fill:#185FA5; font-size:13px; }
.a3f .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a3f .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3f .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a3f .kb-blue, :root[data-theme="dark"] .a3f .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a3f .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a3f .kh-blue{ fill:#85B7EB; }
.a3f .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a3f-blue); }
.a3f .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3f-blue); }
.a3f .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a3f .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a3f .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a3f .ks-teal{ fill:#0F6E56; font-size:13px; }
.a3f .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a3f .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3f .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a3f .kb-teal, :root[data-theme="dark"] .a3f .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a3f .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a3f .kh-teal{ fill:#5DCAA5; }
.a3f .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a3f-teal); }
.a3f .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3f-teal); }
.a3f .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a3f .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a3f .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a3f .ks-purple{ fill:#534AB7; font-size:13px; }
.a3f .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a3f .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3f .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a3f .kb-purple, :root[data-theme="dark"] .a3f .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a3f .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a3f .kh-purple{ fill:#AFA9EC; }
.a3f .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a3f-purple); }
.a3f .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3f-purple); }
.a3f .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a3f .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a3f .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a3f .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a3f .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a3f .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a3f .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a3f .kb-gray, :root[data-theme="dark"] .a3f .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a3f .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a3f .kh-gray{ fill:#B4B2A9; }
.a3f .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a3f-gray); }
.a3f .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a3f-gray); }
.a3f .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a3f-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a3f-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a3f-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a3f-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a3f-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a3f-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a3f-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a3f">
<rect x="20" y="100" width="150" height="64" rx="7" class="k-blue"/>
<text x="95.0" y="127.5" text-anchor="middle" class="kb-blue">client</text>
<text x="95.0" y="145.5" text-anchor="middle" class="ks-blue">token in every request</text>
<rect x="240" y="104" width="130" height="56" rx="7" class="k-gray"/>
<text x="305.0" y="136.5" text-anchor="middle" class="kb-gray">load balancer</text>
<rect x="450" y="30" width="120" height="54" rx="7" class="k-teal"/>
<text x="510.0" y="52.5" text-anchor="middle" class="kb-teal">server 1</text>
<text x="510.0" y="70.5" text-anchor="middle" class="ks-teal">no session state</text>
<line x1="372" y1="132" x2="448" y2="57" class="ar-gray"/>
<rect x="450" y="104" width="120" height="54" rx="7" class="k-teal"/>
<text x="510.0" y="126.5" text-anchor="middle" class="kb-teal">server 2</text>
<text x="510.0" y="144.5" text-anchor="middle" class="ks-teal">no session state</text>
<line x1="372" y1="132" x2="448" y2="131" class="ar-gray"/>
<rect x="450" y="178" width="120" height="54" rx="7" class="k-teal"/>
<text x="510.0" y="200.5" text-anchor="middle" class="kb-teal">server 3</text>
<text x="510.0" y="218.5" text-anchor="middle" class="ks-teal">no session state</text>
<line x1="372" y1="132" x2="448" y2="205" class="ar-gray"/>
<rect x="610" y="100" width="90" height="64" rx="7" class="k-purple"/>
<text x="655.0" y="136.5" text-anchor="middle" class="kb-purple">database</text>
<line x1="572" y1="57" x2="608" y2="132" class="ln"/>
<line x1="572" y1="131" x2="608" y2="132" class="ln"/>
<line x1="572" y1="205" x2="608" y2="132" class="ln"/>
<line x1="172" y1="132" x2="238" y2="132" class="ar-blue"/>
<text x="95" y="210" text-anchor="middle" class="c">request 1 to server 1,</text>
<text x="95" y="228" text-anchor="middle" class="c">request 2 to server 3: fine</text>
</g>
</svg>
<figcaption>Stateless servers are interchangeable, so you can add more of them when traffic grows. State lives in the token and the database.</figcaption>
</figure>

That sounds like a limitation, but it is what lets APIs scale. If every request carries what the server needs, such as an access token identifying the user, then any server in a pool can handle any request. You can add servers behind a load balancer when traffic grows, and lose one without losing anyone's session. Data that must persist lives in a shared database, not in a server's memory.

## Hands on: HTTP with curl

With the echo server running, try these and read every line of output:

```bash
curl -i  http://127.0.0.1:8000/headers                     # response headers, including custom ones
curl -I  http://127.0.0.1:8000/headers                     # HEAD: headers only, no body
curl -i  "http://127.0.0.1:8000/echo?q=jane%20austen&page=2"   # a query string, percent-encoded
curl -s -X PUT http://127.0.0.1:8000/echo -d 'plain text'  # a body without Content-Type JSON
curl -i -X GET http://127.0.0.1:8000/books                 # a path that does not exist: 404
```

The last request returns `404` with a JSON body, because FastAPI answers unknown paths for you. Notice also what `curl` adds without being asked: `Host`, `User-Agent`, and `Accept`.

## Summary

- HTTP messages have a **start line**, **headers**, a **blank line**, and an optional **body**.
- **Methods** state intent. **Safe** methods change nothing; **idempotent** methods can be repeated safely. `POST` is neither.
- **Status codes** give the verdict: 2xx success, 4xx client error, 5xx server error. Use them precisely.
- **Headers** carry metadata: content type, credentials, caching, retry hints.
- HTTP/1.1, /2, and /3 share the same semantics. Real APIs always use **HTTPS**.
- HTTP is **stateless**, which is what lets APIs scale across many servers.

## Check your understanding

Choose the best answer for each question, then check your answers in [Answers to Chapter Questions](answers.md#chapter-3-http-for-apis).

**1. What separates the headers from the body of an HTTP message?**

- A. A blank line
- B. A semicolon
- C. A closing tag
- D. The Content-Length header

**2. Which method is neither safe nor idempotent?**

- A. GET
- B. PUT
- C. POST
- D. DELETE

**3. What does idempotent mean for a method?**

- A. It is fast
- B. It changes nothing on the server
- C. It needs no authentication
- D. Repeating the same request has the same effect as sending it once

**4. A request has no credentials. Which status code fits?**

- A. 400
- B. 401
- C. 403
- D. 404

**5. What does a 5xx status code mean?**

- A. Success
- B. Redirection
- C. The server failed
- D. The client sent a bad request

**6. How does a client ask for a particular response format, such as JSON?**

- A. With the Accept header
- B. With the Content-Type header
- C. With a .json extension
- D. With a query parameter only

**7. Which HTTP version runs over QUIC instead of TCP?**

- A. HTTP/1.0
- B. HTTP/1.1
- C. HTTP/2
- D. HTTP/3

**8. Why does HTTP's statelessness help APIs scale?**

- A. Requests are smaller
- B. It removes the need for TLS
- C. Each request carries everything needed, so any server can handle it
- D. It caches everything
