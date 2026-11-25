# Chapter 8: Authentication and Authorization

So far, anyone who can reach the Library API can change it. Real APIs need to know **who** is calling and decide **what** each caller may do. This chapter covers the common mechanisms, from API keys to OAuth 2.0, and implements two of them in `library_auth.py`.

## Two questions

<figure class="diagram">
<svg viewBox="0 0 720 250" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Authentication answers who is calling; authorization answers whether that caller may do this. A request with missing or invalid credentials gets 401 Unauthorized; a request with valid credentials but without permission gets 403 Forbidden; only a request that passes both checks reaches the handler." xmlns="http://www.w3.org/2000/svg">
<style>
.a8a{ font-family:var(--sans),sans-serif; }
.a8a .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a8a .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a8a .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a8a .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a8a .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a8a .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a8a .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a8a .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a8a .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a8a .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a8a .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a8a .s{ fill:var(--text-dim); font-size:13px; }
.a8a .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a8a .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a8a .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a8a .c{ fill:var(--text-faint); font-size:12.5px; }
.a8a .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a8a .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a8a .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a8a .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a8a-a); }
.a8a .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a8a-a); marker-start:url(#a8a-s); }
.a8a .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a8a-g); }
.a8a .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a8a-a); }
.a8a .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a8a .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a8a .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a8a .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a8a .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a8a .ks-blue{ fill:#185FA5; font-size:13px; }
.a8a .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a8a .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8a .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a8a .kb-blue, :root[data-theme="dark"] .a8a .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a8a .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a8a .kh-blue{ fill:#85B7EB; }
.a8a .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a8a-blue); }
.a8a .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8a-blue); }
.a8a .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a8a .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a8a .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a8a .ks-teal{ fill:#0F6E56; font-size:13px; }
.a8a .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a8a .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8a .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a8a .kb-teal, :root[data-theme="dark"] .a8a .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a8a .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a8a .kh-teal{ fill:#5DCAA5; }
.a8a .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a8a-teal); }
.a8a .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8a-teal); }
.a8a .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a8a .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a8a .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a8a .ks-amber{ fill:#854F0B; font-size:13px; }
.a8a .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a8a .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8a .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a8a .kb-amber, :root[data-theme="dark"] .a8a .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a8a .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a8a .kh-amber{ fill:#EF9F27; }
.a8a .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a8a-amber); }
.a8a .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8a-amber); }
.a8a .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a8a .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a8a .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a8a .ks-purple{ fill:#534AB7; font-size:13px; }
.a8a .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a8a .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8a .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a8a .kb-purple, :root[data-theme="dark"] .a8a .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a8a .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a8a .kh-purple{ fill:#AFA9EC; }
.a8a .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a8a-purple); }
.a8a .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8a-purple); }
.a8a .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a8a .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a8a .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a8a .ks-green{ fill:#3B6D11; font-size:13px; }
.a8a .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a8a .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8a .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a8a .kb-green, :root[data-theme="dark"] .a8a .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a8a .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a8a .kh-green{ fill:#97C459; }
.a8a .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a8a-green); }
.a8a .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8a-green); }
.a8a .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a8a .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a8a .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a8a .ks-red{ fill:#A32D2D; font-size:13px; }
.a8a .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a8a .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8a .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a8a .kb-red, :root[data-theme="dark"] .a8a .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a8a .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a8a .kh-red{ fill:#F09595; }
.a8a .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a8a-red); }
.a8a .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8a-red); }
.a8a .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
</style>
<defs><marker id="a8a-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a8a-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a8a-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a8a-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a8a-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a8a-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a8a-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a8a-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a8a-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker></defs>
<g class="a8a">
<rect x="20" y="90" width="130" height="56" rx="7" class="k-blue"/>
<text x="85.0" y="113.5" text-anchor="middle" class="kb-blue">request</text>
<text x="85.0" y="131.5" text-anchor="middle" class="ks-blue">+ credentials</text>
<rect x="200" y="80" width="160" height="76" rx="7" class="k-amber"/>
<text x="280.0" y="113.5" text-anchor="middle" class="kb-amber">authentication</text>
<text x="280.0" y="131.5" text-anchor="middle" class="ks-amber">who are you?</text>
<rect x="410" y="80" width="160" height="76" rx="7" class="k-purple"/>
<text x="490.0" y="113.5" text-anchor="middle" class="kb-purple">authorization</text>
<text x="490.0" y="131.5" text-anchor="middle" class="ks-purple">may you do this?</text>
<rect x="610" y="90" width="90" height="56" rx="7" class="k-teal"/>
<text x="655.0" y="122.5" text-anchor="middle" class="kb-teal">handler</text>
<line x1="152" y1="118" x2="198" y2="118" class="ar"/>
<line x1="362" y1="118" x2="408" y2="118" class="ar-green"/>
<line x1="572" y1="118" x2="608" y2="118" class="ar-green"/>
<line x1="280" y1="158" x2="280" y2="196" class="ar-red"/>
<rect x="200" y="198" width="160" height="40" rx="7" class="k-red"/>
<text x="280.0" y="222.5" text-anchor="middle" class="kb-red">401 Unauthorized</text>
<line x1="490" y1="158" x2="490" y2="196" class="ar-red"/>
<rect x="410" y="198" width="160" height="40" rx="7" class="k-red"/>
<text x="490.0" y="222.5" text-anchor="middle" class="kb-red">403 Forbidden</text>
<text x="280" y="40" text-anchor="middle" class="kh-amber">token missing, expired, forged</text>
<text x="490" y="40" text-anchor="middle" class="kh-purple">valid token, wrong scope or role</text>
</g>
</svg>
<figcaption>Two different questions, two different status codes. 401 means try again with credentials; 403 means do not try again.</figcaption>
</figure>

- **Authentication** (often shortened to *authn*) establishes identity: this request comes from Bob, or from the partner bookshop's application.
- **Authorization** (*authz*) decides whether that identity may perform this action on this resource.

The status codes follow the split. **401 Unauthorized**, despite its name, means *unauthenticated*: credentials are missing or invalid, and the response includes a `WWW-Authenticate` header saying how to authenticate. **403 Forbidden** means the server knows who you are and the answer is no.

## Ways to prove identity

<figure class="diagram">
<svg viewBox="0 0 720 300" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Four common ways for a client to prove who it is: an API key in a header identifies an application; HTTP Basic sends a username and password on every request; a session cookie refers to state stored on the server; a bearer token carries signed claims that the server can verify without a lookup." xmlns="http://www.w3.org/2000/svg">
<style>
.a8b{ font-family:var(--sans),sans-serif; }
.a8b .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a8b .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a8b .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a8b .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a8b .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a8b .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a8b .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a8b .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a8b .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a8b .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a8b .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a8b .s{ fill:var(--text-dim); font-size:13px; }
.a8b .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a8b .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a8b .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a8b .c{ fill:var(--text-faint); font-size:12.5px; }
.a8b .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a8b .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a8b .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a8b .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a8b-a); }
.a8b .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a8b-a); marker-start:url(#a8b-s); }
.a8b .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a8b-g); }
.a8b .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a8b-a); }
.a8b .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a8b .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a8b .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a8b .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a8b .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a8b .ks-amber{ fill:#854F0B; font-size:13px; }
.a8b .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a8b .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8b .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a8b .kb-amber, :root[data-theme="dark"] .a8b .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a8b .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a8b .kh-amber{ fill:#EF9F27; }
.a8b .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a8b-amber); }
.a8b .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8b-amber); }
.a8b .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a8b .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a8b .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a8b .ks-purple{ fill:#534AB7; font-size:13px; }
.a8b .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a8b .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8b .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a8b .kb-purple, :root[data-theme="dark"] .a8b .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a8b .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a8b .kh-purple{ fill:#AFA9EC; }
.a8b .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a8b-purple); }
.a8b .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8b-purple); }
.a8b .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a8b .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a8b .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a8b .ks-green{ fill:#3B6D11; font-size:13px; }
.a8b .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a8b .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8b .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a8b .kb-green, :root[data-theme="dark"] .a8b .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a8b .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a8b .kh-green{ fill:#97C459; }
.a8b .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a8b-green); }
.a8b .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8b-green); }
.a8b .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a8b .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a8b .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a8b .ks-red{ fill:#A32D2D; font-size:13px; }
.a8b .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a8b .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8b .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a8b .kb-red, :root[data-theme="dark"] .a8b .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a8b .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a8b .kh-red{ fill:#F09595; }
.a8b .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a8b-red); }
.a8b .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8b-red); }
.a8b .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
</style>
<defs><marker id="a8b-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a8b-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a8b-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a8b-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a8b-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a8b-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a8b-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker></defs>
<g class="a8b">
<rect x="20" y="16" width="130" height="56" rx="7" class="k-amber"/>
<text x="85.0" y="48.5" text-anchor="middle" class="kb-amber">API key</text>
<rect x="162" y="16" width="310" height="56" rx="6" class="pnl"/>
<text x="317.0" y="48.5" text-anchor="middle" class="m">X-API-Key: demo-key-123</text>
<text x="488" y="49" text-anchor="start" class="kh-amber">identifies an app, not a user</text>
<rect x="20" y="86" width="130" height="56" rx="7" class="k-red"/>
<text x="85.0" y="118.5" text-anchor="middle" class="kb-red">HTTP Basic</text>
<rect x="162" y="86" width="310" height="56" rx="6" class="pnl"/>
<text x="317.0" y="118.5" text-anchor="middle" class="m">Authorization: Basic YWRhOmxvdmVsYWNl</text>
<text x="488" y="119" text-anchor="start" class="kh-red">password every time: avoid</text>
<rect x="20" y="156" width="130" height="56" rx="7" class="k-purple"/>
<text x="85.0" y="188.5" text-anchor="middle" class="kb-purple">session cookie</text>
<rect x="162" y="156" width="310" height="56" rx="6" class="pnl"/>
<text x="317.0" y="188.5" text-anchor="middle" class="m">Cookie: session=8f3a...</text>
<text x="488" y="189" text-anchor="start" class="kh-purple">browser apps, server state</text>
<rect x="20" y="226" width="130" height="56" rx="7" class="k-green"/>
<text x="85.0" y="258.5" text-anchor="middle" class="kb-green">bearer token</text>
<rect x="162" y="226" width="310" height="56" rx="6" class="pnl"/>
<text x="317.0" y="258.5" text-anchor="middle" class="m">Authorization: Bearer eyJhbGci...</text>
<text x="488" y="259" text-anchor="start" class="kh-green">short-lived, scoped: APIs</text>
</g>
</svg>
<figcaption>All four ride in headers over HTTPS. Without TLS, every one of them can be stolen from the wire.</figcaption>
</figure>

| Scheme | How it works | Good for | Watch out for |
|---|---|---|---|
| **API key** | A long random string in a header | Identifying an application; usage quotas | Identifies an app, not a user; often leaked in code repositories |
| **HTTP Basic** | `base64(username:password)` on every request | Quick internal tools | Sends the password every time; base64 is not encryption |
| **Session cookie** | Server stores a session; browser sends its ID | Traditional browser applications | Needs CSRF protection; server-side state |
| **Bearer token** | A token in `Authorization: Bearer ...` | APIs, mobile apps, services | Must be short-lived and checked carefully |

Every one of them must travel over **HTTPS**. A credential sent over plain HTTP should be considered public.

## API keys

An API key is simple and widely used by public APIs to identify a client application and enforce quotas. `library_auth.py` checks a key sent in the `X-API-Key` header:

```python
# Store only hashes of API keys, never the keys themselves
API_KEYS = {sha256("demo-key-123"): "partner-bookshop"}

def require_api_key(key: str | None = Depends(api_key_header)) -> str:
    client = API_KEYS.get(sha256(key)) if key else None
    if client is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing or invalid API key",
                            headers={"WWW-Authenticate": 'ApiKey realm="library"'})
    return client

@app.get("/partner/books")
def partner_books(client: str = Depends(require_api_key)):
    return {"client": client, "books": BOOKS}
```

Storing a **hash** of each key, as with passwords, means a leaked database does not leak working keys. Run `fastapi dev library_auth.py` and try it:

```bash
curl -i http://127.0.0.1:8000/partner/books
curl -s http://127.0.0.1:8000/partner/books -H "X-API-Key: demo-key-123"
```

```text
HTTP/1.1 401 Unauthorized
www-authenticate: ApiKey realm="library"
{"detail":"Missing or invalid API key"}

{"client":"partner-bookshop","books":[{"id":1,"title":"Dune"},{"id":2,"title":"Emma"}]}
```

Keys belong in headers, never in URLs: URLs end up in server logs, browser history, and `Referer` headers.

## Bearer tokens and JWT

A **bearer token** works like a ticket: whoever holds it gets in. Tokens are issued after the user authenticates once, expire quickly, and carry **scopes** that limit what they allow. The most common format is the **JSON Web Token** (JWT, RFC 7519).

<figure class="diagram">
<svg viewBox="0 0 720 330" style="width:100%;height:auto;max-width:720px" role="img" aria-label="A JSON Web Token has three base64url parts separated by dots: a header naming the algorithm, a payload of claims such as issuer, audience, subject, issued-at, expiry and scope, and a signature computed over the first two parts with the server&#x27;s key. The payload is encoded, not encrypted: anyone can read it." xmlns="http://www.w3.org/2000/svg">
<style>
.a8c{ font-family:var(--sans),sans-serif; }
.a8c .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a8c .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a8c .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a8c .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a8c .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a8c .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a8c .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a8c .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a8c .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a8c .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a8c .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a8c .s{ fill:var(--text-dim); font-size:13px; }
.a8c .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a8c .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a8c .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a8c .c{ fill:var(--text-faint); font-size:12.5px; }
.a8c .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a8c .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a8c .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a8c .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a8c-a); }
.a8c .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a8c-a); marker-start:url(#a8c-s); }
.a8c .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a8c-g); }
.a8c .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a8c-a); }
.a8c .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a8c .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a8c .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a8c .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a8c .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a8c .ks-teal{ fill:#0F6E56; font-size:13px; }
.a8c .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a8c .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8c .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a8c .kb-teal, :root[data-theme="dark"] .a8c .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a8c .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a8c .kh-teal{ fill:#5DCAA5; }
.a8c .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a8c-teal); }
.a8c .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8c-teal); }
.a8c .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a8c .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a8c .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a8c .ks-amber{ fill:#854F0B; font-size:13px; }
.a8c .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a8c .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8c .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a8c .kb-amber, :root[data-theme="dark"] .a8c .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a8c .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a8c .kh-amber{ fill:#EF9F27; }
.a8c .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a8c-amber); }
.a8c .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8c-amber); }
.a8c .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a8c .k-coral{ fill:#FAECE7; stroke:#D85A30; stroke-width:1.6; }
.a8c .kb-coral{ fill:#712B13; font-size:13px; font-weight:700; }
.a8c .ks-coral{ fill:#993C1D; font-size:13px; }
.a8c .km-coral{ fill:#712B13; font-size:12.5px; font-family:var(--mono),monospace; }
.a8c .kh-coral{ fill:#993C1D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8c .k-coral{ fill:#712B13; stroke:#F0997B; }
:root[data-theme="dark"] .a8c .kb-coral, :root[data-theme="dark"] .a8c .km-coral{ fill:#FAECE7; }
:root[data-theme="dark"] .a8c .ks-coral{ fill:#F5C4B3; }
:root[data-theme="dark"] .a8c .kh-coral{ fill:#F0997B; }
.a8c .ar-coral{ stroke:#D85A30; stroke-width:2; fill:none; marker-end:url(#a8c-coral); }
.a8c .ad-coral{ stroke:#D85A30; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8c-coral); }
.a8c .ln-coral{ stroke:#D85A30; stroke-width:2; fill:none; }
.a8c .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a8c .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a8c .ks-purple{ fill:#534AB7; font-size:13px; }
.a8c .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a8c .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8c .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a8c .kb-purple, :root[data-theme="dark"] .a8c .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a8c .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a8c .kh-purple{ fill:#AFA9EC; }
.a8c .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a8c-purple); }
.a8c .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8c-purple); }
.a8c .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
</style>
<defs><marker id="a8c-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a8c-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a8c-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a8c-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a8c-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a8c-coral" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#D85A30"/></marker><marker id="a8c-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker></defs>
<g class="a8c">
<rect x="20" y="16" width="680" height="40" rx="5" class="pnl"/>
<text x="360.0" y="40.5" text-anchor="middle" class="m">eyJhbGciOi...J9  .  eyJpc3MiOi...In0  .  cdbFOe9F1A...WI</text>
<rect x="20" y="76" width="150" height="180" rx="8" class="k-coral"/>
<text x="34" y="98" text-anchor="start" class="kh-coral">header</text>
<text x="34" y="124" text-anchor="start" class="m">{"alg": "HS256",</text>
<text x="41.5" y="145" text-anchor="start" class="m">"typ": "JWT"}</text>
<rect x="182" y="76" width="340" height="180" rx="8" class="k-purple"/>
<text x="196" y="98" text-anchor="start" class="kh-purple">payload (claims)</text>
<text x="196" y="124" text-anchor="start" class="m">{"iss": "https://auth.library.example",</text>
<text x="203.5" y="145" text-anchor="start" class="m">"aud": "library-api",</text>
<text x="203.5" y="166" text-anchor="start" class="m">"sub": "bob",</text>
<text x="203.5" y="187" text-anchor="start" class="m">"iat": 1794725267,</text>
<text x="203.5" y="208" text-anchor="start" class="m">"exp": 1794726167,</text>
<text x="203.5" y="229" text-anchor="start" class="m">"scope": "books:read"}</text>
<rect x="534" y="76" width="166" height="180" rx="8" class="k-teal"/>
<text x="548" y="98" text-anchor="start" class="kh-teal">signature</text>
<text x="548" y="124" text-anchor="start" class="m">HMAC-SHA256(</text>
<text x="563.0" y="145" text-anchor="start" class="m">header.payload,</text>
<text x="563.0" y="166" text-anchor="start" class="m">secret key)</text>
<line x1="95" y1="58" x2="95" y2="74" class="ar-coral"/>
<line x1="352" y1="58" x2="352" y2="74" class="ar-purple"/>
<line x1="617" y1="58" x2="617" y2="74" class="ar-teal"/>
<rect x="20" y="272" width="680" height="46" rx="7" class="k-amber"/>
<text x="360.0" y="299.5" text-anchor="middle" class="kb-amber">encoded, not encrypted: never put secrets in the payload</text>
</g>
</svg>
<figcaption>Paste any token into a base64 decoder and the claims appear. The signature is what makes them trustworthy.</figcaption>
</figure>

Get a token for Bob from the demo's `/token` endpoint, then decode its first two parts with base64:

```bash
curl -s -X POST http://127.0.0.1:8000/token -d "username=bob&password=builder"
```

```text
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGgubGlicmFyeS5leGFtcGxlIiwiYXVkIjoibGlicmFyeS1hcGkiLCJzdWIiOiJib2IiLCJpYXQiOjE3OTQ3MjUyNjcsImV4cCI6MTc5NDcyNjE2Nywic2NvcGUiOiJib29rczpyZWFkIn0.cdbFOe9F1Acyp6i5pYEVkd1v1Dx-M6BHJwX93Fo7QWI",
 "token_type":"bearer","expires_in":900,"scope":"books:read"}

header:  {"alg":"HS256","typ":"JWT"}
payload: {"iss":"https://auth.library.example","aud":"library-api","sub":"bob",
          "iat":1794725267,"exp":1794726167,"scope":"books:read"}
```

The standard **claims** are `iss` (issuer), `aud` (audience: which API the token is for), `sub` (subject: who), `iat` (issued at), and `exp` (expiry), as Unix timestamps. `scope` lists the permissions. Anyone can read them, so a JWT must never contain secrets. What nobody can do without the key is **change** them, because the signature would no longer match.

The demo signs with **HS256**, an HMAC with a shared secret, which suits a single service that both issues and checks tokens. When a separate authorization server issues tokens for many APIs, it signs with a private key (**RS256** or **ES256**) and each API verifies with the public key, which it can download from the server's published key set (JWKS).

### Verifying a token

<figure class="diagram">
<svg viewBox="0 0 720 200" style="width:100%;height:auto;max-width:720px" role="img" aria-label="The checks a server performs on every bearer token before trusting it: the signature with a pinned algorithm, the expiry time, the issuer, the audience, and finally the scopes needed by this endpoint. Failing any of the first four gives 401; failing the scope check gives 403." xmlns="http://www.w3.org/2000/svg">
<style>
.a8d{ font-family:var(--sans),sans-serif; }
.a8d .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a8d .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a8d .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a8d .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a8d .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a8d .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a8d .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a8d .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a8d .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a8d .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a8d .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a8d .s{ fill:var(--text-dim); font-size:13px; }
.a8d .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a8d .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a8d .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a8d .c{ fill:var(--text-faint); font-size:12.5px; }
.a8d .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a8d .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a8d .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a8d .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a8d-a); }
.a8d .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a8d-a); marker-start:url(#a8d-s); }
.a8d .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a8d-g); }
.a8d .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a8d-a); }
.a8d .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a8d .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a8d .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a8d .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a8d .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a8d .ks-amber{ fill:#854F0B; font-size:13px; }
.a8d .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a8d .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8d .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a8d .kb-amber, :root[data-theme="dark"] .a8d .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a8d .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a8d .kh-amber{ fill:#EF9F27; }
.a8d .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a8d-amber); }
.a8d .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8d-amber); }
.a8d .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a8d .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a8d .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a8d .ks-purple{ fill:#534AB7; font-size:13px; }
.a8d .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a8d .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8d .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a8d .kb-purple, :root[data-theme="dark"] .a8d .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a8d .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a8d .kh-purple{ fill:#AFA9EC; }
.a8d .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a8d-purple); }
.a8d .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8d-purple); }
.a8d .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a8d .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a8d .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a8d .ks-red{ fill:#A32D2D; font-size:13px; }
.a8d .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a8d .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8d .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a8d .kb-red, :root[data-theme="dark"] .a8d .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a8d .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a8d .kh-red{ fill:#F09595; }
.a8d .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a8d-red); }
.a8d .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8d-red); }
.a8d .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
</style>
<defs><marker id="a8d-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a8d-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a8d-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a8d-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a8d-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a8d-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker></defs>
<g class="a8d">
<rect x="20" y="40" width="122" height="60" rx="7" class="k-amber"/>
<text x="81.0" y="65.5" text-anchor="middle" class="kb-amber">signature</text>
<text x="81.0" y="83.5" text-anchor="middle" class="ks-amber">algorithm pinned</text>
<rect x="158" y="40" width="122" height="60" rx="7" class="k-amber"/>
<text x="219.0" y="65.5" text-anchor="middle" class="kb-amber">exp</text>
<text x="219.0" y="83.5" text-anchor="middle" class="ks-amber">not expired</text>
<line x1="144" y1="70" x2="156" y2="70" class="ar"/>
<rect x="296" y="40" width="122" height="60" rx="7" class="k-amber"/>
<text x="357.0" y="65.5" text-anchor="middle" class="kb-amber">iss</text>
<text x="357.0" y="83.5" text-anchor="middle" class="ks-amber">our issuer</text>
<line x1="282" y1="70" x2="294" y2="70" class="ar"/>
<rect x="434" y="40" width="122" height="60" rx="7" class="k-amber"/>
<text x="495.0" y="65.5" text-anchor="middle" class="kb-amber">aud</text>
<text x="495.0" y="83.5" text-anchor="middle" class="ks-amber">meant for us</text>
<line x1="420" y1="70" x2="432" y2="70" class="ar"/>
<rect x="572" y="40" width="122" height="60" rx="7" class="k-purple"/>
<text x="633.0" y="65.5" text-anchor="middle" class="kb-purple">scope</text>
<text x="633.0" y="83.5" text-anchor="middle" class="ks-purple">has permission</text>
<line x1="558" y1="70" x2="570" y2="70" class="ar"/>
<rect x="20" y="120" width="536" height="10" rx="3" class="k-red"/>
<text x="288" y="156" text-anchor="middle" class="kh-red">any failure: 401 Unauthorized</text>
<rect x="572" y="120" width="122" height="10" rx="3" class="k-red"/>
<text x="633" y="156" text-anchor="middle" class="kh-red">403 Forbidden</text>
</g>
</svg>
<figcaption>A library such as PyJWT performs the first four in one call, but only if you pass it the algorithm, audience, and issuer.</figcaption>
</figure>

```python
def current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2)) -> dict:
    challenge = f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else "Bearer"
    try:
        claims = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],   # pin the algorithm
                            audience=AUDIENCE, issuer=ISSUER)
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired", headers={"WWW-Authenticate": challenge})
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token", headers={"WWW-Authenticate": challenge})
    have = set(claims.get("scope", "").split())
    missing = [s for s in security_scopes.scopes if s not in have]
    if missing:   # authenticated, but not allowed: 403, not 401
        raise HTTPException(403, f"Missing scope: {' '.join(missing)}",
                            headers={"WWW-Authenticate": challenge})
    return claims

@app.get("/books")
def list_books(user: dict = Security(current_user, scopes=["books:read"])):
    return BOOKS

@app.post("/books", status_code=201)
def add_book(book: dict, user: dict = Security(current_user, scopes=["books:write"])):
    ...
```

**Pin the algorithm.** Passing `algorithms=["HS256"]` stops the classic attacks where a forged token claims `"alg": "none"` or switches algorithms. Each endpoint declares the scopes it needs, and the dependency enforces them.

Bob's token has only `books:read`:

```bash
T=$(curl -s -X POST http://127.0.0.1:8000/token -d "username=bob&password=builder" | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/books -H "Authorization: Bearer $T"
curl -i -X POST http://127.0.0.1:8000/books -H "Authorization: Bearer $T" \
     -H "Content-Type: application/json" -d '{"title": "Kindred"}'
```

```text
200
HTTP/1.1 403 Forbidden
www-authenticate: Bearer scope="books:write"
{"detail":"Missing scope: books:write"}
```

Asking for more than you are allowed does not help: when Bob requests `scope=books:read books:write`, the server grants the intersection with his permissions, `books:read`. A token with its signature altered gets `401 Invalid token`.

### Expiry and refresh

The demo's tokens last **15 minutes**. A JWT cannot easily be revoked, since the API checks it without asking anyone, so a short lifetime limits the damage if one leaks. To avoid logging in every 15 minutes, OAuth issues a longer-lived **refresh token** alongside, which the client exchanges for a new access token at the authorization server, where it **can** be revoked.

## OAuth 2.0

The `/token` endpoint above takes a username and password directly. That is the OAuth 2.0 **password grant**, used here only because it fits in one file. It is a teaching shortcut: the client handles the user's password, which is exactly what OAuth was invented to avoid. **OAuth 2.1**, which consolidates a decade of security advice (RFC 9700, the OAuth 2.0 Security Best Current Practice), removes it.

OAuth 2.0 (RFC 6749) is a framework for **delegated authorization**: letting an application act on a user's behalf, with limited permissions, without ever seeing the user's password.

<figure class="diagram">
<svg viewBox="0 0 720 280" style="width:100%;height:auto;max-width:720px" role="img" aria-label="The four OAuth 2.0 roles: the resource owner (a user) grants a client application limited access; the authorization server authenticates the user and issues an access token to the client; the client presents the token to the resource server, which is the API." xmlns="http://www.w3.org/2000/svg">
<style>
.a8e{ font-family:var(--sans),sans-serif; }
.a8e .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a8e .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a8e .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a8e .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a8e .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a8e .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a8e .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a8e .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a8e .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a8e .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a8e .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a8e .s{ fill:var(--text-dim); font-size:13px; }
.a8e .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a8e .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a8e .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a8e .c{ fill:var(--text-faint); font-size:12.5px; }
.a8e .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a8e .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a8e .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a8e .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a8e-a); }
.a8e .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a8e-a); marker-start:url(#a8e-s); }
.a8e .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a8e-g); }
.a8e .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a8e-a); }
.a8e .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a8e .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a8e .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a8e .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a8e .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a8e .ks-blue{ fill:#185FA5; font-size:13px; }
.a8e .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a8e .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8e .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a8e .kb-blue, :root[data-theme="dark"] .a8e .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a8e .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a8e .kh-blue{ fill:#85B7EB; }
.a8e .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a8e-blue); }
.a8e .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8e-blue); }
.a8e .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a8e .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a8e .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a8e .ks-teal{ fill:#0F6E56; font-size:13px; }
.a8e .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a8e .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8e .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a8e .kb-teal, :root[data-theme="dark"] .a8e .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a8e .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a8e .kh-teal{ fill:#5DCAA5; }
.a8e .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a8e-teal); }
.a8e .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8e-teal); }
.a8e .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a8e .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a8e .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a8e .ks-amber{ fill:#854F0B; font-size:13px; }
.a8e .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a8e .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8e .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a8e .kb-amber, :root[data-theme="dark"] .a8e .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a8e .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a8e .kh-amber{ fill:#EF9F27; }
.a8e .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a8e-amber); }
.a8e .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8e-amber); }
.a8e .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
</style>
<defs><marker id="a8e-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a8e-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a8e-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a8e-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a8e-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a8e-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker></defs>
<g class="a8e">
<rect x="20" y="20" width="180" height="64" rx="7" class="k-blue"/>
<text x="110.0" y="47.5" text-anchor="middle" class="kb-blue">resource owner</text>
<text x="110.0" y="65.5" text-anchor="middle" class="ks-blue">the user</text>
<rect x="20" y="190" width="180" height="64" rx="7" class="k-blue"/>
<text x="110.0" y="217.5" text-anchor="middle" class="kb-blue">client</text>
<text x="110.0" y="235.5" text-anchor="middle" class="ks-blue">app wanting access</text>
<rect x="500" y="20" width="200" height="64" rx="7" class="k-amber"/>
<text x="600.0" y="47.5" text-anchor="middle" class="kb-amber">authorization server</text>
<text x="600.0" y="65.5" text-anchor="middle" class="ks-amber">logs in, issues tokens</text>
<rect x="500" y="190" width="200" height="64" rx="7" class="k-teal"/>
<text x="600.0" y="217.5" text-anchor="middle" class="kb-teal">resource server</text>
<text x="600.0" y="235.5" text-anchor="middle" class="ks-teal">the API</text>
<line x1="110" y1="86" x2="110" y2="188" class="ar-blue"/>
<text x="120" y="142" text-anchor="start" class="s">uses</text>
<line x1="202" y1="52" x2="498" y2="52" class="ar-blue"/>
<text x="350" y="44" text-anchor="middle" class="s">logs in, consents</text>
<path d="M498 70 C 380 110, 300 160, 204 200" class="ar-amber"/>
<text x="410" y="162" text-anchor="middle" class="kh-amber">access token</text>
<line x1="202" y1="230" x2="498" y2="230" class="ar-teal"/>
<text x="350" y="222" text-anchor="middle" class="s">Authorization: Bearer ...</text>
</g>
</svg>
<figcaption>The client never sees the user's password. It receives a token limited in scope and lifetime.</figcaption>
</figure>

### Authorization code with PKCE

The flow for any application acting for a user, whether a web app, a mobile app, or a single-page app, is the **authorization code flow with PKCE** (Proof Key for Code Exchange, RFC 7636).

<figure class="diagram">
<svg viewBox="0 0 720 420" style="width:100%;height:auto;max-width:720px" role="img" aria-label="The authorization code flow with PKCE. The client creates a random code verifier and sends its hash, the code challenge, when redirecting the browser to the authorization server. The user logs in and consents. The authorization server redirects back with a one-time code. The client exchanges the code plus the original verifier for tokens. The server checks that the verifier matches the challenge. The client then calls the API with the access token." xmlns="http://www.w3.org/2000/svg">
<style>
.a8f{ font-family:var(--sans),sans-serif; }
.a8f .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a8f .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a8f .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a8f .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a8f .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a8f .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a8f .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a8f .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a8f .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a8f .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a8f .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a8f .s{ fill:var(--text-dim); font-size:13px; }
.a8f .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a8f .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a8f .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a8f .c{ fill:var(--text-faint); font-size:12.5px; }
.a8f .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a8f .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a8f .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a8f .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a8f-a); }
.a8f .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a8f-a); marker-start:url(#a8f-s); }
.a8f .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a8f-g); }
.a8f .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a8f-a); }
.a8f .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a8f .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a8f .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a8f .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a8f .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a8f .ks-blue{ fill:#185FA5; font-size:13px; }
.a8f .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a8f .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8f .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a8f .kb-blue, :root[data-theme="dark"] .a8f .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a8f .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a8f .kh-blue{ fill:#85B7EB; }
.a8f .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a8f-blue); }
.a8f .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8f-blue); }
.a8f .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a8f .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a8f .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a8f .ks-teal{ fill:#0F6E56; font-size:13px; }
.a8f .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a8f .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8f .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a8f .kb-teal, :root[data-theme="dark"] .a8f .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a8f .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a8f .kh-teal{ fill:#5DCAA5; }
.a8f .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a8f-teal); }
.a8f .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8f-teal); }
.a8f .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a8f .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a8f .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a8f .ks-amber{ fill:#854F0B; font-size:13px; }
.a8f .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a8f .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8f .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a8f .kb-amber, :root[data-theme="dark"] .a8f .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a8f .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a8f .kh-amber{ fill:#EF9F27; }
.a8f .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a8f-amber); }
.a8f .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8f-amber); }
.a8f .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
</style>
<defs><marker id="a8f-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a8f-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a8f-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a8f-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a8f-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a8f-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker></defs>
<g class="a8f">
<rect x="5" y="16" width="150" height="40" rx="7" class="k-blue"/>
<text x="80.0" y="40.5" text-anchor="middle" class="kb-blue">browser / user</text>
<line x1="80" y1="56" x2="80" y2="410" class="gd"/>
<rect x="195" y="16" width="150" height="40" rx="7" class="k-blue"/>
<text x="270.0" y="40.5" text-anchor="middle" class="kb-blue">client app</text>
<line x1="270" y1="56" x2="270" y2="410" class="gd"/>
<rect x="385" y="16" width="150" height="40" rx="7" class="k-amber"/>
<text x="460.0" y="40.5" text-anchor="middle" class="kb-amber">auth server</text>
<line x1="460" y1="56" x2="460" y2="410" class="gd"/>
<rect x="555" y="16" width="150" height="40" rx="7" class="k-teal"/>
<text x="630.0" y="40.5" text-anchor="middle" class="kb-teal">API</text>
<line x1="630" y1="56" x2="630" y2="410" class="gd"/>
<line x1="272" y1="128" x2="458" y2="128" class="ar-blue"/>
<text x="365.0" y="121" text-anchor="middle" class="s">/authorize + challenge</text>
<line x1="82" y1="166" x2="458" y2="166" class="ar-blue"/>
<text x="175.0" y="159" text-anchor="middle" class="s">log in, consent</text>
<line x1="458" y1="204" x2="272" y2="204" class="ar-amber"/>
<text x="365.0" y="197" text-anchor="middle" class="s">?code=one-time</text>
<line x1="272" y1="252" x2="458" y2="252" class="ar-blue"/>
<text x="365.0" y="245" text-anchor="middle" class="s">code + verifier v</text>
<line x1="458" y1="290" x2="272" y2="290" class="ar-amber"/>
<text x="365.0" y="283" text-anchor="middle" class="s">access token</text>
<line x1="272" y1="338" x2="628" y2="338" class="ar-blue"/>
<text x="365.0" y="331" text-anchor="middle" class="s">Bearer token</text>
<line x1="628" y1="376" x2="272" y2="376" class="ar-teal"/>
<text x="545.0" y="369" text-anchor="middle" class="s">200 OK</text>
<text x="365" y="96" text-anchor="middle" class="kh-blue">random verifier v</text>
<text x="545" y="272" text-anchor="middle" class="kh-amber">SHA256(v) = challenge?</text>
</g>
</svg>
<figcaption>PKCE binds the code to the client that asked for it, so a stolen code is useless. OAuth 2.1 requires it for every client.</figcaption>
</figure>

1. The client generates a random **code verifier** and sends its SHA-256 hash, the **code challenge**, as it redirects the browser to the authorization server.
2. The user logs in **at the authorization server** and approves the requested scopes.
3. The authorization server redirects back to the client with a short-lived, one-time **authorization code**.
4. The client exchanges the code, together with the original verifier, for tokens. The server checks that the verifier hashes to the challenge.
5. The client calls the API with the access token.

An attacker who intercepts the code cannot use it without the verifier, which never left the client. OAuth 2.1 makes PKCE mandatory for all clients.

### Client credentials

<figure class="diagram">
<svg viewBox="0 0 720 200" style="width:100%;height:auto;max-width:720px" role="img" aria-label="The client credentials flow for machine-to-machine calls: a backend service authenticates to the authorization server with its own client id and secret, receives an access token, and calls the API with it. No user is involved." xmlns="http://www.w3.org/2000/svg">
<style>
.a8g{ font-family:var(--sans),sans-serif; }
.a8g .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a8g .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a8g .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a8g .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a8g .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a8g .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a8g .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a8g .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a8g .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a8g .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a8g .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a8g .s{ fill:var(--text-dim); font-size:13px; }
.a8g .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a8g .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a8g .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a8g .c{ fill:var(--text-faint); font-size:12.5px; }
.a8g .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a8g .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a8g .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a8g .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a8g-a); }
.a8g .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a8g-a); marker-start:url(#a8g-s); }
.a8g .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a8g-g); }
.a8g .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a8g-a); }
.a8g .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a8g .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a8g .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a8g .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a8g .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a8g .ks-blue{ fill:#185FA5; font-size:13px; }
.a8g .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a8g .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8g .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a8g .kb-blue, :root[data-theme="dark"] .a8g .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a8g .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a8g .kh-blue{ fill:#85B7EB; }
.a8g .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a8g-blue); }
.a8g .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8g-blue); }
.a8g .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a8g .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a8g .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a8g .ks-teal{ fill:#0F6E56; font-size:13px; }
.a8g .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a8g .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8g .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a8g .kb-teal, :root[data-theme="dark"] .a8g .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a8g .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a8g .kh-teal{ fill:#5DCAA5; }
.a8g .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a8g-teal); }
.a8g .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8g-teal); }
.a8g .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a8g .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a8g .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a8g .ks-amber{ fill:#854F0B; font-size:13px; }
.a8g .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a8g .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a8g .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a8g .kb-amber, :root[data-theme="dark"] .a8g .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a8g .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a8g .kh-amber{ fill:#EF9F27; }
.a8g .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a8g-amber); }
.a8g .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a8g-amber); }
.a8g .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
</style>
<defs><marker id="a8g-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a8g-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a8g-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a8g-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a8g-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a8g-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker></defs>
<g class="a8g">
<rect x="45" y="16" width="150" height="40" rx="7" class="k-blue"/>
<text x="120.0" y="40.5" text-anchor="middle" class="kb-blue">backend service</text>
<line x1="120" y1="56" x2="120" y2="190" class="gd"/>
<rect x="285" y="16" width="150" height="40" rx="7" class="k-amber"/>
<text x="360.0" y="40.5" text-anchor="middle" class="kb-amber">auth server</text>
<line x1="360" y1="56" x2="360" y2="190" class="gd"/>
<rect x="525" y="16" width="150" height="40" rx="7" class="k-teal"/>
<text x="600.0" y="40.5" text-anchor="middle" class="kb-teal">API</text>
<line x1="600" y1="56" x2="600" y2="190" class="gd"/>
<line x1="122" y1="90" x2="358" y2="90" class="ar-blue"/>
<text x="240.0" y="83" text-anchor="middle" class="s">client id + secret</text>
<line x1="358" y1="124" x2="122" y2="124" class="ar-amber"/>
<text x="240.0" y="117" text-anchor="middle" class="s">access token</text>
<line x1="122" y1="160" x2="598" y2="160" class="ar-blue"/>
<text x="240.0" y="153" text-anchor="middle" class="s">Bearer token</text>
<line x1="598" y1="190" x2="122" y2="190" class="ar-teal"/>
<text x="480.0" y="183" text-anchor="middle" class="s">200 OK</text>
</g>
</svg>
<figcaption>For a nightly job or one service calling another: the application is acting for itself.</figcaption>
</figure>

When no user is involved, such as a nightly job or one microservice calling another, the application authenticates as itself with the **client credentials** grant and receives a token for its own permissions.

### OpenID Connect

OAuth answers "may this app access the API?", not "who is the user?". **OpenID Connect** (OIDC) is a thin identity layer on top: with the `openid` scope, the authorization server also returns an **ID token**, a JWT describing the user, which the client uses to log the user in. "Sign in with Google" or Microsoft is OIDC. The rule of thumb: **ID tokens are for the client; access tokens are for the API.**

In practice you rarely build an authorization server yourself. Use an established identity provider, such as Keycloak, Auth0, Okta, Microsoft Entra ID, or a cloud provider's service, and make your API a well-behaved resource server that verifies tokens as shown above.

## Good habits

- HTTPS everywhere, always.
- Short-lived access tokens; verify **signature, algorithm, expiry, issuer, and audience** on every request.
- **Least privilege**: narrow scopes, and grant only what the client needs.
- Never put tokens or keys in URLs, logs, or source code. Load secrets from the environment, as `library_auth.py` does with `LIBRARY_SECRET`.
- Hash stored passwords with a slow algorithm (scrypt, bcrypt, Argon2) and compare secrets in constant time (`hmac.compare_digest`).
- Return **401** with `WWW-Authenticate` for authentication failures and **403** for permission failures.

## Summary

- **Authentication** is who you are (**401**); **authorization** is what you may do (**403**).
- **API keys** identify applications; **bearer tokens** carry identity and **scopes** for users and services.
- A **JWT** is signed, not encrypted. Verify it fully, with a **pinned algorithm**.
- **OAuth 2.0** delegates limited access; use **authorization code with PKCE** for users and **client credentials** for services. **OAuth 2.1** removes the password and implicit grants.
- **OpenID Connect** adds login with **ID tokens**. Use an existing identity provider.

## Check your understanding

Choose the best answer for each question, then check your answers in [Answers to Chapter Questions](answers.md#chapter-8-authentication-and-authorization).

**1. What question does authentication answer, and which status code reports its failure?**

- A. What may you do? 403
- B. Who are you? 401
- C. Where are you? 404
- D. How many requests? 429

**2. How should a server store API keys?**

- A. In plain text
- B. In the URL
- C. As hashes, like passwords
- D. In a cookie

**3. Is a JWT's payload secret?**

- A. No, it is signed, not encrypted, so anyone can read it
- B. Yes, it is encrypted
- C. Only the header is readable
- D. Only with HTTPS

**4. Why pin the algorithm, as in algorithms=["HS256"], when verifying a JWT?**

- A. It stops forged tokens that claim alg none or switch algorithms
- B. It is faster
- C. It shortens the token
- D. It encrypts the payload

**5. Why do the demo's access tokens last only 15 minutes?**

- A. To save memory
- B. OAuth requires it
- C. A JWT is hard to revoke, so a short lifetime limits damage if one leaks
- D. Clocks drift

**6. Which OAuth 2.0 flow should a user-facing app use?**

- A. Password grant
- B. Authorization code with PKCE
- C. Implicit grant
- D. Client credentials

**7. Which flow fits one backend service calling another, with no user involved?**

- A. Authorization code with PKCE
- B. Implicit grant
- C. Device code
- D. Client credentials

**8. What does OpenID Connect add to OAuth 2.0?**

- A. Rate limiting
- B. Login, with an ID token that tells the client who the user is
- C. Encryption of all traffic
- D. API versioning
