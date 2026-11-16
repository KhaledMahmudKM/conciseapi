# Chapter 1: What Is an API?

**API** stands for **Application Programming Interface**: a defined way for one piece of software to use another. The definition is broad on purpose. A Python function you import, a system call into the operating system, and a request to a payment service on the other side of the world are all APIs. This chapter explains what they have in common, narrows the focus to **web APIs**, and introduces the vocabulary used in the rest of the book.

## A contract, not an implementation

An API is a **contract**. It says which requests a client may make, what each request must contain, and what will come back.

<figure class="diagram">
<svg viewBox="0 0 720 270" style="width:100%;height:auto;max-width:720px" role="img" aria-label="An API is a contract between a client and a service. The client only sees the contract: which requests it may send and what responses come back. Behind the contract, the implementation, its code and its database, is hidden and can change freely." xmlns="http://www.w3.org/2000/svg">
<style>
.a1a{ font-family:var(--sans),sans-serif; }
.a1a .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a1a .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a1a .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a1a .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a1a .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a1a .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a1a .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a1a .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a1a .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a1a .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a1a .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a1a .s{ fill:var(--text-dim); font-size:13px; }
.a1a .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a1a .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a1a .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a1a .c{ fill:var(--text-faint); font-size:12.5px; }
.a1a .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a1a .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a1a .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a1a .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a1a-a); }
.a1a .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a1a-a); marker-start:url(#a1a-s); }
.a1a .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a1a-g); }
.a1a .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a1a-a); }
.a1a .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a1a .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a1a .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a1a .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a1a .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a1a .ks-blue{ fill:#185FA5; font-size:13px; }
.a1a .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a1a .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a1a .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a1a .kb-blue, :root[data-theme="dark"] .a1a .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a1a .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a1a .kh-blue{ fill:#85B7EB; }
.a1a .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a1a-blue); }
.a1a .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a1a-blue); }
.a1a .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a1a .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a1a .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a1a .ks-teal{ fill:#0F6E56; font-size:13px; }
.a1a .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a1a .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a1a .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a1a .kb-teal, :root[data-theme="dark"] .a1a .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a1a .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a1a .kh-teal{ fill:#5DCAA5; }
.a1a .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a1a-teal); }
.a1a .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a1a-teal); }
.a1a .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a1a .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a1a .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a1a .ks-amber{ fill:#854F0B; font-size:13px; }
.a1a .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a1a .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a1a .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a1a .kb-amber, :root[data-theme="dark"] .a1a .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a1a .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a1a .kh-amber{ fill:#EF9F27; }
.a1a .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a1a-amber); }
.a1a .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a1a-amber); }
.a1a .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a1a .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a1a .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a1a .ks-purple{ fill:#534AB7; font-size:13px; }
.a1a .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a1a .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a1a .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a1a .kb-purple, :root[data-theme="dark"] .a1a .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a1a .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a1a .kh-purple{ fill:#AFA9EC; }
.a1a .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a1a-purple); }
.a1a .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a1a-purple); }
.a1a .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
</style>
<defs><marker id="a1a-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a1a-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a1a-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a1a-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a1a-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a1a-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a1a-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker></defs>
<g class="a1a">
<rect x="20" y="90" width="150" height="70" rx="7" class="k-blue"/>
<text x="95.0" y="120.5" text-anchor="middle" class="kb-blue">Client</text>
<text x="95.0" y="138.5" text-anchor="middle" class="ks-blue">app, script, browser</text>
<rect x="220" y="30" width="180" height="190" rx="10" class="k-amber"/>
<text x="310" y="56" text-anchor="middle" class="kh-amber">the API (contract)</text>
<rect x="240" y="72" width="140" height="34" rx="5" class="pnl"/>
<text x="310.0" y="93.5" text-anchor="middle" class="m">GET /books</text>
<rect x="240" y="116" width="140" height="34" rx="5" class="pnl"/>
<text x="310.0" y="137.5" text-anchor="middle" class="m">POST /books</text>
<rect x="240" y="160" width="140" height="34" rx="5" class="pnl"/>
<text x="310.0" y="181.5" text-anchor="middle" class="m">GET /books/{id}</text>
<rect x="450" y="30" width="250" height="190" rx="10" class="zone"/>
<text x="575" y="56" text-anchor="middle" class="c">implementation (hidden)</text>
<rect x="470" y="76" width="210" height="50" rx="7" class="k-teal"/>
<text x="575.0" y="96.5" text-anchor="middle" class="kb-teal">server code</text>
<text x="575.0" y="114.5" text-anchor="middle" class="ks-teal">any language</text>
<rect x="470" y="146" width="210" height="50" rx="7" class="k-purple"/>
<text x="575.0" y="166.5" text-anchor="middle" class="kb-purple">database</text>
<text x="575.0" y="184.5" text-anchor="middle" class="ks-purple">any schema</text>
<line x1="172" y1="112" x2="218" y2="112" class="ar-blue"/>
<line x1="218" y1="140" x2="172" y2="140" class="ar-teal"/>
<line x1="402" y1="101" x2="468" y2="101" class="ar"/>
<line x1="575" y1="128" x2="575" y2="144" class="ln"/>
<text x="195" y="246" text-anchor="middle" class="c">requests</text>
<text x="575" y="246" text-anchor="middle" class="c">free to change, as long as the contract holds</text>
</g>
</svg>
<figcaption>The client depends on the contract, never on the implementation. That separation is the whole point of an API.</figcaption>
</figure>

The client depends only on the contract. It does not know, and should not care, which language the service is written in, which database it uses, or how many servers run it. That separation is what makes APIs useful:

- **Teams work independently.** The team building the mobile app and the team building the backend agree on the API, then work in parallel.
- **Implementations can change.** The backend can move from one database to another, or be rewritten entirely, without breaking any client, as long as the contract holds.
- **Capabilities can be shared.** A company can offer a service, such as payments or maps, to thousands of customers it will never meet.

The flip side is that a published contract is hard to change. Once clients depend on it, removing a field or changing its meaning breaks them. Chapter 11 covers how APIs evolve without breaking their users.

### A restaurant analogy

A restaurant menu is an API. It lists what you can order (the operations), what you must specify ("how would you like your steak?", the parameters), and what you will receive (the response). You never enter the kitchen. The kitchen can change its suppliers, its staff, and its recipes; as long as the menu stays the same, you, the client, are unaffected. If you order something not on the menu, the waiter says no: an error response.

## Kinds of API

<figure class="diagram">
<svg viewBox="0 0 720 250" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Three kinds of API: a library API is a function call inside the same program; an operating system API is a system call into the kernel; a web API is a request sent over the network to another computer, usually with HTTP." xmlns="http://www.w3.org/2000/svg">
<style>
.a1b{ font-family:var(--sans),sans-serif; }
.a1b .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a1b .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a1b .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a1b .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a1b .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a1b .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a1b .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a1b .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a1b .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a1b .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a1b .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a1b .s{ fill:var(--text-dim); font-size:13px; }
.a1b .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a1b .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a1b .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a1b .c{ fill:var(--text-faint); font-size:12.5px; }
.a1b .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a1b .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a1b .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a1b .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a1b-a); }
.a1b .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a1b-a); marker-start:url(#a1b-s); }
.a1b .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a1b-g); }
.a1b .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a1b-a); }
.a1b .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a1b .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a1b .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a1b .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a1b .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a1b .ks-blue{ fill:#185FA5; font-size:13px; }
.a1b .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a1b .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a1b .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a1b .kb-blue, :root[data-theme="dark"] .a1b .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a1b .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a1b .kh-blue{ fill:#85B7EB; }
.a1b .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a1b-blue); }
.a1b .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a1b-blue); }
.a1b .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a1b .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a1b .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a1b .ks-teal{ fill:#0F6E56; font-size:13px; }
.a1b .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a1b .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a1b .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a1b .kb-teal, :root[data-theme="dark"] .a1b .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a1b .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a1b .kh-teal{ fill:#5DCAA5; }
.a1b .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a1b-teal); }
.a1b .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a1b-teal); }
.a1b .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a1b .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a1b .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a1b .ks-purple{ fill:#534AB7; font-size:13px; }
.a1b .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a1b .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a1b .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a1b .kb-purple, :root[data-theme="dark"] .a1b .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a1b .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a1b .kh-purple{ fill:#AFA9EC; }
.a1b .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a1b-purple); }
.a1b .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a1b-purple); }
.a1b .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a1b .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a1b .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a1b .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a1b .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a1b .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a1b .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a1b .kb-gray, :root[data-theme="dark"] .a1b .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a1b .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a1b .kh-gray{ fill:#B4B2A9; }
.a1b .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a1b-gray); }
.a1b .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a1b-gray); }
.a1b .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a1b-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a1b-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a1b-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a1b-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a1b-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a1b-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a1b-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a1b">
<rect x="20" y="20" width="216" height="44" rx="7" class="k-blue"/>
<text x="128.0" y="46.5" text-anchor="middle" class="kb-blue">Library API</text>
<rect x="20" y="76" width="216" height="40" rx="5" class="pnl"/>
<text x="128.0" y="100.5" text-anchor="middle" class="m">json.dumps(obj)</text>
<text x="128" y="146" text-anchor="middle" class="s">a function call</text>
<text x="128" y="168" text-anchor="middle" class="c">same process</text>
<rect x="252" y="20" width="216" height="44" rx="7" class="k-purple"/>
<text x="360.0" y="46.5" text-anchor="middle" class="kb-purple">OS API</text>
<rect x="252" y="76" width="216" height="40" rx="5" class="pnl"/>
<text x="360.0" y="100.5" text-anchor="middle" class="m">open("notes.txt")</text>
<text x="360" y="146" text-anchor="middle" class="s">a system call</text>
<text x="360" y="168" text-anchor="middle" class="c">same machine</text>
<rect x="484" y="20" width="216" height="44" rx="7" class="k-teal"/>
<text x="592.0" y="46.5" text-anchor="middle" class="kb-teal">Web API</text>
<rect x="484" y="76" width="216" height="40" rx="5" class="pnl"/>
<text x="592.0" y="100.5" text-anchor="middle" class="m">GET /books/42</text>
<text x="592" y="146" text-anchor="middle" class="s">an HTTP request</text>
<text x="592" y="168" text-anchor="middle" class="c">across the network</text>
<line x1="40" y1="200" x2="680" y2="200" class="ar-gray"/>
<text x="60" y="226" text-anchor="start" class="c">faster, tightly coupled</text>
<text x="680" y="226" text-anchor="end" class="c">slower, loosely coupled</text>
</g>
</svg>
<figcaption>All three are contracts. This book is about the third kind: web APIs, which connect separate programs over a network.</figcaption>
</figure>

- A **library API** is a set of functions or classes you call inside your own program, such as Python's `json` module. Calls are fast and fail only with exceptions.
- An **operating system API** lets programs ask the kernel for services: open a file, create a process, send network data. Python's `open()` eventually becomes a system call.
- A **web API** is offered over a network, almost always using HTTP. The client and server are separate programs, often owned by different organisations, running on different machines.

Web APIs are slower and less reliable than function calls, because a network sits in between: requests can be delayed, lost, or answered by a server that is overloaded or down. Much of good API design, and much of this book, is about dealing with that honestly.

## Web APIs are everywhere

<figure class="diagram">
<svg viewBox="0 0 720 290" style="width:100%;height:auto;max-width:720px" role="img" aria-label="One food-delivery app calls many APIs: the mobile app calls the company&#x27;s own backend API, which in turn calls a payments API, a maps API, an SMS API and an email API run by other companies." xmlns="http://www.w3.org/2000/svg">
<style>
.a1c{ font-family:var(--sans),sans-serif; }
.a1c .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a1c .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a1c .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a1c .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a1c .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a1c .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a1c .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a1c .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a1c .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a1c .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a1c .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a1c .s{ fill:var(--text-dim); font-size:13px; }
.a1c .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a1c .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a1c .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a1c .c{ fill:var(--text-faint); font-size:12.5px; }
.a1c .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a1c .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a1c .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a1c .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a1c-a); }
.a1c .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a1c-a); marker-start:url(#a1c-s); }
.a1c .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a1c-g); }
.a1c .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a1c-a); }
.a1c .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a1c .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a1c .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a1c .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a1c .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a1c .ks-blue{ fill:#185FA5; font-size:13px; }
.a1c .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a1c .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a1c .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a1c .kb-blue, :root[data-theme="dark"] .a1c .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a1c .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a1c .kh-blue{ fill:#85B7EB; }
.a1c .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a1c-blue); }
.a1c .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a1c-blue); }
.a1c .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a1c .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a1c .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a1c .ks-teal{ fill:#0F6E56; font-size:13px; }
.a1c .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a1c .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a1c .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a1c .kb-teal, :root[data-theme="dark"] .a1c .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a1c .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a1c .kh-teal{ fill:#5DCAA5; }
.a1c .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a1c-teal); }
.a1c .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a1c-teal); }
.a1c .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a1c .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a1c .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a1c .ks-amber{ fill:#854F0B; font-size:13px; }
.a1c .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a1c .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a1c .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a1c .kb-amber, :root[data-theme="dark"] .a1c .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a1c .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a1c .kh-amber{ fill:#EF9F27; }
.a1c .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a1c-amber); }
.a1c .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a1c-amber); }
.a1c .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
</style>
<defs><marker id="a1c-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a1c-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a1c-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a1c-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a1c-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a1c-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker></defs>
<g class="a1c">
<rect x="20" y="110" width="140" height="60" rx="7" class="k-blue"/>
<text x="90.0" y="135.5" text-anchor="middle" class="kb-blue">mobile app</text>
<text x="90.0" y="153.5" text-anchor="middle" class="ks-blue">phone</text>
<rect x="230" y="100" width="180" height="80" rx="7" class="k-teal"/>
<text x="320.0" y="135.5" text-anchor="middle" class="kb-teal">company backend</text>
<text x="320.0" y="153.5" text-anchor="middle" class="ks-teal">its own API</text>
<line x1="162" y1="140" x2="228" y2="140" class="ar-blue"/>
<text x="195" y="128" text-anchor="middle" class="c">HTTPS</text>
<rect x="520" y="20" width="180" height="48" rx="7" class="k-amber"/>
<text x="610.0" y="48.5" text-anchor="middle" class="kb-amber">payments API</text>
<line x1="412" y1="140" x2="518" y2="44" class="ar-teal"/>
<rect x="520" y="86" width="180" height="48" rx="7" class="k-amber"/>
<text x="610.0" y="114.5" text-anchor="middle" class="kb-amber">maps API</text>
<line x1="412" y1="140" x2="518" y2="110" class="ar-teal"/>
<rect x="520" y="152" width="180" height="48" rx="7" class="k-amber"/>
<text x="610.0" y="180.5" text-anchor="middle" class="kb-amber">SMS API</text>
<line x1="412" y1="140" x2="518" y2="176" class="ar-teal"/>
<rect x="520" y="218" width="180" height="48" rx="7" class="k-amber"/>
<text x="610.0" y="246.5" text-anchor="middle" class="kb-amber">email API</text>
<line x1="412" y1="140" x2="518" y2="242" class="ar-teal"/>
<text x="610" y="284" text-anchor="middle" class="c">third-party services, paid per call</text>
</g>
</svg>
<figcaption>Modern software is assembled from APIs. A single tap in an app can trigger a dozen API calls behind the scenes.</figcaption>
</figure>

A typical app is built from APIs. Its own frontend talks to its own backend through an API, and the backend in turn uses third-party APIs for payments, maps, messaging, email, identity, and storage. Companies such as Stripe, Twilio, and the major cloud providers exist largely to sell API calls. Inside large organisations, hundreds of small services, often called **microservices**, talk to each other the same way.

Two broad audiences use web APIs:

- **Internal APIs** connect a company's own applications and services. The company controls both sides.
- **Public APIs** (or partner APIs) are offered to outside developers. Their contracts must be especially stable and well documented, and their security must assume that clients are untrusted.

## API styles

Web APIs come in several styles. They differ in how requests and responses are shaped, not in what they achieve.

<figure class="diagram">
<svg viewBox="0 0 720 300" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Common web API styles: REST with resources and HTTP methods; GraphQL with one endpoint and client-written queries; gRPC with remote procedure calls and binary messages; webhooks where the server calls the client when an event happens; and older SOAP with XML envelopes." xmlns="http://www.w3.org/2000/svg">
<style>
.a1d{ font-family:var(--sans),sans-serif; }
.a1d .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a1d .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a1d .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a1d .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a1d .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a1d .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a1d .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a1d .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a1d .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a1d .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a1d .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a1d .s{ fill:var(--text-dim); font-size:13px; }
.a1d .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a1d .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a1d .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a1d .c{ fill:var(--text-faint); font-size:12.5px; }
.a1d .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a1d .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a1d .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a1d .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a1d-a); }
.a1d .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a1d-a); marker-start:url(#a1d-s); }
.a1d .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a1d-g); }
.a1d .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a1d-a); }
.a1d .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a1d .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a1d .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a1d .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a1d .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a1d .ks-blue{ fill:#185FA5; font-size:13px; }
.a1d .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a1d .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a1d .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a1d .kb-blue, :root[data-theme="dark"] .a1d .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a1d .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a1d .kh-blue{ fill:#85B7EB; }
.a1d .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a1d-blue); }
.a1d .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a1d-blue); }
.a1d .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a1d .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a1d .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a1d .ks-teal{ fill:#0F6E56; font-size:13px; }
.a1d .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a1d .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a1d .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a1d .kb-teal, :root[data-theme="dark"] .a1d .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a1d .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a1d .kh-teal{ fill:#5DCAA5; }
.a1d .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a1d-teal); }
.a1d .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a1d-teal); }
.a1d .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a1d .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a1d .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a1d .ks-amber{ fill:#854F0B; font-size:13px; }
.a1d .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a1d .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a1d .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a1d .kb-amber, :root[data-theme="dark"] .a1d .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a1d .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a1d .kh-amber{ fill:#EF9F27; }
.a1d .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a1d-amber); }
.a1d .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a1d-amber); }
.a1d .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a1d .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a1d .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a1d .ks-purple{ fill:#534AB7; font-size:13px; }
.a1d .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a1d .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a1d .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a1d .kb-purple, :root[data-theme="dark"] .a1d .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a1d .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a1d .kh-purple{ fill:#AFA9EC; }
.a1d .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a1d-purple); }
.a1d .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a1d-purple); }
.a1d .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a1d .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a1d .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a1d .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a1d .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a1d .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a1d .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a1d .kb-gray, :root[data-theme="dark"] .a1d .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a1d .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a1d .kh-gray{ fill:#B4B2A9; }
.a1d .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a1d-gray); }
.a1d .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a1d-gray); }
.a1d .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a1d-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a1d-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a1d-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a1d-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a1d-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a1d-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a1d-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a1d-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a1d">
<rect x="20" y="20" width="120" height="42" rx="7" class="k-teal"/>
<text x="80.0" y="45.5" text-anchor="middle" class="kb-teal">REST</text>
<text x="160" y="46" text-anchor="start" class="s">resources + HTTP methods</text>
<rect x="430" y="24" width="180" height="34" rx="5" class="pnl"/>
<text x="520.0" y="45.5" text-anchor="middle" class="m">GET /books/42</text>
<text x="690" y="46" text-anchor="end" class="c">Ch 5 to 7</text>
<rect x="20" y="74" width="120" height="42" rx="7" class="k-purple"/>
<text x="80.0" y="99.5" text-anchor="middle" class="kb-purple">GraphQL</text>
<text x="160" y="100" text-anchor="start" class="s">one endpoint, client picks fields</text>
<rect x="430" y="78" width="180" height="34" rx="5" class="pnl"/>
<text x="520.0" y="99.5" text-anchor="middle" class="m">POST /graphql</text>
<text x="690" y="100" text-anchor="end" class="c">Ch 12</text>
<rect x="20" y="128" width="120" height="42" rx="7" class="k-blue"/>
<text x="80.0" y="153.5" text-anchor="middle" class="kb-blue">gRPC</text>
<text x="160" y="154" text-anchor="start" class="s">remote functions, binary messages</text>
<rect x="430" y="132" width="180" height="34" rx="5" class="pnl"/>
<text x="520.0" y="153.5" text-anchor="middle" class="m">Library.GetBook()</text>
<text x="690" y="154" text-anchor="end" class="c">Ch 12</text>
<rect x="20" y="182" width="120" height="42" rx="7" class="k-amber"/>
<text x="80.0" y="207.5" text-anchor="middle" class="kb-amber">Webhooks</text>
<text x="160" y="208" text-anchor="start" class="s">the server calls you on events</text>
<rect x="430" y="186" width="180" height="34" rx="5" class="pnl"/>
<text x="520.0" y="207.5" text-anchor="middle" class="m">POST /your/hook</text>
<text x="690" y="208" text-anchor="end" class="c">Ch 12</text>
<rect x="20" y="236" width="120" height="42" rx="7" class="k-gray"/>
<text x="80.0" y="261.5" text-anchor="middle" class="kb-gray">SOAP</text>
<text x="160" y="262" text-anchor="start" class="s">XML envelopes, older systems</text>
<rect x="430" y="240" width="180" height="34" rx="5" class="pnl"/>
<text x="520.0" y="261.5" text-anchor="middle" class="m">&lt;soap:Envelope&gt;</text>
<text x="690" y="262" text-anchor="end" class="c">legacy</text>
</g>
</svg>
<figcaption>API styles differ in how requests are shaped, but all of them move structured messages between programs.</figcaption>
</figure>

- **REST** organises an API around **resources**, such as books or orders, each with a URL, and uses the standard HTTP methods (`GET`, `POST`, `PUT`, `DELETE`) on them. It is the most common style for public web APIs and is the focus of Part II.
- **GraphQL** exposes a single endpoint and lets the client write a query that names exactly the fields it wants.
- **gRPC** makes remote calls look like local function calls and sends compact binary messages over HTTP/2. It is popular between internal services.
- **Webhooks** reverse the direction: the server calls an endpoint on the client's side when something happens, such as a payment succeeding.
- **SOAP** wraps every message in an XML envelope. It is found in older enterprise and government systems.

Chapter 12 compares REST, GraphQL, gRPC, and webhooks in detail.

## The vocabulary

| Term | Meaning |
|---|---|
| **Client** | The program that sends requests: an app, a script, a browser, another service |
| **Server** | The program that receives requests and sends responses |
| **Endpoint** | One address an API exposes, such as `GET /books/{id}` |
| **Request / response** | One message from client to server, and its answer |
| **Resource** | A thing the API lets you work with, such as a book or an order |
| **Payload** | The data in the body of a request or response, usually JSON |
| **Consumer / provider** | Another name for the client side and the server side of an API |
| **SDK** | A library that wraps an API in functions for one programming language |

## Reading the diagrams

The diagrams in this book use colour consistently:

| Colour | Means |
|---|---|
| Blue | Clients: apps, scripts, browsers |
| Teal | Servers and APIs |
| Purple | Data and storage |
| Amber | Messages on the wire, and contracts |
| Gray | Infrastructure in between: load balancers, gateways, servers like uvicorn |
| Green / red | Success and failure; red also marks attackers |

## Summary

- An **API** is a contract that lets one program use another without knowing how it is built.
- **Web APIs** are offered over a network, usually HTTP, and must cope with delays and failures.
- APIs let teams work **independently**, let implementations **change**, and let capabilities be **shared**; published contracts are **hard to change**.
- Main styles: **REST**, **GraphQL**, **gRPC**, **webhooks**, and legacy **SOAP**.

The next chapter sets up the lab and builds your first API.
