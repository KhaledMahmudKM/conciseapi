# Chapter 10: Performance and Reliability

An API that works for one user on a laptop can still fail in production: slow under load, overwhelmed by a single noisy client, or creating duplicate orders when the network hiccups. This chapter covers the techniques that keep APIs fast and dependable, all demonstrated in `library_perf.py` and `retry_client.py`.

## Where the time goes

<figure class="diagram">
<svg viewBox="0 0 720 200" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Where the time goes in one API call from a distant client: DNS lookup, TCP connection, TLS handshake, sending the request, server processing including a database query, and transferring the response. On a new connection the network setup can take longer than the server&#x27;s own work." xmlns="http://www.w3.org/2000/svg">
<style>
.a10a{ font-family:var(--sans),sans-serif; }
.a10a .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a10a .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a10a .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a10a .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a10a .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a10a .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a10a .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a10a .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a10a .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a10a .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a10a .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a10a .s{ fill:var(--text-dim); font-size:13px; }
.a10a .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a10a .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a10a .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a10a .c{ fill:var(--text-faint); font-size:12.5px; }
.a10a .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a10a .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a10a .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a10a .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a10a-a); }
.a10a .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a10a-a); marker-start:url(#a10a-s); }
.a10a .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a10a-g); }
.a10a .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a10a-a); }
.a10a .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a10a .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a10a .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a10a .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a10a .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a10a .ks-blue{ fill:#185FA5; font-size:13px; }
.a10a .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a10a .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10a .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a10a .kb-blue, :root[data-theme="dark"] .a10a .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a10a .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a10a .kh-blue{ fill:#85B7EB; }
.a10a .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a10a-blue); }
.a10a .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10a-blue); }
.a10a .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a10a .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a10a .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a10a .ks-teal{ fill:#0F6E56; font-size:13px; }
.a10a .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a10a .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10a .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a10a .kb-teal, :root[data-theme="dark"] .a10a .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a10a .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a10a .kh-teal{ fill:#5DCAA5; }
.a10a .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a10a-teal); }
.a10a .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10a-teal); }
.a10a .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a10a .k-coral{ fill:#FAECE7; stroke:#D85A30; stroke-width:1.6; }
.a10a .kb-coral{ fill:#712B13; font-size:13px; font-weight:700; }
.a10a .ks-coral{ fill:#993C1D; font-size:13px; }
.a10a .km-coral{ fill:#712B13; font-size:12.5px; font-family:var(--mono),monospace; }
.a10a .kh-coral{ fill:#993C1D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10a .k-coral{ fill:#712B13; stroke:#F0997B; }
:root[data-theme="dark"] .a10a .kb-coral, :root[data-theme="dark"] .a10a .km-coral{ fill:#FAECE7; }
:root[data-theme="dark"] .a10a .ks-coral{ fill:#F5C4B3; }
:root[data-theme="dark"] .a10a .kh-coral{ fill:#F0997B; }
.a10a .ar-coral{ stroke:#D85A30; stroke-width:2; fill:none; marker-end:url(#a10a-coral); }
.a10a .ad-coral{ stroke:#D85A30; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10a-coral); }
.a10a .ln-coral{ stroke:#D85A30; stroke-width:2; fill:none; }
.a10a .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a10a .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a10a .ks-purple{ fill:#534AB7; font-size:13px; }
.a10a .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a10a .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10a .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a10a .kb-purple, :root[data-theme="dark"] .a10a .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a10a .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a10a .kh-purple{ fill:#AFA9EC; }
.a10a .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a10a-purple); }
.a10a .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10a-purple); }
.a10a .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a10a .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a10a .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a10a .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a10a .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a10a .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10a .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a10a .kb-gray, :root[data-theme="dark"] .a10a .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a10a .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a10a .kh-gray{ fill:#B4B2A9; }
.a10a .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a10a-gray); }
.a10a .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10a-gray); }
.a10a .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a10a-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a10a-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a10a-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a10a-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a10a-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a10a-coral" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#D85A30"/></marker><marker id="a10a-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a10a-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a10a">
<rect x="20" y="40" width="46.89655172413793" height="50" rx="4" class="k-gray"/>
<text x="43.44827586206897" y="69.5" text-anchor="middle" class="ks-gray">DNS</text>
<rect x="66.89655172413794" y="40" width="82.06896551724138" height="50" rx="4" class="k-blue"/>
<text x="107.93103448275863" y="69.5" text-anchor="middle" class="ks-blue">TCP</text>
<rect x="148.9655172413793" y="40" width="140.68965517241378" height="50" rx="4" class="k-purple"/>
<text x="219.3103448275862" y="69.5" text-anchor="middle" class="ks-purple">TLS</text>
<rect x="289.6551724137931" y="40" width="46.89655172413793" height="50" rx="4" class="k-blue"/>
<text x="313.10344827586204" y="69.5" text-anchor="middle" class="ks-blue">send</text>
<rect x="336.551724137931" y="40" width="82.06896551724138" height="50" rx="4" class="k-teal"/>
<text x="377.5862068965517" y="69.5" text-anchor="middle" class="ks-teal">app</text>
<rect x="418.6206896551724" y="40" width="175.86206896551724" height="50" rx="4" class="k-coral"/>
<text x="506.551724137931" y="69.5" text-anchor="middle" class="ks-coral">database</text>
<rect x="594.4827586206897" y="40" width="105.51724137931035" height="50" rx="4" class="k-blue"/>
<text x="647.2413793103449" y="69.5" text-anchor="middle" class="ks-blue">response</text>
<text x="20" y="26" text-anchor="start" class="kh-gray">new connection, distant client (illustrative)</text>
<line x1="20" y1="110" x2="336.55172413793105" y2="110" class="ln-purple"/>
<text x="178.27586206896552" y="130" text-anchor="middle" class="kh-purple">connection setup: reuse it</text>
<line x1="383.44827586206895" y1="110" x2="641.3793103448276" y2="110" class="ln-coral"/>
<text x="512.4137931034483" y="130" text-anchor="middle" class="kh-coral">server work: cache it</text>
<text x="360" y="180" text-anchor="middle" class="c">keep-alive connections, caching, smaller payloads, and fewer round trips all cut latency</text>
</g>
</svg>
<figcaption>Measure before optimising. The slowest part is often not the code you are looking at.</figcaption>
</figure>

Before optimising, measure. For a client far from the server, setting up a new connection (DNS, TCP, TLS) can take several round trips before the request is even sent. Inside the server, the database is often the slowest part. The main levers:

- **Reuse connections.** HTTP keep-alive (and HTTP/2) avoids repeated handshakes. In Python, use a `requests.Session` or an `httpx.Client` instead of one-off calls.
- **Cache** results so that repeated requests skip work.
- **Send less**: paginate, let clients choose fields, and compress responses (`Content-Encoding: gzip` or `br`).
- **Make fewer calls**: design endpoints around what clients actually need, so a screen does not need ten requests.
- **Watch the database**: add indexes, avoid one query per item in a loop (the "N+1" problem), and use connection pools.

Report latency as **percentiles**, not averages. A p95 of 300 ms means 95% of requests finish within 300 ms; the average hides the slow tail that users actually notice.

## HTTP caching

<figure class="diagram">
<svg viewBox="0 0 720 230" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Caches along the path of a request: the client&#x27;s own HTTP cache, a CDN or shared proxy, a cache at the gateway, an application cache such as Redis, and finally the database. Each cache that answers saves every hop behind it." xmlns="http://www.w3.org/2000/svg">
<style>
.a10b{ font-family:var(--sans),sans-serif; }
.a10b .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a10b .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a10b .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a10b .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a10b .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a10b .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a10b .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a10b .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a10b .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a10b .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a10b .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a10b .s{ fill:var(--text-dim); font-size:13px; }
.a10b .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a10b .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a10b .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a10b .c{ fill:var(--text-faint); font-size:12.5px; }
.a10b .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a10b .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a10b .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a10b .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a10b-a); }
.a10b .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a10b-a); marker-start:url(#a10b-s); }
.a10b .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a10b-g); }
.a10b .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a10b-a); }
.a10b .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a10b .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a10b .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a10b .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a10b .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a10b .ks-blue{ fill:#185FA5; font-size:13px; }
.a10b .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a10b .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10b .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a10b .kb-blue, :root[data-theme="dark"] .a10b .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a10b .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a10b .kh-blue{ fill:#85B7EB; }
.a10b .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a10b-blue); }
.a10b .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10b-blue); }
.a10b .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a10b .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a10b .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a10b .ks-teal{ fill:#0F6E56; font-size:13px; }
.a10b .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a10b .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10b .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a10b .kb-teal, :root[data-theme="dark"] .a10b .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a10b .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a10b .kh-teal{ fill:#5DCAA5; }
.a10b .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a10b-teal); }
.a10b .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10b-teal); }
.a10b .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a10b .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a10b .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a10b .ks-amber{ fill:#854F0B; font-size:13px; }
.a10b .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a10b .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10b .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a10b .kb-amber, :root[data-theme="dark"] .a10b .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a10b .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a10b .kh-amber{ fill:#EF9F27; }
.a10b .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a10b-amber); }
.a10b .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10b-amber); }
.a10b .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a10b .k-coral{ fill:#FAECE7; stroke:#D85A30; stroke-width:1.6; }
.a10b .kb-coral{ fill:#712B13; font-size:13px; font-weight:700; }
.a10b .ks-coral{ fill:#993C1D; font-size:13px; }
.a10b .km-coral{ fill:#712B13; font-size:12.5px; font-family:var(--mono),monospace; }
.a10b .kh-coral{ fill:#993C1D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10b .k-coral{ fill:#712B13; stroke:#F0997B; }
:root[data-theme="dark"] .a10b .kb-coral, :root[data-theme="dark"] .a10b .km-coral{ fill:#FAECE7; }
:root[data-theme="dark"] .a10b .ks-coral{ fill:#F5C4B3; }
:root[data-theme="dark"] .a10b .kh-coral{ fill:#F0997B; }
.a10b .ar-coral{ stroke:#D85A30; stroke-width:2; fill:none; marker-end:url(#a10b-coral); }
.a10b .ad-coral{ stroke:#D85A30; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10b-coral); }
.a10b .ln-coral{ stroke:#D85A30; stroke-width:2; fill:none; }
.a10b .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a10b .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a10b .ks-purple{ fill:#534AB7; font-size:13px; }
.a10b .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a10b .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10b .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a10b .kb-purple, :root[data-theme="dark"] .a10b .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a10b .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a10b .kh-purple{ fill:#AFA9EC; }
.a10b .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a10b-purple); }
.a10b .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10b-purple); }
.a10b .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a10b .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a10b .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a10b .ks-green{ fill:#3B6D11; font-size:13px; }
.a10b .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a10b .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10b .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a10b .kb-green, :root[data-theme="dark"] .a10b .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a10b .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a10b .kh-green{ fill:#97C459; }
.a10b .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a10b-green); }
.a10b .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10b-green); }
.a10b .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a10b .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a10b .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a10b .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a10b .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a10b .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10b .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a10b .kb-gray, :root[data-theme="dark"] .a10b .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a10b .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a10b .kh-gray{ fill:#B4B2A9; }
.a10b .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a10b-gray); }
.a10b .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10b-gray); }
.a10b .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a10b-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a10b-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a10b-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a10b-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a10b-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a10b-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a10b-coral" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#D85A30"/></marker><marker id="a10b-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a10b-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a10b-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a10b">
<rect x="20" y="50" width="120" height="64" rx="7" class="k-blue"/>
<text x="80.0" y="77.5" text-anchor="middle" class="kb-blue">client cache</text>
<text x="80.0" y="95.5" text-anchor="middle" class="ks-blue">private</text>
<rect x="160" y="50" width="120" height="64" rx="7" class="k-amber"/>
<text x="220.0" y="77.5" text-anchor="middle" class="kb-amber">CDN / proxy</text>
<text x="220.0" y="95.5" text-anchor="middle" class="ks-amber">public, shared</text>
<line x1="142" y1="82" x2="158" y2="82" class="ar"/>
<rect x="300" y="50" width="120" height="64" rx="7" class="k-gray"/>
<text x="360.0" y="77.5" text-anchor="middle" class="kb-gray">gateway</text>
<text x="360.0" y="95.5" text-anchor="middle" class="ks-gray">response cache</text>
<line x1="282" y1="82" x2="298" y2="82" class="ar"/>
<rect x="440" y="50" width="120" height="64" rx="7" class="k-teal"/>
<text x="500.0" y="77.5" text-anchor="middle" class="kb-teal">app cache</text>
<text x="500.0" y="95.5" text-anchor="middle" class="ks-teal">Redis, memory</text>
<line x1="422" y1="82" x2="438" y2="82" class="ar"/>
<rect x="580" y="50" width="120" height="64" rx="7" class="k-purple"/>
<text x="640.0" y="77.5" text-anchor="middle" class="kb-purple">database</text>
<text x="640.0" y="95.5" text-anchor="middle" class="ks-purple">source of truth</text>
<line x1="562" y1="82" x2="578" y2="82" class="ar"/>
<line x1="80" y1="130" x2="640" y2="130" class="ln"/>
<text x="80" y="150" text-anchor="start" class="kh-green">fastest, closest</text>
<text x="640" y="150" text-anchor="end" class="kh-coral">slowest, authoritative</text>
<rect x="20" y="172" width="680" height="44" rx="7" class="k-amber"/>
<text x="360.0" y="198.5" text-anchor="middle" class="kb-amber">HTTP headers control the first two: Cache-Control, ETag, Last-Modified, Vary</text>
</g>
</svg>
<figcaption>A response marked private may be stored only by the client; public lets shared caches such as CDNs store it too.</figcaption>
</figure>

HTTP has caching built in, controlled by response headers:

| Header | Meaning |
|---|---|
| `Cache-Control: max-age=60` | The response may be reused for 60 seconds without asking the server |
| `Cache-Control: private` | Only the client may store it, not shared caches (use for per-user data) |
| `Cache-Control: public` | Shared caches such as CDNs may store it |
| `Cache-Control: no-store` | Never store it (sensitive data) |
| `ETag: "3b554e5b11cd51b1"` | A version identifier for this representation |
| `Vary: Accept, Authorization` | The response differs by these request headers; caches must key on them |

### Conditional requests

<figure class="diagram">
<svg viewBox="0 0 720 260" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Conditional GET with an ETag. The first request returns 200 with the book and an ETag header. Later the client sends If-None-Match with that ETag. If the book is unchanged the server returns 304 Not Modified with no body, and the client uses its cached copy." xmlns="http://www.w3.org/2000/svg">
<style>
.a10c{ font-family:var(--sans),sans-serif; }
.a10c .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a10c .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a10c .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a10c .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a10c .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a10c .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a10c .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a10c .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a10c .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a10c .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a10c .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a10c .s{ fill:var(--text-dim); font-size:13px; }
.a10c .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a10c .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a10c .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a10c .c{ fill:var(--text-faint); font-size:12.5px; }
.a10c .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a10c .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a10c .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a10c .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a10c-a); }
.a10c .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a10c-a); marker-start:url(#a10c-s); }
.a10c .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a10c-g); }
.a10c .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a10c-a); }
.a10c .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a10c .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a10c .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a10c .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a10c .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a10c .ks-blue{ fill:#185FA5; font-size:13px; }
.a10c .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a10c .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10c .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a10c .kb-blue, :root[data-theme="dark"] .a10c .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a10c .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a10c .kh-blue{ fill:#85B7EB; }
.a10c .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a10c-blue); }
.a10c .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10c-blue); }
.a10c .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a10c .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a10c .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a10c .ks-teal{ fill:#0F6E56; font-size:13px; }
.a10c .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a10c .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10c .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a10c .kb-teal, :root[data-theme="dark"] .a10c .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a10c .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a10c .kh-teal{ fill:#5DCAA5; }
.a10c .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a10c-teal); }
.a10c .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10c-teal); }
.a10c .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a10c .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a10c .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a10c .ks-green{ fill:#3B6D11; font-size:13px; }
.a10c .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a10c .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10c .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a10c .kb-green, :root[data-theme="dark"] .a10c .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a10c .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a10c .kh-green{ fill:#97C459; }
.a10c .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a10c-green); }
.a10c .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10c-green); }
.a10c .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a10c .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a10c .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a10c .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a10c .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a10c .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10c .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a10c .kb-gray, :root[data-theme="dark"] .a10c .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a10c .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a10c .kh-gray{ fill:#B4B2A9; }
.a10c .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a10c-gray); }
.a10c .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10c-gray); }
.a10c .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a10c-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a10c-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a10c-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a10c-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a10c-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a10c-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a10c-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a10c">
<rect x="85" y="16" width="150" height="40" rx="7" class="k-blue"/>
<text x="160.0" y="40.5" text-anchor="middle" class="kb-blue">client</text>
<line x1="160" y1="56" x2="160" y2="250" class="gd"/>
<rect x="485" y="16" width="150" height="40" rx="7" class="k-teal"/>
<text x="560.0" y="40.5" text-anchor="middle" class="kb-teal">server</text>
<line x1="560" y1="56" x2="560" y2="250" class="gd"/>
<line x1="162" y1="90" x2="558" y2="90" class="ar-blue"/>
<text x="360.0" y="83" text-anchor="middle" class="s">GET /books/1</text>
<line x1="558" y1="130" x2="162" y2="130" class="ar-teal"/>
<text x="360.0" y="123" text-anchor="middle" class="s">200, ETag: "3b55...", body</text>
<line x1="162" y1="190" x2="558" y2="190" class="ar-blue"/>
<text x="360.0" y="183" text-anchor="middle" class="s">GET /books/1, If-None-Match: "3b55..."</text>
<line x1="558" y1="230" x2="162" y2="230" class="ar-green"/>
<text x="360.0" y="223" text-anchor="middle" class="s">304 Not Modified, no body</text>
<text x="60" y="166" text-anchor="start" class="kh-gray">60 s later</text>
</g>
</svg>
<figcaption>A 304 still costs a round trip, but no body and usually no database work. Cache-Control: max-age avoids even the round trip.</figcaption>
</figure>

An **ETag** lets a client ask "has it changed?" instead of downloading again. `library_perf.py` computes the ETag as a hash of the book's JSON:

```python
@app.get("/books/{book_id}")
def get_book(book_id: int, response: Response, if_none_match: str | None = Header(default=None)):
    book = BOOKS.get(book_id)
    if book is None:
        raise HTTPException(404, "No such book")
    tag = etag_of(book)
    headers = {"ETag": tag, "Cache-Control": "private, max-age=60"}
    if if_none_match == tag:                       # the client's copy is still current
        return Response(status_code=304, headers=headers)
    response.headers.update(headers)
    return book
```

Run `fastapi dev library_perf.py` and try it:

```bash
curl -i http://127.0.0.1:8000/books/1
curl -i http://127.0.0.1:8000/books/1 -H 'If-None-Match: "3b554e5b11cd51b1"'
```

```text
HTTP/1.1 200 OK
etag: "3b554e5b11cd51b1"
cache-control: private, max-age=60
{"id":1,"title":"Dune","year":1965}

HTTP/1.1 304 Not Modified
```

### Preventing lost updates

<figure class="diagram">
<svg viewBox="0 0 720 300" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Preventing lost updates with If-Match. Alice and Bob both read book 1 with the same ETag. Alice writes first with If-Match and succeeds, which changes the ETag. Bob then writes with the old ETag and gets 412 Precondition Failed, so he must re-read before writing, instead of silently overwriting Alice&#x27;s change." xmlns="http://www.w3.org/2000/svg">
<style>
.a10d{ font-family:var(--sans),sans-serif; }
.a10d .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a10d .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a10d .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a10d .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a10d .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a10d .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a10d .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a10d .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a10d .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a10d .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a10d .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a10d .s{ fill:var(--text-dim); font-size:13px; }
.a10d .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a10d .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a10d .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a10d .c{ fill:var(--text-faint); font-size:12.5px; }
.a10d .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a10d .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a10d .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a10d .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a10d-a); }
.a10d .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a10d-a); marker-start:url(#a10d-s); }
.a10d .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a10d-g); }
.a10d .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a10d-a); }
.a10d .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a10d .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a10d .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a10d .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a10d .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a10d .ks-blue{ fill:#185FA5; font-size:13px; }
.a10d .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a10d .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10d .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a10d .kb-blue, :root[data-theme="dark"] .a10d .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a10d .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a10d .kh-blue{ fill:#85B7EB; }
.a10d .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a10d-blue); }
.a10d .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10d-blue); }
.a10d .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a10d .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a10d .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a10d .ks-teal{ fill:#0F6E56; font-size:13px; }
.a10d .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a10d .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10d .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a10d .kb-teal, :root[data-theme="dark"] .a10d .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a10d .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a10d .kh-teal{ fill:#5DCAA5; }
.a10d .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a10d-teal); }
.a10d .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10d-teal); }
.a10d .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a10d .k-coral{ fill:#FAECE7; stroke:#D85A30; stroke-width:1.6; }
.a10d .kb-coral{ fill:#712B13; font-size:13px; font-weight:700; }
.a10d .ks-coral{ fill:#993C1D; font-size:13px; }
.a10d .km-coral{ fill:#712B13; font-size:12.5px; font-family:var(--mono),monospace; }
.a10d .kh-coral{ fill:#993C1D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10d .k-coral{ fill:#712B13; stroke:#F0997B; }
:root[data-theme="dark"] .a10d .kb-coral, :root[data-theme="dark"] .a10d .km-coral{ fill:#FAECE7; }
:root[data-theme="dark"] .a10d .ks-coral{ fill:#F5C4B3; }
:root[data-theme="dark"] .a10d .kh-coral{ fill:#F0997B; }
.a10d .ar-coral{ stroke:#D85A30; stroke-width:2; fill:none; marker-end:url(#a10d-coral); }
.a10d .ad-coral{ stroke:#D85A30; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10d-coral); }
.a10d .ln-coral{ stroke:#D85A30; stroke-width:2; fill:none; }
.a10d .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a10d .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a10d .ks-green{ fill:#3B6D11; font-size:13px; }
.a10d .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a10d .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10d .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a10d .kb-green, :root[data-theme="dark"] .a10d .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a10d .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a10d .kh-green{ fill:#97C459; }
.a10d .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a10d-green); }
.a10d .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10d-green); }
.a10d .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a10d .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a10d .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a10d .ks-red{ fill:#A32D2D; font-size:13px; }
.a10d .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a10d .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10d .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a10d .kb-red, :root[data-theme="dark"] .a10d .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a10d .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a10d .kh-red{ fill:#F09595; }
.a10d .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a10d-red); }
.a10d .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10d-red); }
.a10d .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
</style>
<defs><marker id="a10d-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a10d-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a10d-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a10d-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a10d-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a10d-coral" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#D85A30"/></marker><marker id="a10d-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a10d-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker></defs>
<g class="a10d">
<rect x="35" y="16" width="150" height="40" rx="7" class="k-blue"/>
<text x="110.0" y="40.5" text-anchor="middle" class="kb-blue">Alice</text>
<line x1="110" y1="56" x2="110" y2="290" class="gd"/>
<rect x="285" y="16" width="150" height="40" rx="7" class="k-teal"/>
<text x="360.0" y="40.5" text-anchor="middle" class="kb-teal">server</text>
<line x1="360" y1="56" x2="360" y2="290" class="gd"/>
<rect x="535" y="16" width="150" height="40" rx="7" class="k-coral"/>
<text x="610.0" y="40.5" text-anchor="middle" class="kb-coral">Bob</text>
<line x1="610" y1="56" x2="610" y2="290" class="gd"/>
<line x1="112" y1="90" x2="358" y2="90" class="ar-blue"/>
<text x="235.0" y="83" text-anchor="middle" class="s">GET  (ETag A)</text>
<line x1="608" y1="120" x2="362" y2="120" class="ar-coral"/>
<text x="485.0" y="113" text-anchor="middle" class="s">GET  (ETag A)</text>
<line x1="112" y1="166" x2="358" y2="166" class="ar-blue"/>
<text x="235.0" y="159" text-anchor="middle" class="s">PUT, If-Match: A</text>
<line x1="358" y1="196" x2="112" y2="196" class="ar-green"/>
<text x="235.0" y="189" text-anchor="middle" class="s">200, now ETag B</text>
<line x1="608" y1="242" x2="362" y2="242" class="ar-coral"/>
<text x="485.0" y="235" text-anchor="middle" class="s">PUT, If-Match: A</text>
<line x1="362" y1="272" x2="608" y2="272" class="ar-red"/>
<text x="485.0" y="265" text-anchor="middle" class="s">412 Precondition Failed</text>
</g>
</svg>
<figcaption>Optimistic concurrency: no locks, just a check that nobody changed the resource since you read it.</figcaption>
</figure>

The same ETag solves a different problem. If Alice and Bob both read a book and both save changes, the second save silently overwrites the first. With **optimistic concurrency**, a write must include `If-Match` with the ETag the client last read:

```text
PUT /books/1 (no If-Match)          -> 428 {"detail":"Send If-Match with the ETag you last read"}
PUT /books/1, If-Match: "3b55..."   -> 200 {"id":1,"title":"Dune","year":1966}
PUT /books/1, If-Match: "3b55..."   -> 412 {"detail":"The book changed; read it again"}
```

The third request uses the old ETag, so the server refuses it with **412 Precondition Failed**. **428 Precondition Required** tells clients that forget the header to add it.

## Rate limiting

<figure class="diagram">
<svg viewBox="0 0 720 260" style="width:100%;height:auto;max-width:720px" role="img" aria-label="A token bucket rate limiter. Tokens drip into a bucket at a steady rate, five per second, up to a capacity of ten. Each request takes one token. A burst of up to ten requests is allowed at once; when the bucket is empty, requests get 429 Too Many Requests with a Retry-After header." xmlns="http://www.w3.org/2000/svg">
<style>
.a10e{ font-family:var(--sans),sans-serif; }
.a10e .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a10e .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a10e .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a10e .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a10e .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a10e .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a10e .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a10e .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a10e .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a10e .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a10e .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a10e .s{ fill:var(--text-dim); font-size:13px; }
.a10e .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a10e .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a10e .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a10e .c{ fill:var(--text-faint); font-size:12.5px; }
.a10e .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a10e .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a10e .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a10e .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a10e-a); }
.a10e .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a10e-a); marker-start:url(#a10e-s); }
.a10e .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a10e-g); }
.a10e .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a10e-a); }
.a10e .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a10e .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a10e .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a10e .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a10e .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a10e .ks-blue{ fill:#185FA5; font-size:13px; }
.a10e .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a10e .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10e .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a10e .kb-blue, :root[data-theme="dark"] .a10e .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a10e .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a10e .kh-blue{ fill:#85B7EB; }
.a10e .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a10e-blue); }
.a10e .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10e-blue); }
.a10e .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a10e .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a10e .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a10e .ks-teal{ fill:#0F6E56; font-size:13px; }
.a10e .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a10e .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10e .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a10e .kb-teal, :root[data-theme="dark"] .a10e .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a10e .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a10e .kh-teal{ fill:#5DCAA5; }
.a10e .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a10e-teal); }
.a10e .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10e-teal); }
.a10e .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a10e .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a10e .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a10e .ks-amber{ fill:#854F0B; font-size:13px; }
.a10e .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a10e .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10e .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a10e .kb-amber, :root[data-theme="dark"] .a10e .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a10e .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a10e .kh-amber{ fill:#EF9F27; }
.a10e .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a10e-amber); }
.a10e .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10e-amber); }
.a10e .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a10e .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a10e .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a10e .ks-red{ fill:#A32D2D; font-size:13px; }
.a10e .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a10e .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10e .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a10e .kb-red, :root[data-theme="dark"] .a10e .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a10e .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a10e .kh-red{ fill:#F09595; }
.a10e .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a10e-red); }
.a10e .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10e-red); }
.a10e .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
</style>
<defs><marker id="a10e-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a10e-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a10e-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a10e-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a10e-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a10e-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a10e-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker></defs>
<g class="a10e">
<path d="M180 60 L 200 200 L 320 200 L 340 60" class="ln-teal"/>
<circle cx="222" cy="182" r="12" class="k-amber"/>
<circle cx="260" cy="182" r="12" class="k-amber"/>
<circle cx="298" cy="182" r="12" class="k-amber"/>
<circle cx="222" cy="152" r="12" class="k-amber"/>
<circle cx="260" cy="152" r="12" class="k-amber"/>
<circle cx="298" cy="152" r="12" class="k-amber"/>
<circle cx="260" cy="30" r="9" class="k-amber"/>
<line x1="260" y1="42" x2="260" y2="70" class="ar-amber"/>
<text x="360" y="34" text-anchor="start" class="kh-amber">refill: 5 tokens per second</text>
<text x="360" y="104" text-anchor="start" class="kh-teal">capacity: 10 (the burst size)</text>
<rect x="400" y="140" width="140" height="40" rx="7" class="k-blue"/>
<text x="470.0" y="164.5" text-anchor="middle" class="kb-blue">request</text>
<line x1="398" y1="160" x2="324" y2="160" class="ar-blue"/>
<text x="600" y="166" text-anchor="middle" class="s">takes 1 token</text>
<rect x="20" y="210" width="680" height="40" rx="7" class="k-red"/>
<text x="360.0" y="234.5" text-anchor="middle" class="kb-red">bucket empty: 429 Too Many Requests, Retry-After: 1</text>
</g>
</svg>
<figcaption>Bursts are allowed; sustained overload is not. The same idea limits per user, per API key, or per IP address.</figcaption>
</figure>

Rate limits protect the API from overload and from any one client using more than its share (OWASP API4). The **token bucket** algorithm is the most common: each client has a bucket that refills at a steady rate; each request spends a token; when the bucket is empty, requests are rejected. `library_perf.py` implements it as middleware on `/limited/*`, keyed by API key or IP address, with a burst of 10 and a refill rate of 5 per second:

```bash
for i in $(seq 1 13); do curl -s -o /dev/null -D - http://127.0.0.1:8000/limited/books | grep -iE "^HTTP|remaining|retry-after" | tr -d '\r' | tr '\n' ' '; echo; done
```

```text
HTTP/1.1 200 OK x-ratelimit-remaining: 9
HTTP/1.1 200 OK x-ratelimit-remaining: 8
...
HTTP/1.1 200 OK x-ratelimit-remaining: 0
HTTP/1.1 429 Too Many Requests retry-after: 1 x-ratelimit-remaining: 0
HTTP/1.1 429 Too Many Requests retry-after: 1 x-ratelimit-remaining: 0
```

**429 Too Many Requests** with a **Retry-After** header tells the client when to try again. The `X-RateLimit-Limit` and `X-RateLimit-Remaining` headers are a widespread convention that lets well-behaved clients slow down before hitting the limit; the IETF is standardising similar `RateLimit` headers. In production, rate limiting usually lives in the API gateway (Chapter 11) and keeps its counters in a shared store such as Redis, so that every server instance sees the same buckets.

## Retries, done safely

Networks fail. A client that never retries is fragile; a client that retries instantly and forever turns a brief outage into a flood. Good retry logic:

- retries only **transient** failures: timeouts, connection errors, `429`, `502`, `503`, `504`;
- never retries most `4xx` errors, which will fail again;
- waits with **exponential backoff and jitter**, and honours `Retry-After`;
- gives up after a few attempts.

<figure class="diagram">
<svg viewBox="0 0 720 250" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Exponential backoff with full jitter. After each failed attempt the client waits a random time between zero and a cap that doubles each time: up to 0.5, 1, 2 and 4 seconds. Randomness spreads clients out so they do not all retry at the same moment." xmlns="http://www.w3.org/2000/svg">
<style>
.a10f{ font-family:var(--sans),sans-serif; }
.a10f .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a10f .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a10f .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a10f .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a10f .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a10f .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a10f .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a10f .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a10f .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a10f .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a10f .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a10f .s{ fill:var(--text-dim); font-size:13px; }
.a10f .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a10f .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a10f .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a10f .c{ fill:var(--text-faint); font-size:12.5px; }
.a10f .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a10f .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a10f .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a10f .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a10f-a); }
.a10f .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a10f-a); marker-start:url(#a10f-s); }
.a10f .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a10f-g); }
.a10f .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a10f-a); }
.a10f .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a10f .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a10f .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a10f .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a10f .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a10f .ks-teal{ fill:#0F6E56; font-size:13px; }
.a10f .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a10f .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10f .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a10f .kb-teal, :root[data-theme="dark"] .a10f .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a10f .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a10f .kh-teal{ fill:#5DCAA5; }
.a10f .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a10f-teal); }
.a10f .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10f-teal); }
.a10f .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
</style>
<defs><marker id="a10f-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a10f-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a10f-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a10f-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker></defs>
<g class="a10f">
<text x="20" y="52" text-anchor="start" class="s">retry 1</text>
<rect x="100" y="36" width="70.0" height="26" rx="3" class="pnl"/>
<circle cx="110.5" cy="49" r="5" class="k-teal"/>
<circle cx="135.0" cy="49" r="5" class="k-teal"/>
<circle cx="159.5" cy="49" r="5" class="k-teal"/>
<text x="180.0" y="54" text-anchor="start" class="kh-teal">0 to 0.5 s</text>
<text x="20" y="98" text-anchor="start" class="s">retry 2</text>
<rect x="100" y="82" width="140" height="26" rx="3" class="pnl"/>
<circle cx="111.2" cy="95" r="5" class="k-teal"/>
<circle cx="142.0" cy="95" r="5" class="k-teal"/>
<circle cx="177.0" cy="95" r="5" class="k-teal"/>
<circle cx="219.0" cy="95" r="5" class="k-teal"/>
<text x="250" y="100" text-anchor="start" class="kh-teal">0 to 1 s</text>
<text x="20" y="144" text-anchor="start" class="s">retry 3</text>
<rect x="100" y="128" width="280" height="26" rx="3" class="pnl"/>
<circle cx="114.0" cy="141" r="5" class="k-teal"/>
<circle cx="161.6" cy="141" r="5" class="k-teal"/>
<circle cx="212.0" cy="141" r="5" class="k-teal"/>
<circle cx="276.4" cy="141" r="5" class="k-teal"/>
<circle cx="346.4" cy="141" r="5" class="k-teal"/>
<text x="390" y="146" text-anchor="start" class="kh-teal">0 to 2 s</text>
<text x="20" y="190" text-anchor="start" class="s">retry 4</text>
<rect x="100" y="174" width="560" height="26" rx="3" class="pnl"/>
<circle cx="156.0" cy="187" r="5" class="k-teal"/>
<circle cx="251.20000000000002" cy="187" r="5" class="k-teal"/>
<circle cx="357.6" cy="187" r="5" class="k-teal"/>
<circle cx="436.0" cy="187" r="5" class="k-teal"/>
<circle cx="542.4000000000001" cy="187" r="5" class="k-teal"/>
<circle cx="632.0" cy="187" r="5" class="k-teal"/>
<text x="670" y="192" text-anchor="start" class="kh-teal">0 to 4 s</text>
<text x="360" y="236" text-anchor="middle" class="c">each dot is a client: jitter spreads them out instead of a synchronised stampede</text>
</g>
</svg>
<figcaption>Retry only what is safe to retry, cap the number of attempts, and prefer the server's Retry-After when it sends one.</figcaption>
</figure>

```python
def call_with_retries(method: str, url: str, attempts: int = 5, **kwargs) -> requests.Response:
    """Retry on timeouts and retryable status codes, with exponential backoff and full jitter."""
    for attempt in range(attempts):
        try:
            resp = requests.request(method, url, timeout=(3, 10), **kwargs)
        except (requests.ConnectionError, requests.Timeout) as exc:
            resp, reason = None, type(exc).__name__
        else:
            if resp.status_code not in RETRYABLE:
                return resp
            reason = resp.status_code
        if attempt == attempts - 1:
            break
        retry_after = resp.headers.get("Retry-After") if resp is not None else None
        delay = float(retry_after) if retry_after and retry_after.isdigit() else random.uniform(0, 0.5 * 2**attempt)
        print(f"  attempt {attempt + 1} failed ({reason}); waiting {delay:.2f}s")
        time.sleep(delay)
    raise RuntimeError(f"giving up on {method} {url}")
```

Running `python retry_client.py` makes 15 quick calls against a burst of 10. The eleventh is rate-limited; the client waits the second the server asked for, and carries on:

```text
9 200 remaining: 1
10 200 remaining: 0
  attempt 1 failed (429); waiting 1.00s
11 200 remaining: 4
12 200 remaining: 3
```

## Idempotency keys

Retrying a `GET` is harmless. Retrying a `POST` is not: if the first request created an order and only the **response** was lost, a retry creates a second order and charges the customer twice.

<figure class="diagram">
<svg viewBox="0 0 720 290" style="width:100%;height:auto;max-width:720px" role="img" aria-label="An idempotency key makes a POST safe to retry. The client sends POST /orders with Idempotency-Key k1. The server creates the order, but the response is lost. The client retries with the same key. The server finds k1, does not create a second order, and replays the stored response." xmlns="http://www.w3.org/2000/svg">
<style>
.a10g{ font-family:var(--sans),sans-serif; }
.a10g .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a10g .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a10g .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a10g .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a10g .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a10g .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a10g .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a10g .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a10g .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a10g .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a10g .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a10g .s{ fill:var(--text-dim); font-size:13px; }
.a10g .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a10g .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a10g .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a10g .c{ fill:var(--text-faint); font-size:12.5px; }
.a10g .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a10g .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a10g .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a10g .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a10g-a); }
.a10g .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a10g-a); marker-start:url(#a10g-s); }
.a10g .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a10g-g); }
.a10g .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a10g-a); }
.a10g .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a10g .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a10g .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a10g .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a10g .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a10g .ks-blue{ fill:#185FA5; font-size:13px; }
.a10g .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a10g .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10g .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a10g .kb-blue, :root[data-theme="dark"] .a10g .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a10g .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a10g .kh-blue{ fill:#85B7EB; }
.a10g .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a10g-blue); }
.a10g .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10g-blue); }
.a10g .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a10g .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a10g .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a10g .ks-teal{ fill:#0F6E56; font-size:13px; }
.a10g .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a10g .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10g .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a10g .kb-teal, :root[data-theme="dark"] .a10g .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a10g .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a10g .kh-teal{ fill:#5DCAA5; }
.a10g .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a10g-teal); }
.a10g .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10g-teal); }
.a10g .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a10g .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a10g .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a10g .ks-purple{ fill:#534AB7; font-size:13px; }
.a10g .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a10g .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10g .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a10g .kb-purple, :root[data-theme="dark"] .a10g .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a10g .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a10g .kh-purple{ fill:#AFA9EC; }
.a10g .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a10g-purple); }
.a10g .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10g-purple); }
.a10g .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a10g .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a10g .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a10g .ks-green{ fill:#3B6D11; font-size:13px; }
.a10g .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a10g .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10g .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a10g .kb-green, :root[data-theme="dark"] .a10g .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a10g .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a10g .kh-green{ fill:#97C459; }
.a10g .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a10g-green); }
.a10g .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10g-green); }
.a10g .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a10g .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a10g .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a10g .ks-red{ fill:#A32D2D; font-size:13px; }
.a10g .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a10g .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10g .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a10g .kb-red, :root[data-theme="dark"] .a10g .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a10g .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a10g .kh-red{ fill:#F09595; }
.a10g .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a10g-red); }
.a10g .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10g-red); }
.a10g .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
</style>
<defs><marker id="a10g-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a10g-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a10g-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a10g-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a10g-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a10g-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a10g-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a10g-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker></defs>
<g class="a10g">
<rect x="55" y="16" width="150" height="40" rx="7" class="k-blue"/>
<text x="130.0" y="40.5" text-anchor="middle" class="kb-blue">client</text>
<line x1="130" y1="56" x2="130" y2="280" class="gd"/>
<rect x="305" y="16" width="150" height="40" rx="7" class="k-teal"/>
<text x="380.0" y="40.5" text-anchor="middle" class="kb-teal">server</text>
<line x1="380" y1="56" x2="380" y2="280" class="gd"/>
<rect x="535" y="16" width="150" height="40" rx="7" class="k-purple"/>
<text x="610.0" y="40.5" text-anchor="middle" class="kb-purple">store</text>
<line x1="610" y1="56" x2="610" y2="280" class="gd"/>
<line x1="132" y1="90" x2="378" y2="90" class="ar-blue"/>
<text x="255.0" y="83" text-anchor="middle" class="s">POST /orders, key k1</text>
<line x1="382" y1="122" x2="608" y2="122" class="ar-teal"/>
<text x="495.0" y="115" text-anchor="middle" class="s">save order + k1</text>
<line x1="132" y1="190" x2="378" y2="190" class="ar-blue"/>
<text x="255.0" y="183" text-anchor="middle" class="s">retry: same key k1</text>
<line x1="382" y1="222" x2="608" y2="222" class="ar-teal"/>
<text x="495.0" y="215" text-anchor="middle" class="s">k1 seen</text>
<line x1="378" y1="262" x2="132" y2="262" class="ar-green"/>
<text x="255.0" y="255" text-anchor="middle" class="s">201, Idempotent-Replayed</text>
<line x1="380" y1="152" x2="300" y2="152" class="ar-red"/>
<text x="250" y="157" text-anchor="end" class="kh-red">lost</text>
<text x="500" y="252" text-anchor="middle" class="kh-green">no second order</text>
</g>
</svg>
<figcaption>The client generates a unique key per operation and reuses it for every retry of that operation.</figcaption>
</figure>

The fix, popularised by payment APIs and being standardised by the IETF as the `Idempotency-Key` header, is for the client to send a unique key with each operation and reuse it for every retry. The server remembers the key with the response and, on a repeat, returns the stored response instead of acting again:

```python
@app.post("/orders", status_code=201)
def create_order(order: OrderIn, response: Response, idempotency_key: str = Header()):
    fingerprint = hashlib.sha256(order.model_dump_json().encode()).hexdigest()
    if idempotency_key in idempotency:
        seen_fp, stored = idempotency[idempotency_key]
        if seen_fp != fingerprint:
            raise HTTPException(422, "Idempotency-Key reused with a different request")
        response.headers["Idempotent-Replayed"] = "true"
        return stored                              # same answer, no second order
    new = {"id": str(uuid.uuid4()), **order.model_dump()}
    orders[new["id"]] = new
    idempotency[idempotency_key] = (fingerprint, new)
    return new
```

Sending the same request twice with `Idempotency-Key: 7f9c-order-1` returns the same order ID both times, the second with `idempotent-replayed: true`. Reusing the key with a different body is an error, `422`. A real implementation stores keys in the database, in the same transaction as the order, and expires them after a day or so.

## Long-running operations

<figure class="diagram">
<svg viewBox="0 0 720 260" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Long-running work with 202 Accepted. The client posts a request; the server queues a job and responds immediately with 202, a Location header for the job, and Retry-After. The client polls the job URL until its status is done and then reads the result." xmlns="http://www.w3.org/2000/svg">
<style>
.a10h{ font-family:var(--sans),sans-serif; }
.a10h .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a10h .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a10h .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a10h .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a10h .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a10h .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a10h .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a10h .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a10h .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a10h .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a10h .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a10h .s{ fill:var(--text-dim); font-size:13px; }
.a10h .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a10h .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a10h .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a10h .c{ fill:var(--text-faint); font-size:12.5px; }
.a10h .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a10h .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a10h .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a10h .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a10h-a); }
.a10h .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a10h-a); marker-start:url(#a10h-s); }
.a10h .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a10h-g); }
.a10h .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a10h-a); }
.a10h .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a10h .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a10h .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a10h .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a10h .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a10h .ks-blue{ fill:#185FA5; font-size:13px; }
.a10h .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a10h .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10h .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a10h .kb-blue, :root[data-theme="dark"] .a10h .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a10h .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a10h .kh-blue{ fill:#85B7EB; }
.a10h .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a10h-blue); }
.a10h .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10h-blue); }
.a10h .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a10h .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a10h .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a10h .ks-teal{ fill:#0F6E56; font-size:13px; }
.a10h .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a10h .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10h .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a10h .kb-teal, :root[data-theme="dark"] .a10h .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a10h .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a10h .kh-teal{ fill:#5DCAA5; }
.a10h .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a10h-teal); }
.a10h .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10h-teal); }
.a10h .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a10h .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a10h .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a10h .ks-amber{ fill:#854F0B; font-size:13px; }
.a10h .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a10h .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10h .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a10h .kb-amber, :root[data-theme="dark"] .a10h .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a10h .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a10h .kh-amber{ fill:#EF9F27; }
.a10h .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a10h-amber); }
.a10h .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10h-amber); }
.a10h .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a10h .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a10h .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a10h .ks-green{ fill:#3B6D11; font-size:13px; }
.a10h .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a10h .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a10h .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a10h .kb-green, :root[data-theme="dark"] .a10h .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a10h .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a10h .kh-green{ fill:#97C459; }
.a10h .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a10h-green); }
.a10h .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a10h-green); }
.a10h .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
</style>
<defs><marker id="a10h-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a10h-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a10h-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a10h-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a10h-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a10h-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a10h-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker></defs>
<g class="a10h">
<rect x="55" y="16" width="150" height="40" rx="7" class="k-blue"/>
<text x="130.0" y="40.5" text-anchor="middle" class="kb-blue">client</text>
<line x1="130" y1="56" x2="130" y2="250" class="gd"/>
<rect x="305" y="16" width="150" height="40" rx="7" class="k-teal"/>
<text x="380.0" y="40.5" text-anchor="middle" class="kb-teal">API</text>
<line x1="380" y1="56" x2="380" y2="250" class="gd"/>
<rect x="535" y="16" width="150" height="40" rx="7" class="k-amber"/>
<text x="610.0" y="40.5" text-anchor="middle" class="kb-amber">worker</text>
<line x1="610" y1="56" x2="610" y2="250" class="gd"/>
<line x1="132" y1="90" x2="378" y2="90" class="ar-blue"/>
<text x="255.0" y="83" text-anchor="middle" class="s">POST /reports</text>
<line x1="382" y1="118" x2="608" y2="118" class="ar-teal"/>
<text x="495.0" y="111" text-anchor="middle" class="s">queue job</text>
<line x1="378" y1="146" x2="132" y2="146" class="ar-green"/>
<text x="255.0" y="139" text-anchor="middle" class="s">202, Location: /reports/98cd</text>
<line x1="132" y1="186" x2="378" y2="186" class="ar-blue"/>
<text x="255.0" y="179" text-anchor="middle" class="s">GET /reports/98cd</text>
<line x1="378" y1="214" x2="132" y2="214" class="ar-teal"/>
<text x="255.0" y="207" text-anchor="middle" class="s">{"status": "running"}</text>
<line x1="378" y1="242" x2="132" y2="242" class="ar-green"/>
<text x="255.0" y="235" text-anchor="middle" class="s">{"status": "done", "result"}</text>
<line x1="610" y1="130" x2="610" y2="230" class="ln-amber"/>
</g>
</svg>
<figcaption>Never hold an HTTP request open for minutes. Hand back a ticket instead; a webhook (Chapter 12) can replace the polling.</figcaption>
</figure>

Some work takes seconds or minutes: generating a report, transcoding a video. Holding the HTTP request open that long ties up resources and runs into proxy timeouts. Instead, accept the job and return immediately with **202 Accepted** and a `Location` to check on it:

```bash
curl -i -X POST http://127.0.0.1:8000/reports
```

```text
HTTP/1.1 202 Accepted
location: /reports/98cd3012
retry-after: 1
{"id":"98cd3012","status":"queued"}
```

The client polls the `Location` URL until the status is `done`. `retry_client.py` shows the loop:

```text
job: running
job: running
job: done
result: {'books': 2}
```

The demo uses FastAPI's background tasks, which run in the same process. Real systems hand jobs to a queue (Celery, RQ, a cloud queue service) processed by separate workers, so work survives restarts and scales independently.

## Summary

- **Measure** latency as percentiles; reuse connections; send less; watch the database.
- Use **Cache-Control** and **ETag**; answer **304** to conditional requests.
- Use **If-Match** (412 and 428) to prevent **lost updates**.
- **Rate-limit** with a token bucket; answer **429** with **Retry-After**.
- Clients retry only transient failures, with **exponential backoff and jitter**, and **timeouts** always.
- **Idempotency keys** make `POST` safe to retry.
- Return **202 Accepted** and a status URL for **long-running** work.
