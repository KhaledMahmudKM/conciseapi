# Chapter 9: API Security

Authentication is necessary but nowhere near sufficient. Most serious API breaches involve callers who were properly logged in and then asked for something they should not have had. This chapter walks through the **OWASP API Security Top 10**, demonstrates six of the risks against a deliberately vulnerable API, and fixes each one.

## The OWASP API Security Top 10

OWASP, the Open Worldwide Application Security Project, publishes a list of the most critical API risks. The current edition is from **2023**.

<figure class="diagram">
<svg viewBox="0 0 720 330" style="width:100%;height:auto;max-width:720px" role="img" aria-label="The OWASP API Security Top 10, 2023 edition: API1 broken object level authorization; API2 broken authentication; API3 broken object property level authorization; API4 unrestricted resource consumption; API5 broken function level authorization; API6 unrestricted access to sensitive business flows; API7 server side request forgery; API8 security misconfiguration; API9 improper inventory management; API10 unsafe consumption of APIs." xmlns="http://www.w3.org/2000/svg">
<style>
.a9a{ font-family:var(--sans),sans-serif; }
.a9a .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a9a .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a9a .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a9a .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a9a .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a9a .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a9a .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a9a .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a9a .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a9a .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a9a .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a9a .s{ fill:var(--text-dim); font-size:13px; }
.a9a .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a9a .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a9a .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a9a .c{ fill:var(--text-faint); font-size:12.5px; }
.a9a .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a9a .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a9a .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a9a .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a9a-a); }
.a9a .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a9a-a); marker-start:url(#a9a-s); }
.a9a .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a9a-g); }
.a9a .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a9a-a); }
.a9a .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a9a .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a9a .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a9a .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a9a .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a9a .ks-amber{ fill:#854F0B; font-size:13px; }
.a9a .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a9a .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9a .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a9a .kb-amber, :root[data-theme="dark"] .a9a .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a9a .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a9a .kh-amber{ fill:#EF9F27; }
.a9a .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a9a-amber); }
.a9a .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9a-amber); }
.a9a .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a9a .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a9a .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a9a .ks-purple{ fill:#534AB7; font-size:13px; }
.a9a .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a9a .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9a .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a9a .kb-purple, :root[data-theme="dark"] .a9a .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a9a .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a9a .kh-purple{ fill:#AFA9EC; }
.a9a .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a9a-purple); }
.a9a .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9a-purple); }
.a9a .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a9a .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a9a .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a9a .ks-green{ fill:#3B6D11; font-size:13px; }
.a9a .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a9a .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9a .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a9a .kb-green, :root[data-theme="dark"] .a9a .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a9a .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a9a .kh-green{ fill:#97C459; }
.a9a .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a9a-green); }
.a9a .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9a-green); }
.a9a .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a9a .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a9a .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a9a .ks-red{ fill:#A32D2D; font-size:13px; }
.a9a .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a9a .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9a .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a9a .kb-red, :root[data-theme="dark"] .a9a .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a9a .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a9a .kh-red{ fill:#F09595; }
.a9a .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a9a-red); }
.a9a .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9a-red); }
.a9a .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
.a9a .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a9a .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a9a .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a9a .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a9a .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9a .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a9a .kb-gray, :root[data-theme="dark"] .a9a .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a9a .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a9a .kh-gray{ fill:#B4B2A9; }
.a9a .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a9a-gray); }
.a9a .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9a-gray); }
.a9a .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a9a-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a9a-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a9a-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a9a-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a9a-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a9a-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a9a-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker><marker id="a9a-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a9a">
<rect x="20" y="16" width="334" height="44" rx="7" class="k-red"/>
<text x="187.0" y="42.5" text-anchor="middle" class="kb-red">API1  Broken Object Level Authorization</text>
<circle cx="338" cy="26" r="6" class="k-green"/>
<rect x="366" y="16" width="334" height="44" rx="7" class="k-red"/>
<text x="533.0" y="42.5" text-anchor="middle" class="kb-red">API2  Broken Authentication</text>
<rect x="20" y="72" width="334" height="44" rx="7" class="k-red"/>
<text x="187.0" y="98.5" text-anchor="middle" class="kb-red">API3  Broken Object Property Level Authz</text>
<circle cx="338" cy="82" r="6" class="k-green"/>
<rect x="366" y="72" width="334" height="44" rx="7" class="k-amber"/>
<text x="533.0" y="98.5" text-anchor="middle" class="kb-amber">API4  Unrestricted Resource Consumption</text>
<circle cx="684" cy="82" r="6" class="k-green"/>
<rect x="20" y="128" width="334" height="44" rx="7" class="k-red"/>
<text x="187.0" y="154.5" text-anchor="middle" class="kb-red">API5  Broken Function Level Authorization</text>
<circle cx="338" cy="138" r="6" class="k-green"/>
<rect x="366" y="128" width="334" height="44" rx="7" class="k-amber"/>
<text x="533.0" y="154.5" text-anchor="middle" class="kb-amber">API6  Unrestricted Access to Business Flows</text>
<rect x="20" y="184" width="334" height="44" rx="7" class="k-purple"/>
<text x="187.0" y="210.5" text-anchor="middle" class="kb-purple">API7  Server Side Request Forgery</text>
<circle cx="338" cy="194" r="6" class="k-green"/>
<rect x="366" y="184" width="334" height="44" rx="7" class="k-gray"/>
<text x="533.0" y="210.5" text-anchor="middle" class="kb-gray">API8  Security Misconfiguration</text>
<rect x="20" y="240" width="334" height="44" rx="7" class="k-gray"/>
<text x="187.0" y="266.5" text-anchor="middle" class="kb-gray">API9  Improper Inventory Management</text>
<rect x="366" y="240" width="334" height="44" rx="7" class="k-purple"/>
<text x="533.0" y="266.5" text-anchor="middle" class="kb-purple">API10  Unsafe Consumption of APIs</text>
<circle cx="30" cy="306" r="6" class="k-green"/>
<text x="44" y="311" text-anchor="start" class="s">demonstrated with shop_insecure.py and fixed in shop_secure.py</text>
</g>
</svg>
<figcaption>Red: authorization and authentication. Amber: abuse of capacity. Purple: trusting other systems. Gray: operations.</figcaption>
</figure>

| Risk | In one sentence |
|---|---|
| **API1** Broken Object Level Authorization | The API returns or changes an object without checking that the caller may access **that** object. |
| **API2** Broken Authentication | Weak login, token, or password handling lets attackers become other users. |
| **API3** Broken Object Property Level Authorization | The API exposes or accepts **fields** the caller should not see or set. |
| **API4** Unrestricted Resource Consumption | No limits on request size, page size, rate, or cost. |
| **API5** Broken Function Level Authorization | Ordinary users can call administrative **functions**. |
| **API6** Unrestricted Access to Sensitive Business Flows | Automated abuse of legitimate features: bulk ticket buying, fake sign-ups. |
| **API7** Server Side Request Forgery | The API fetches a URL the caller supplies, reaching internal systems. |
| **API8** Security Misconfiguration | Verbose errors, default settings, missing TLS, permissive CORS. |
| **API9** Improper Inventory Management | Forgotten old versions and undocumented endpoints stay exposed. |
| **API10** Unsafe Consumption of APIs | Trusting data from third-party APIs more than user input. |

## The lab

The code folder has two versions of a small shop API. `shop_insecure.py` contains one flaw per endpoint, marked in comments. `shop_secure.py` is the same API with each flaw fixed. Run them side by side:

```bash
fastapi dev shop_insecure.py --port 8001     # in one terminal
fastapi dev shop_secure.py   --port 8002     # in another
```

Three users authenticate with fixed bearer tokens: `token-alice` and `token-bob` are customers, `token-admin` is an administrator. Alice owns the odd-numbered orders, Bob the even ones. **Never deploy the insecure version**, not even on a lab network shared with others.

## API1: Broken object level authorization

<figure class="diagram">
<svg viewBox="0 0 720 270" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Broken object level authorization. Alice is logged in and owns order 1. She changes the ID in the URL to 2, which belongs to Bob. The insecure API checks only that she is logged in and returns Bob&#x27;s order. The secure API also checks that the order&#x27;s owner is the caller and answers 404." xmlns="http://www.w3.org/2000/svg">
<style>
.a9b{ font-family:var(--sans),sans-serif; }
.a9b .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a9b .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a9b .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a9b .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a9b .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a9b .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a9b .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a9b .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a9b .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a9b .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a9b .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a9b .s{ fill:var(--text-dim); font-size:13px; }
.a9b .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a9b .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a9b .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a9b .c{ fill:var(--text-faint); font-size:12.5px; }
.a9b .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a9b .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a9b .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a9b .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a9b-a); }
.a9b .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a9b-a); marker-start:url(#a9b-s); }
.a9b .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a9b-g); }
.a9b .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a9b-a); }
.a9b .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a9b .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a9b .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a9b .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a9b .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a9b .ks-blue{ fill:#185FA5; font-size:13px; }
.a9b .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a9b .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9b .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a9b .kb-blue, :root[data-theme="dark"] .a9b .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a9b .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a9b .kh-blue{ fill:#85B7EB; }
.a9b .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a9b-blue); }
.a9b .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9b-blue); }
.a9b .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a9b .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a9b .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a9b .ks-purple{ fill:#534AB7; font-size:13px; }
.a9b .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a9b .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9b .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a9b .kb-purple, :root[data-theme="dark"] .a9b .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a9b .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a9b .kh-purple{ fill:#AFA9EC; }
.a9b .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a9b-purple); }
.a9b .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9b-purple); }
.a9b .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a9b .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a9b .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a9b .ks-green{ fill:#3B6D11; font-size:13px; }
.a9b .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a9b .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9b .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a9b .kb-green, :root[data-theme="dark"] .a9b .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a9b .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a9b .kh-green{ fill:#97C459; }
.a9b .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a9b-green); }
.a9b .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9b-green); }
.a9b .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a9b .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a9b .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a9b .ks-red{ fill:#A32D2D; font-size:13px; }
.a9b .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a9b .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9b .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a9b .kb-red, :root[data-theme="dark"] .a9b .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a9b .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a9b .kh-red{ fill:#F09595; }
.a9b .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a9b-red); }
.a9b .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9b-red); }
.a9b .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
</style>
<defs><marker id="a9b-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a9b-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a9b-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a9b-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a9b-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a9b-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a9b-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker></defs>
<g class="a9b">
<rect x="20" y="100" width="106" height="60" rx="7" class="k-blue"/>
<text x="73.0" y="125.5" text-anchor="middle" class="kb-blue">alice</text>
<text x="73.0" y="143.5" text-anchor="middle" class="ks-blue">token-alice</text>
<line x1="128" y1="130" x2="240" y2="130" class="ar-blue"/>
<text x="184" y="120" text-anchor="middle" class="m">GET /orders/2</text>
<rect x="244" y="20" width="210" height="100" rx="7" class="k-red"/>
<text x="349.0" y="52.5" text-anchor="middle" class="kb-red">insecure</text>
<text x="349.0" y="74.5" text-anchor="middle" class="ks-red">logged in?  yes</text>
<text x="349.0" y="96.5" text-anchor="middle" class="ks-red">return order 2</text>
<rect x="244" y="140" width="210" height="110" rx="7" class="k-green"/>
<text x="349.0" y="166.5" text-anchor="middle" class="kb-green">secure</text>
<text x="349.0" y="188.5" text-anchor="middle" class="ks-green">logged in?  yes</text>
<text x="349.0" y="210.5" text-anchor="middle" class="ks-green">owner == alice?  no</text>
<text x="349.0" y="232.5" text-anchor="middle" class="kb-green">404 No such order</text>
<rect x="500" y="30" width="200" height="80" rx="7" class="k-purple"/>
<text x="600.0" y="65.5" text-anchor="middle" class="kb-purple">bob's order 2</text>
<text x="600.0" y="83.5" text-anchor="middle" class="km-purple">{"owner": 2, "total": 12}</text>
<line x1="456" y1="70" x2="498" y2="70" class="ar-red"/>
<text x="600" y="160" text-anchor="middle" class="kh-red">authentication is not</text>
<text x="600" y="180" text-anchor="middle" class="kh-red">authorization</text>
<text x="600" y="212" text-anchor="middle" class="s">check ownership on</text>
<text x="600" y="230" text-anchor="middle" class="s">every object, every call</text>
</g>
</svg>
<figcaption>The most common API flaw: the API trusts the ID in the URL. Sequential IDs make it trivial to walk through everyone's data.</figcaption>
</figure>

Alice asks for order 2, which is Bob's:

```bash
curl -s localhost:8001/orders/2 -H "Authorization: Bearer token-alice"   # insecure
curl -s localhost:8002/orders/2 -H "Authorization: Bearer token-alice"   # secure
```

```text
{"id":2,"owner":2,"item":"book #2","total":12}
{"detail":"No such order"}
```

The insecure handler only checks that the order exists. The fix checks ownership:

```python
@app.get("/orders/{order_id}")
def get_order(order_id: int, user: dict = Depends(current_user)):
    order = ORDERS.get(order_id)
    if order is None or order["owner"] != user["id"]:
        raise HTTPException(404, "No such order")
    return order
```

Answering **404** rather than 403 avoids confirming that order 2 exists. BOLA tops the list because it is easy to introduce and easy to exploit: a loop over IDs downloads everyone's data. The defence is a rule, applied to **every** endpoint that takes an ID: look up the object **through** the user (`WHERE id = ? AND owner_id = ?`), never by ID alone. Random IDs make guessing harder but are not a substitute for the check.

## API3: Broken object property level authorization

<figure class="diagram">
<svg viewBox="0 0 720 290" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Broken object property level authorization, in both directions. On reading, the insecure API returns every field, including the password hash and an internal flag; a response model returns only id, name, email and credit. On writing, the insecure API accepts any field, so a customer can set role to admin and credit to a million; an input model with extra fields forbidden accepts only name and email." xmlns="http://www.w3.org/2000/svg">
<style>
.a9c{ font-family:var(--sans),sans-serif; }
.a9c .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a9c .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a9c .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a9c .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a9c .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a9c .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a9c .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a9c .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a9c .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a9c .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a9c .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a9c .s{ fill:var(--text-dim); font-size:13px; }
.a9c .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a9c .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a9c .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a9c .c{ fill:var(--text-faint); font-size:12.5px; }
.a9c .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a9c .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a9c .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a9c .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a9c-a); }
.a9c .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a9c-a); marker-start:url(#a9c-s); }
.a9c .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a9c-g); }
.a9c .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a9c-a); }
.a9c .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a9c .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a9c .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a9c .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a9c .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a9c .ks-amber{ fill:#854F0B; font-size:13px; }
.a9c .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a9c .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9c .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a9c .kb-amber, :root[data-theme="dark"] .a9c .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a9c .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a9c .kh-amber{ fill:#EF9F27; }
.a9c .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a9c-amber); }
.a9c .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9c-amber); }
.a9c .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a9c .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a9c .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a9c .ks-purple{ fill:#534AB7; font-size:13px; }
.a9c .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a9c .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9c .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a9c .kb-purple, :root[data-theme="dark"] .a9c .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a9c .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a9c .kh-purple{ fill:#AFA9EC; }
.a9c .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a9c-purple); }
.a9c .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9c-purple); }
.a9c .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a9c .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a9c .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a9c .ks-green{ fill:#3B6D11; font-size:13px; }
.a9c .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a9c .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9c .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a9c .kb-green, :root[data-theme="dark"] .a9c .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a9c .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a9c .kh-green{ fill:#97C459; }
.a9c .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a9c-green); }
.a9c .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9c-green); }
.a9c .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a9c .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a9c .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a9c .ks-red{ fill:#A32D2D; font-size:13px; }
.a9c .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a9c .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9c .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a9c .kb-red, :root[data-theme="dark"] .a9c .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a9c .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a9c .kh-red{ fill:#F09595; }
.a9c .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a9c-red); }
.a9c .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9c-red); }
.a9c .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
</style>
<defs><marker id="a9c-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a9c-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a9c-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a9c-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a9c-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a9c-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a9c-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker></defs>
<g class="a9c">
<text x="20" y="24" text-anchor="start" class="kh-purple">read: excessive data exposure</text>
<rect x="20" y="36" width="200" height="40" rx="5" class="k-green"/>
<text x="120.0" y="60.5" text-anchor="middle" class="km-green">id, name, email, credit</text>
<rect x="232" y="36" width="90" height="40" rx="5" class="k-amber"/>
<text x="277.0" y="60.5" text-anchor="middle" class="km-amber">role</text>
<rect x="334" y="36" width="170" height="40" rx="5" class="k-red"/>
<text x="419.0" y="60.5" text-anchor="middle" class="km-red">password_hash</text>
<rect x="516" y="36" width="184" height="40" rx="5" class="k-red"/>
<text x="608.0" y="60.5" text-anchor="middle" class="km-red">is_internal_tester</text>
<text x="20" y="98" text-anchor="start" class="s">response_model=PublicUser lets only the green box through</text>
<text x="20" y="146" text-anchor="start" class="kh-purple">write: mass assignment</text>
<rect x="20" y="158" width="330" height="50" rx="6" class="k-red"/>
<text x="185.0" y="178.5" text-anchor="middle" class="km-red">PATCH /users/me  {"role": "admin",</text>
<text x="185.0" y="196.5" text-anchor="middle" class="km-red">                 "credit": 1000000}</text>
<line x1="352" y1="183" x2="400" y2="183" class="ar"/>
<rect x="404" y="158" width="296" height="50" rx="7" class="k-red"/>
<text x="552.0" y="187.5" text-anchor="middle" class="kb-red">insecure: 200, alice is now admin</text>
<rect x="404" y="222" width="296" height="50" rx="7" class="k-green"/>
<text x="552.0" y="251.5" text-anchor="middle" class="kb-green">secure: 422, extra inputs forbidden</text>
<text x="20" y="248" text-anchor="start" class="s">UserUpdate accepts name and email only</text>
</g>
</svg>
<figcaption>Never pass a raw dictionary from the client into your data, or your data straight back to the client. Models are allowlists.</figcaption>
</figure>

**Reading.** Alice asks for her own profile:

```text
insecure: {"id":1,"name":"alice","email":"alice@example.com","role":"customer","credit":20,
           "password_hash":"scrypt$9f2c...","is_internal_tester":false}
secure:   {"id":1,"name":"alice","email":"alice@example.com","credit":20}
```

The insecure handler returns the stored record, including a password hash and an internal flag. Relying on the client to hide fields is not security: anyone can read the raw response. The fix is a response model, which acts as an **allowlist** of fields:

```python
class PublicUser(BaseModel):            # only what the client may see
    id: int
    name: str
    email: str
    credit: int

@app.get("/users/me", response_model=PublicUser)
```

**Writing** ("mass assignment"). Alice tries to promote herself:

```bash
curl -s -X PATCH localhost:8001/users/me -H "Authorization: Bearer token-alice" \
     -H "Content-Type: application/json" -d '{"role": "admin", "credit": 1000000}'
```

The insecure API accepts a raw dictionary and copies every key into the user record; Alice is now an admin with a million in credit. The secure API declares exactly what may change:

```python
class UserUpdate(BaseModel):            # only what the client may change
    model_config = ConfigDict(extra="forbid")
    name: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = None
```

and rejects the request with `422` and `"Extra inputs are not permitted"` for both `role` and `credit`.

## API4: Unrestricted resource consumption

```bash
curl -s -o /dev/null -w "%{http_code} %{size_download} bytes\n" \
     "localhost:8001/orders?limit=1000000" -H "Authorization: Bearer token-alice"
```

```text
insecure: 200 53351 bytes      (all 1000 of Alice's orders in one response)
secure:   422 146 bytes        (limit must be at most 50)
```

With real data, an unbounded query can exhaust memory, the database, or a paid third-party service. The fix is one line, `limit: int = Query(default=10, ge=1, le=50)`, and the principle is wider: limit **page sizes, request body sizes, upload sizes, query complexity, timeouts, and request rates**. Chapter 10 adds rate limiting.

## API5: Broken function level authorization

Bob, an ordinary customer, calls an admin endpoint to delete a user:

```text
insecure: DELETE /admin/users/2 -> 204 No Content
secure:   DELETE /admin/users/2 -> 403 {"detail":"Admins only"}
```

The insecure endpoint checks only that the caller is logged in. A `/admin` prefix in a URL hides nothing: attackers read your OpenAPI document and your JavaScript. The fix is a dependency that checks the role, applied to every administrative route (or to a whole router):

```python
def require_admin(user: dict = Depends(current_user)) -> dict:
    if user["role"] != "admin":
        raise HTTPException(403, "Admins only")
    return user
```

API1 asks "may this user touch **this object**?"; API5 asks "may this user call **this function** at all?". Both checks are needed.

## API7: Server side request forgery

<figure class="diagram">
<svg viewBox="0 0 720 300" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Server side request forgery. The attacker asks the API to fetch a URL. Instead of a public image, the attacker supplies an internal address such as the cloud metadata service at 169.254.169.254 or an admin service on localhost. The API server, which sits inside the network, fetches it and returns the response, leaking credentials. The fix is an allowlist of hosts, https only, and a check that the address resolves to a public IP, with redirects disabled." xmlns="http://www.w3.org/2000/svg">
<style>
.a9d{ font-family:var(--sans),sans-serif; }
.a9d .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a9d .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a9d .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a9d .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a9d .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a9d .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a9d .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a9d .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a9d .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a9d .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a9d .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a9d .s{ fill:var(--text-dim); font-size:13px; }
.a9d .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a9d .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a9d .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a9d .c{ fill:var(--text-faint); font-size:12.5px; }
.a9d .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a9d .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a9d .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a9d .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a9d-a); }
.a9d .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a9d-a); marker-start:url(#a9d-s); }
.a9d .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a9d-g); }
.a9d .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a9d-a); }
.a9d .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a9d .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a9d .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a9d .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a9d .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a9d .ks-teal{ fill:#0F6E56; font-size:13px; }
.a9d .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a9d .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9d .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a9d .kb-teal, :root[data-theme="dark"] .a9d .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a9d .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a9d .kh-teal{ fill:#5DCAA5; }
.a9d .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a9d-teal); }
.a9d .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9d-teal); }
.a9d .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a9d .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a9d .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a9d .ks-purple{ fill:#534AB7; font-size:13px; }
.a9d .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a9d .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9d .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a9d .kb-purple, :root[data-theme="dark"] .a9d .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a9d .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a9d .kh-purple{ fill:#AFA9EC; }
.a9d .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a9d-purple); }
.a9d .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9d-purple); }
.a9d .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a9d .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a9d .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a9d .ks-green{ fill:#3B6D11; font-size:13px; }
.a9d .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a9d .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9d .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a9d .kb-green, :root[data-theme="dark"] .a9d .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a9d .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a9d .kh-green{ fill:#97C459; }
.a9d .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a9d-green); }
.a9d .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9d-green); }
.a9d .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a9d .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a9d .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a9d .ks-red{ fill:#A32D2D; font-size:13px; }
.a9d .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a9d .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9d .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a9d .kb-red, :root[data-theme="dark"] .a9d .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a9d .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a9d .kh-red{ fill:#F09595; }
.a9d .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a9d-red); }
.a9d .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9d-red); }
.a9d .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
.a9d .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a9d .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a9d .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a9d .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a9d .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9d .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a9d .kb-gray, :root[data-theme="dark"] .a9d .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a9d .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a9d .kh-gray{ fill:#B4B2A9; }
.a9d .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a9d-gray); }
.a9d .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9d-gray); }
.a9d .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a9d-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a9d-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a9d-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a9d-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a9d-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a9d-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a9d-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker><marker id="a9d-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a9d">
<rect x="20" y="110" width="140" height="60" rx="7" class="k-red"/>
<text x="90.0" y="144.5" text-anchor="middle" class="kb-red">attacker</text>
<rect x="220" y="20" width="480" height="260" rx="10" class="k-gray"/>
<text x="240" y="44" text-anchor="start" class="kh-gray">inside the network</text>
<rect x="250" y="100" width="160" height="80" rx="7" class="k-teal"/>
<text x="330.0" y="135.5" text-anchor="middle" class="kb-teal">API server</text>
<text x="330.0" y="153.5" text-anchor="middle" class="km-teal">POST /covers/preview</text>
<rect x="500" y="60" width="180" height="60" rx="7" class="k-purple"/>
<text x="590.0" y="85.5" text-anchor="middle" class="km-purple">169.254.169.254</text>
<text x="590.0" y="103.5" text-anchor="middle" class="ks-purple">cloud credentials</text>
<rect x="500" y="160" width="180" height="60" rx="7" class="k-purple"/>
<text x="590.0" y="185.5" text-anchor="middle" class="km-purple">localhost:8080/admin</text>
<text x="590.0" y="203.5" text-anchor="middle" class="ks-purple">internal service</text>
<line x1="162" y1="140" x2="248" y2="140" class="ar-red"/>
<text x="205" y="130" text-anchor="middle" class="s">{"url": ...}</text>
<line x1="412" y1="125" x2="498" y2="92" class="ar-red"/>
<line x1="412" y1="155" x2="498" y2="188" class="ar-red"/>
<rect x="250" y="232" width="430" height="36" rx="7" class="k-green"/>
<text x="465.0" y="254.5" text-anchor="middle" class="kb-green">fix: allowlist host, https only, public IPs only, no redirects</text>
</g>
</svg>
<figcaption>The server has network access the attacker does not. Every URL a client supplies is a request the server makes on the attacker's behalf.</figcaption>
</figure>

The shop offers a cover preview: the client sends an image URL and the server fetches it. Alice sends a URL pointing at the server itself:

```bash
curl -s -X POST localhost:8001/covers/preview -H "Authorization: Bearer token-alice" \
     -H "Content-Type: application/json" -d '{"url": "http://127.0.0.1:8001/openapi.json"}'
```

```text
insecure: {"preview":"{\"openapi\":\"3.1.0\",\"info\":{\"title\":\"Shop API (INSECURE)\", ...
secure:   400 {"detail":"URL not allowed"}
```

Here the server fetched a page from itself, but the same request could reach a database admin console on the internal network or, in the cloud, the **instance metadata service** at `169.254.169.254`, which can hand out the server's credentials. The secure version only fetches URLs that pass every check:

```python
def safe_cover_url(url: str) -> bool:
    u = urlparse(url)
    if u.scheme != "https" or u.hostname not in COVER_HOSTS or u.port not in (None, 443):
        return False
    try:
        addresses = {i[4][0] for i in socket.getaddrinfo(u.hostname, 443)}
    except socket.gaierror:
        return False
    return all(ipaddress.ip_address(a).is_global for a in addresses)
```

and fetches with `allow_redirects=False`, so an allowed host cannot bounce the request elsewhere. An allowlist of hosts is far stronger than a blocklist of addresses, which attackers bypass with alternative IP notations, DNS names that resolve to internal addresses, and redirects.

## The other four

- **API2 Broken authentication**: covered in Chapter 8. Rate-limit login and token endpoints, require strong passwords or better, verify tokens fully, and never accept unsigned tokens.
- **API6 Sensitive business flows**: protect flows such as checkout or sign-up from automation with rate limits per account, device fingerprinting, CAPTCHAs, or business rules (one ticket purchase per customer).
- **API8 Security misconfiguration**: return problem details without stack traces, turn off debug modes, set security headers, keep TLS current, and configure CORS narrowly.
- **API9 Inventory management**: know every API, version, and environment you expose; retire old versions (Chapter 11); keep the OpenAPI document as the inventory.
- **API10 Unsafe consumption**: validate responses from third-party APIs with models, just like client input, use timeouts, and do not follow redirects blindly.

## CORS

Browsers enforce the **same-origin policy**: JavaScript on `https://app.example.com` cannot read responses from `https://api.example.com` unless the API allows it. **Cross-Origin Resource Sharing** (CORS) is how it does.

<figure class="diagram">
<svg viewBox="0 0 720 330" style="width:100%;height:auto;max-width:720px" role="img" aria-label="A CORS preflight. A page from app.example.com wants to call api.example.com with a PATCH and a JSON body. The browser first sends an OPTIONS request with Origin and Access-Control-Request-Method headers. The API replies with Access-Control-Allow-Origin and allowed methods and headers. Only if they match does the browser send the real request and let the page read the response." xmlns="http://www.w3.org/2000/svg">
<style>
.a9e{ font-family:var(--sans),sans-serif; }
.a9e .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a9e .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a9e .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a9e .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a9e .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a9e .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a9e .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a9e .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a9e .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a9e .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a9e .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a9e .s{ fill:var(--text-dim); font-size:13px; }
.a9e .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a9e .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a9e .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a9e .c{ fill:var(--text-faint); font-size:12.5px; }
.a9e .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a9e .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a9e .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a9e .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a9e-a); }
.a9e .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a9e-a); marker-start:url(#a9e-s); }
.a9e .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a9e-g); }
.a9e .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a9e-a); }
.a9e .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a9e .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a9e .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a9e .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a9e .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a9e .ks-blue{ fill:#185FA5; font-size:13px; }
.a9e .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a9e .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9e .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a9e .kb-blue, :root[data-theme="dark"] .a9e .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a9e .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a9e .kh-blue{ fill:#85B7EB; }
.a9e .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a9e-blue); }
.a9e .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9e-blue); }
.a9e .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a9e .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a9e .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a9e .ks-teal{ fill:#0F6E56; font-size:13px; }
.a9e .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a9e .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9e .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a9e .kb-teal, :root[data-theme="dark"] .a9e .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a9e .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a9e .kh-teal{ fill:#5DCAA5; }
.a9e .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a9e-teal); }
.a9e .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9e-teal); }
.a9e .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a9e .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a9e .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a9e .ks-green{ fill:#3B6D11; font-size:13px; }
.a9e .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a9e .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9e .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a9e .kb-green, :root[data-theme="dark"] .a9e .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a9e .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a9e .kh-green{ fill:#97C459; }
.a9e .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a9e-green); }
.a9e .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9e-green); }
.a9e .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a9e .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a9e .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a9e .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a9e .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a9e .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9e .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a9e .kb-gray, :root[data-theme="dark"] .a9e .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a9e .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a9e .kh-gray{ fill:#B4B2A9; }
.a9e .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a9e-gray); }
.a9e .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9e-gray); }
.a9e .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a9e-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a9e-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a9e-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a9e-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a9e-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a9e-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a9e-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a9e">
<rect x="35" y="16" width="150" height="40" rx="7" class="k-blue"/>
<text x="110.0" y="40.5" text-anchor="middle" class="kb-blue">web page</text>
<line x1="110" y1="56" x2="110" y2="320" class="gd"/>
<rect x="285" y="16" width="150" height="40" rx="7" class="k-gray"/>
<text x="360.0" y="40.5" text-anchor="middle" class="kb-gray">browser</text>
<line x1="360" y1="56" x2="360" y2="320" class="gd"/>
<rect x="535" y="16" width="150" height="40" rx="7" class="k-teal"/>
<text x="610.0" y="40.5" text-anchor="middle" class="kb-teal">api.example.com</text>
<line x1="610" y1="56" x2="610" y2="320" class="gd"/>
<line x1="112" y1="92" x2="358" y2="92" class="ar-blue"/>
<text x="235.0" y="85" text-anchor="middle" class="s">fetch()</text>
<line x1="362" y1="140" x2="608" y2="140" class="ar-gray"/>
<text x="485.0" y="133" text-anchor="middle" class="s">OPTIONS + Origin</text>
<line x1="608" y1="178" x2="362" y2="178" class="ar-teal"/>
<text x="485.0" y="171" text-anchor="middle" class="s">Allow-Origin: app.example.com</text>
<line x1="362" y1="226" x2="608" y2="226" class="ar-gray"/>
<text x="485.0" y="219" text-anchor="middle" class="s">the real PATCH</text>
<line x1="608" y1="264" x2="362" y2="264" class="ar-teal"/>
<text x="485.0" y="257" text-anchor="middle" class="s">200 + Allow-Origin</text>
<line x1="358" y1="304" x2="112" y2="304" class="ar-green"/>
<text x="235.0" y="297" text-anchor="middle" class="s">page reads it</text>
</g>
</svg>
<figcaption>CORS is enforced by browsers, to protect users. It does nothing against curl or a script, so it is not access control.</figcaption>
</figure>

For anything beyond simple requests, the browser sends a **preflight** `OPTIONS` request first. In FastAPI:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(CORSMiddleware,
                   allow_origins=["https://app.example.com"],    # never "*" with credentials
                   allow_methods=["GET", "POST", "PATCH", "DELETE"],
                   allow_headers=["Authorization", "Content-Type"])
```

Two common misunderstandings: CORS **does not protect your API**, because curl, scripts, and servers ignore it entirely; and `allow_origins=["*"]` combined with credentials, or reflecting any `Origin` back, lets any website make authenticated calls with your users' cookies.

## Defence in depth

<figure class="diagram">
<svg viewBox="0 0 720 250" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Layers of defence for an API: TLS everywhere; a gateway with rate limits and request size limits; authentication of every request; authorization of every object, property and function; validation of input with strict models; minimal output through response models; and logging and monitoring of everything." xmlns="http://www.w3.org/2000/svg">
<style>
.a9f{ font-family:var(--sans),sans-serif; }
.a9f .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a9f .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a9f .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a9f .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a9f .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a9f .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a9f .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a9f .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a9f .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a9f .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a9f .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a9f .s{ fill:var(--text-dim); font-size:13px; }
.a9f .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a9f .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a9f .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a9f .c{ fill:var(--text-faint); font-size:12.5px; }
.a9f .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a9f .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a9f .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a9f .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a9f-a); }
.a9f .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a9f-a); marker-start:url(#a9f-s); }
.a9f .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a9f-g); }
.a9f .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a9f-a); }
.a9f .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a9f .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a9f .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a9f .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a9f .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a9f .ks-blue{ fill:#185FA5; font-size:13px; }
.a9f .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a9f .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9f .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a9f .kb-blue, :root[data-theme="dark"] .a9f .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a9f .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a9f .kh-blue{ fill:#85B7EB; }
.a9f .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a9f-blue); }
.a9f .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9f-blue); }
.a9f .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a9f .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a9f .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a9f .ks-teal{ fill:#0F6E56; font-size:13px; }
.a9f .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a9f .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9f .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a9f .kb-teal, :root[data-theme="dark"] .a9f .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a9f .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a9f .kh-teal{ fill:#5DCAA5; }
.a9f .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a9f-teal); }
.a9f .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9f-teal); }
.a9f .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a9f .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a9f .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a9f .ks-amber{ fill:#854F0B; font-size:13px; }
.a9f .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a9f .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9f .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a9f .kb-amber, :root[data-theme="dark"] .a9f .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a9f .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a9f .kh-amber{ fill:#EF9F27; }
.a9f .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a9f-amber); }
.a9f .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9f-amber); }
.a9f .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a9f .k-coral{ fill:#FAECE7; stroke:#D85A30; stroke-width:1.6; }
.a9f .kb-coral{ fill:#712B13; font-size:13px; font-weight:700; }
.a9f .ks-coral{ fill:#993C1D; font-size:13px; }
.a9f .km-coral{ fill:#712B13; font-size:12.5px; font-family:var(--mono),monospace; }
.a9f .kh-coral{ fill:#993C1D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9f .k-coral{ fill:#712B13; stroke:#F0997B; }
:root[data-theme="dark"] .a9f .kb-coral, :root[data-theme="dark"] .a9f .km-coral{ fill:#FAECE7; }
:root[data-theme="dark"] .a9f .ks-coral{ fill:#F5C4B3; }
:root[data-theme="dark"] .a9f .kh-coral{ fill:#F0997B; }
.a9f .ar-coral{ stroke:#D85A30; stroke-width:2; fill:none; marker-end:url(#a9f-coral); }
.a9f .ad-coral{ stroke:#D85A30; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9f-coral); }
.a9f .ln-coral{ stroke:#D85A30; stroke-width:2; fill:none; }
.a9f .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a9f .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a9f .ks-purple{ fill:#534AB7; font-size:13px; }
.a9f .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a9f .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9f .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a9f .kb-purple, :root[data-theme="dark"] .a9f .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a9f .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a9f .kh-purple{ fill:#AFA9EC; }
.a9f .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a9f-purple); }
.a9f .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9f-purple); }
.a9f .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a9f .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a9f .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a9f .ks-red{ fill:#A32D2D; font-size:13px; }
.a9f .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a9f .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9f .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a9f .kb-red, :root[data-theme="dark"] .a9f .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a9f .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a9f .kh-red{ fill:#F09595; }
.a9f .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a9f-red); }
.a9f .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9f-red); }
.a9f .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
.a9f .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a9f .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a9f .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a9f .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a9f .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a9f .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a9f .kb-gray, :root[data-theme="dark"] .a9f .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a9f .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a9f .kh-gray{ fill:#B4B2A9; }
.a9f .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a9f-gray); }
.a9f .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a9f-gray); }
.a9f .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a9f-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a9f-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a9f-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a9f-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a9f-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a9f-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a9f-coral" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#D85A30"/></marker><marker id="a9f-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a9f-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker><marker id="a9f-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a9f">
<rect x="20" y="16" width="680" height="26" rx="5" class="k-gray"/>
<text x="360.0" y="33.5" text-anchor="middle" class="kb-gray">TLS</text>
<rect x="38" y="46" width="644" height="26" rx="5" class="k-amber"/>
<text x="360.0" y="63.5" text-anchor="middle" class="kb-amber">gateway, rate limits</text>
<rect x="56" y="76" width="608" height="26" rx="5" class="k-coral"/>
<text x="360.0" y="93.5" text-anchor="middle" class="kb-coral">authenticate</text>
<rect x="74" y="106" width="572" height="26" rx="5" class="k-red"/>
<text x="360.0" y="123.5" text-anchor="middle" class="kb-red">authorize object, property, function</text>
<rect x="92" y="136" width="536" height="26" rx="5" class="k-purple"/>
<text x="360.0" y="153.5" text-anchor="middle" class="kb-purple">validate input</text>
<rect x="110" y="166" width="500" height="26" rx="5" class="k-teal"/>
<text x="360.0" y="183.5" text-anchor="middle" class="kb-teal">filter output</text>
<rect x="20" y="206" width="680" height="34" rx="7" class="k-blue"/>
<text x="360.0" y="227.5" text-anchor="middle" class="kb-blue">log and monitor all of it: request IDs, failures, unusual patterns</text>
</g>
</svg>
<figcaption>No single control is enough. Each layer catches what the previous one missed.</figcaption>
</figure>

Test your own APIs the way an attacker would. `tests/test_shop.py` writes one test per flaw and runs it against both implementations:

```python
def test_api1_bola(insecure, secure):
    # order 2 belongs to bob; alice asks for it
    assert insecure.get("/orders/2", headers=ALICE).status_code == 200      # leak
    assert secure.get("/orders/2", headers=ALICE).status_code == 404        # fixed
    assert secure.get("/orders/1", headers=ALICE).status_code == 200        # her own order still works


def test_api3_mass_assignment(insecure, secure):
    r = insecure.patch("/users/me", json={"role": "admin", "credit": 9999}, headers=ALICE)
    assert r.json()["role"] == "admin" and r.json()["credit"] == 9999           # privilege escalation
    assert secure.patch("/users/me", json={"credit": 9999}, headers=ALICE).status_code == 422
```

Each test proves both that the attack works on the insecure API and that the fix blocks it without breaking legitimate use. Run them all with `pytest tests/test_shop.py -v`.

Tools such as OWASP ZAP, Burp Suite, and the contract-testing tools from Chapter 7 automate much more of this.

## Summary

- Most API breaches come from **authorization** failures by authenticated users.
- **API1**: check ownership of **every object**; answer 404. **API5**: check the role for **every function**.
- **API3**: use **response models** and **input models with extra fields forbidden**; never pass raw dictionaries through.
- **API4**: enforce **limits** on everything a client controls.
- **API7**: fetch client-supplied URLs only through an **allowlist**, https only, public IPs only, no redirects.
- **CORS** protects browser users, not your API; configure it narrowly.
- Layer defences and write **tests** for every security rule.

## Check your understanding

Choose the best answer for each question, then check your answers in [Answers to Chapter Questions](answers.md#chapter-9-api-security).

**1. According to the chapter, where do most API breaches come from?**

- A. Authorization failures by authenticated users
- B. Broken encryption
- C. DDoS attacks
- D. Weak passwords only

**2. A user changes /orders/41 to /orders/42 and sees someone else's order. Which risk is this?**

- A. API4 Unrestricted resource consumption
- B. API7 Server side request forgery
- C. API1 Broken object level authorization
- D. API9 Inventory management

**3. What should the API answer when a user requests another user's object?**

- A. 403, to be precise
- B. 404, so it does not reveal that the object exists
- C. 200 with an empty body
- D. 500

**4. A user sets "role": "admin" in a profile update and it is saved. Which defence would have stopped this?**

- A. CORS
- B. HTTPS
- C. Rate limiting
- D. Input models with extra fields forbidden, instead of raw dictionaries

**5. A regular user calls DELETE /admin/users/7 successfully. Which risk is this?**

- A. API1
- B. API5 Broken function level authorization
- C. API3
- D. API8

**6. Why is SSRF dangerous in the cloud?**

- A. It slows the server
- B. It breaks CORS
- C. It deletes logs
- D. The server can be made to fetch internal addresses such as the metadata service at 169.254.169.254, which hands out credentials

**7. What does CORS protect?**

- A. Browser users, by controlling which sites' scripts may read your API's responses
- B. Your API from all attackers
- C. The database
- D. Server-to-server calls

**8. Which practice does the chapter recommend for every security rule?**

- A. Document it in a wiki
- B. Enforce it only in the gateway
- C. Write a test for it
- D. Check it once a year
