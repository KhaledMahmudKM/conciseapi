# Chapter 5: Designing REST APIs

**REST** (Representational State Transfer) is an architectural style described by Roy Fielding in his 2000 doctoral dissertation, based on how the web itself works. In everyday use, "REST API" means something more modest: an HTTP API organised around **resources**, each with a URL, manipulated with the standard HTTP methods, and exchanging representations such as JSON. This chapter turns that idea into concrete design rules, using the Library API that you will build in Chapter 6.

## Resources

A **resource** is anything worth naming: a book, an author, an order, a user's profile, even a search. Design starts by listing the resources and how they relate, not the operations.

<figure class="diagram">
<svg viewBox="0 0 720 300" style="width:100%;height:auto;max-width:720px" role="img" aria-label="A resource tree for the Library API: collections /books and /authors; individual items /books/{id} and /authors/{id}; and nested collections /books/{id}/reviews and /authors/{id}/books for related resources." xmlns="http://www.w3.org/2000/svg">
<style>
.a5a{ font-family:var(--sans),sans-serif; }
.a5a .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a5a .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a5a .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a5a .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a5a .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a5a .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a5a .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a5a .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a5a .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a5a .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a5a .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a5a .s{ fill:var(--text-dim); font-size:13px; }
.a5a .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a5a .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a5a .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a5a .c{ fill:var(--text-faint); font-size:12.5px; }
.a5a .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a5a .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a5a .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a5a .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a5a-a); }
.a5a .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a5a-a); marker-start:url(#a5a-s); }
.a5a .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a5a-g); }
.a5a .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a5a-a); }
.a5a .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a5a .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a5a .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a5a .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a5a .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a5a .ks-blue{ fill:#185FA5; font-size:13px; }
.a5a .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a5a .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5a .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a5a .kb-blue, :root[data-theme="dark"] .a5a .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a5a .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a5a .kh-blue{ fill:#85B7EB; }
.a5a .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a5a-blue); }
.a5a .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5a-blue); }
.a5a .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a5a .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a5a .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a5a .ks-teal{ fill:#0F6E56; font-size:13px; }
.a5a .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a5a .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5a .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a5a .kb-teal, :root[data-theme="dark"] .a5a .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a5a .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a5a .kh-teal{ fill:#5DCAA5; }
.a5a .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a5a-teal); }
.a5a .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5a-teal); }
.a5a .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a5a .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a5a .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a5a .ks-purple{ fill:#534AB7; font-size:13px; }
.a5a .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a5a .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5a .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a5a .kb-purple, :root[data-theme="dark"] .a5a .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a5a .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a5a .kh-purple{ fill:#AFA9EC; }
.a5a .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a5a-purple); }
.a5a .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5a-purple); }
.a5a .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a5a .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a5a .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a5a .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a5a .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a5a .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5a .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a5a .kb-gray, :root[data-theme="dark"] .a5a .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a5a .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a5a .kh-gray{ fill:#B4B2A9; }
.a5a .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a5a-gray); }
.a5a .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5a-gray); }
.a5a .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a5a-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a5a-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a5a-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a5a-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a5a-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a5a-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a5a-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a5a">
<rect x="290" y="16" width="140" height="40" rx="7" class="k-gray"/>
<text x="360.0" y="40.5" text-anchor="middle" class="km-gray">/  (API root)</text>
<rect x="110" y="96" width="170" height="44" rx="7" class="k-teal"/>
<text x="195.0" y="122.5" text-anchor="middle" class="km-teal">/books</text>
<rect x="440" y="96" width="170" height="44" rx="7" class="k-teal"/>
<text x="525.0" y="122.5" text-anchor="middle" class="km-teal">/authors</text>
<rect x="110" y="176" width="170" height="44" rx="7" class="k-blue"/>
<text x="195.0" y="202.5" text-anchor="middle" class="km-blue">/books/{id}</text>
<rect x="440" y="176" width="170" height="44" rx="7" class="k-blue"/>
<text x="525.0" y="202.5" text-anchor="middle" class="km-blue">/authors/{id}</text>
<rect x="100" y="248" width="190" height="40" rx="7" class="k-purple"/>
<text x="195.0" y="272.5" text-anchor="middle" class="km-purple">/books/{id}/reviews</text>
<rect x="430" y="248" width="190" height="40" rx="7" class="k-purple"/>
<text x="525.0" y="272.5" text-anchor="middle" class="km-purple">/authors/{id}/books</text>
<line x1="330" y1="56" x2="200" y2="94" class="ln"/>
<line x1="390" y1="56" x2="520" y2="94" class="ln"/>
<line x1="195" y1="140" x2="195" y2="174" class="ln"/>
<line x1="525" y1="140" x2="525" y2="174" class="ln"/>
<line x1="195" y1="220" x2="195" y2="246" class="ln"/>
<line x1="525" y1="220" x2="525" y2="246" class="ln"/>
<text x="20" y="122" text-anchor="start" class="kh-teal">collections</text>
<text x="20" y="202" text-anchor="start" class="kh-blue">items</text>
<text x="20" y="272" text-anchor="start" class="kh-purple">nested</text>
</g>
</svg>
<figcaption>Nouns, not verbs. Each URL names a thing, and the HTTP method says what to do with it.</figcaption>
</figure>

Rules that keep URLs predictable:

- **Use nouns, not verbs.** `/books`, not `/getBooks`. The HTTP method is the verb.
- **Use plural collection names.** `/books` is the collection; `/books/42` is one item in it.
- **Nest only for real ownership, and not deeply.** `/books/42/reviews` makes sense because a review belongs to a book. Avoid more than two levels; `/authors/7/books/42/reviews/3` is better expressed as `/reviews/3`.
- **Use lowercase and hyphens** for multi-word names: `/reading-lists`, not `/ReadingLists` or `/reading_lists`.
- **Keep IDs opaque.** Clients should treat `42` as a label, not do arithmetic on it. Many APIs use random identifiers (UUIDs) so that IDs reveal nothing and cannot be guessed. Chapter 9 shows why guessable IDs are dangerous when authorization is weak.
- **No file extensions or implementation details** in URLs: not `/books.json`, not `/cgi-bin/books.php`.

## Methods on resources

With resources named, the HTTP methods from Chapter 3 provide the operations.

<figure class="diagram">
<svg viewBox="0 0 720 280" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Methods on a collection and on an item. On the collection /books, GET lists books and POST creates a new one. On an item /books/42, GET reads it, PUT replaces it, PATCH changes some fields, and DELETE removes it." xmlns="http://www.w3.org/2000/svg">
<style>
.a5b{ font-family:var(--sans),sans-serif; }
.a5b .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a5b .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a5b .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a5b .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a5b .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a5b .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a5b .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a5b .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a5b .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a5b .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a5b .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a5b .s{ fill:var(--text-dim); font-size:13px; }
.a5b .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a5b .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a5b .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a5b .c{ fill:var(--text-faint); font-size:12.5px; }
.a5b .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a5b .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a5b .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a5b .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a5b-a); }
.a5b .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a5b-a); marker-start:url(#a5b-s); }
.a5b .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a5b-g); }
.a5b .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a5b-a); }
.a5b .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a5b .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a5b .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a5b .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a5b .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a5b .ks-blue{ fill:#185FA5; font-size:13px; }
.a5b .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a5b .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5b .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a5b .kb-blue, :root[data-theme="dark"] .a5b .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a5b .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a5b .kh-blue{ fill:#85B7EB; }
.a5b .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a5b-blue); }
.a5b .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5b-blue); }
.a5b .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a5b .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a5b .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a5b .ks-teal{ fill:#0F6E56; font-size:13px; }
.a5b .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a5b .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5b .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a5b .kb-teal, :root[data-theme="dark"] .a5b .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a5b .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a5b .kh-teal{ fill:#5DCAA5; }
.a5b .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a5b-teal); }
.a5b .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5b-teal); }
.a5b .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a5b .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a5b .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a5b .ks-green{ fill:#3B6D11; font-size:13px; }
.a5b .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a5b .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5b .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a5b .kb-green, :root[data-theme="dark"] .a5b .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a5b .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a5b .kh-green{ fill:#97C459; }
.a5b .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a5b-green); }
.a5b .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5b-green); }
.a5b .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
</style>
<defs><marker id="a5b-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a5b-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a5b-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a5b-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a5b-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a5b-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker></defs>
<g class="a5b">
<rect x="20" y="20" width="200" height="110" rx="7" class="k-teal"/>
<text x="120.0" y="70.5" text-anchor="middle" class="kb-teal">collection</text>
<text x="120.0" y="88.5" text-anchor="middle" class="km-teal">/books</text>
<rect x="240" y="26" width="150" height="40" rx="5" class="pnl"/>
<text x="315.0" y="50.5" text-anchor="middle" class="m">GET /books</text>
<text x="410" y="51" text-anchor="start" class="s">list books (filter, sort, page)</text>
<text x="700" y="51" text-anchor="end" class="kh-green">200</text>
<rect x="240" y="78" width="150" height="40" rx="5" class="pnl"/>
<text x="315.0" y="102.5" text-anchor="middle" class="m">POST /books</text>
<text x="410" y="103" text-anchor="start" class="s">create a book</text>
<text x="700" y="103" text-anchor="end" class="kh-green">201 + Location</text>
<rect x="20" y="150" width="200" height="110" rx="7" class="k-blue"/>
<text x="120.0" y="200.5" text-anchor="middle" class="kb-blue">item</text>
<text x="120.0" y="218.5" text-anchor="middle" class="km-blue">/books/42</text>
<rect x="240" y="150" width="150" height="24" rx="4" class="pnl"/>
<text x="315.0" y="166.5" text-anchor="middle" class="m">GET</text>
<text x="410" y="167" text-anchor="start" class="s">read the book</text>
<text x="700" y="167" text-anchor="end" class="kh-green">200</text>
<rect x="240" y="178" width="150" height="24" rx="4" class="pnl"/>
<text x="315.0" y="194.5" text-anchor="middle" class="m">PUT</text>
<text x="410" y="195" text-anchor="start" class="s">replace it entirely</text>
<text x="700" y="195" text-anchor="end" class="kh-green">200</text>
<rect x="240" y="206" width="150" height="24" rx="4" class="pnl"/>
<text x="315.0" y="222.5" text-anchor="middle" class="m">PATCH</text>
<text x="410" y="223" text-anchor="start" class="s">change some fields</text>
<text x="700" y="223" text-anchor="end" class="kh-green">200</text>
<rect x="240" y="234" width="150" height="24" rx="4" class="pnl"/>
<text x="315.0" y="250.5" text-anchor="middle" class="m">DELETE</text>
<text x="410" y="251" text-anchor="start" class="s">remove it</text>
<text x="700" y="251" text-anchor="end" class="kh-green">204</text>
</g>
</svg>
<figcaption>Six combinations cover most of what an API does. Learn them once and every REST API looks familiar.</figcaption>
</figure>

| Request | Meaning | Success |
|---|---|---|
| `GET /books` | List books | `200` with a page of books |
| `POST /books` | Create a book | `201` with the book and a `Location` header |
| `GET /books/42` | Read book 42 | `200` with the book |
| `PUT /books/42` | Replace book 42 with the body | `200` with the book |
| `PATCH /books/42` | Change some fields of book 42 | `200` with the book |
| `DELETE /books/42` | Delete book 42 | `204` with no body |

`PUT` versus `PATCH` is a frequent source of confusion. `PUT` sends the **complete** new state; any field left out is reset. `PATCH` sends only the **changes**. Most APIs use `PATCH` for updates because clients rarely want to resend everything.

### Status codes and errors

Use status codes precisely, because clients act on them automatically:

- `404` when the resource does not exist, `422` when the request body is invalid, `409` when it conflicts with the current state (a duplicate ISBN, for example).
- `401` when credentials are missing or wrong, `403` when they are valid but not allowed.
- Never return `200` with an error inside the body (`{"success": false}`). Proxies, monitoring tools, and client libraries all rely on the status code.

Every error should also have a body that explains it, in **one consistent format** across the whole API. Chapter 6 uses the standard format for this, **problem details**.

## Actions that are not CRUD

Some operations do not map neatly onto create, read, update, delete. Cancelling an order, resending an email, or approving a request are typical.

<figure class="diagram">
<svg viewBox="0 0 720 250" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Three ways to model an action that is not plain create, read, update or delete, such as cancelling an order: change a status field with PATCH, create a cancellation resource with POST, or as a last resort post to an action sub-resource." xmlns="http://www.w3.org/2000/svg">
<style>
.a5d{ font-family:var(--sans),sans-serif; }
.a5d .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a5d .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a5d .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a5d .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a5d .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a5d .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a5d .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a5d .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a5d .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a5d .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a5d .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a5d .s{ fill:var(--text-dim); font-size:13px; }
.a5d .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a5d .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a5d .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a5d .c{ fill:var(--text-faint); font-size:12.5px; }
.a5d .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a5d .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a5d .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a5d .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a5d-a); }
.a5d .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a5d-a); marker-start:url(#a5d-s); }
.a5d .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a5d-g); }
.a5d .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a5d-a); }
.a5d .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a5d .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a5d .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a5d .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a5d .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a5d .ks-teal{ fill:#0F6E56; font-size:13px; }
.a5d .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a5d .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5d .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a5d .kb-teal, :root[data-theme="dark"] .a5d .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a5d .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a5d .kh-teal{ fill:#5DCAA5; }
.a5d .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a5d-teal); }
.a5d .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5d-teal); }
.a5d .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a5d .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a5d .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a5d .ks-amber{ fill:#854F0B; font-size:13px; }
.a5d .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a5d .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5d .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a5d .kb-amber, :root[data-theme="dark"] .a5d .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a5d .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a5d .kh-amber{ fill:#EF9F27; }
.a5d .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a5d-amber); }
.a5d .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5d-amber); }
.a5d .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a5d .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a5d .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a5d .ks-green{ fill:#3B6D11; font-size:13px; }
.a5d .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a5d .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5d .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a5d .kb-green, :root[data-theme="dark"] .a5d .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a5d .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a5d .kh-green{ fill:#97C459; }
.a5d .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a5d-green); }
.a5d .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5d-green); }
.a5d .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a5d .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a5d .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a5d .ks-red{ fill:#A32D2D; font-size:13px; }
.a5d .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a5d .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5d .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a5d .kb-red, :root[data-theme="dark"] .a5d .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a5d .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a5d .kh-red{ fill:#F09595; }
.a5d .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a5d-red); }
.a5d .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5d-red); }
.a5d .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
</style>
<defs><marker id="a5d-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a5d-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a5d-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a5d-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a5d-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a5d-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a5d-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker></defs>
<g class="a5d">
<rect x="20" y="30" width="224" height="110" rx="7" class="k-green"/>
<text x="132.0" y="63.5" text-anchor="middle" class="km-green">PATCH /orders/42</text>
<text x="132.0" y="89.5" text-anchor="middle" class="km-green">{"status": "cancelled"}</text>
<text x="132.0" y="115.5" text-anchor="middle" class="kb-green">state change: preferred</text>
<rect x="248" y="30" width="224" height="110" rx="7" class="k-teal"/>
<text x="360.0" y="63.5" text-anchor="middle" class="km-teal">POST /orders/42/cancellations</text>
<text x="360.0" y="89.5" text-anchor="middle" class="km-teal">{"reason": "late"}</text>
<text x="360.0" y="115.5" text-anchor="middle" class="kb-teal">the action is a thing too</text>
<rect x="476" y="30" width="224" height="110" rx="7" class="k-amber"/>
<text x="588.0" y="63.5" text-anchor="middle" class="km-amber">POST /orders/42/cancel</text>
<text x="588.0" y="89.5" text-anchor="middle" class="km-amber">(no body)</text>
<text x="588.0" y="115.5" text-anchor="middle" class="kb-amber">RPC-style: acceptable</text>
<rect x="20" y="170" width="680" height="50" rx="7" class="k-red"/>
<text x="360.0" y="199.5" text-anchor="middle" class="ks-red">Avoid verbs as resources like  GET /getOrder?id=42  or  POST /deleteBook</text>
</g>
</svg>
<figcaption>Most actions are state changes in disguise. When one really is not, a clearly named action endpoint is fine.</figcaption>
</figure>

First, look for a state change in disguise: cancelling an order is usually `PATCH /orders/42` with `{"status": "cancelled"}`. Second, consider making the action a resource of its own: `POST /orders/42/cancellations` creates a cancellation record, which may carry a reason and a timestamp. Only if neither fits, use an action endpoint such as `POST /orders/42/cancel`. It is not "pure" REST, but it is clear, and clarity beats purity.

## Collections: filtering, sorting, pagination

Lists need controls, and these belong in the **query string**:

| Need | Convention | Example |
|---|---|---|
| Filter | One parameter per field | `/books?author=austen&year=1815` |
| Sort | A `sort` parameter, `-` for descending | `/books?sort=-year` |
| Paginate | `limit` with `offset`, or a cursor | `/books?limit=20&offset=40` |
| Choose fields | A `fields` parameter | `/books?fields=id,title` |
| Search | A `q` parameter | `/books?q=dune` |

**Always paginate collections**, with a sensible default and a **maximum** page size enforced by the server. A collection that returns everything works in testing with ten rows and fails in production with ten million.

<figure class="diagram">
<svg viewBox="0 0 720 290" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Offset pagination versus cursor pagination. Offset pagination asks for items 20 to 29 with offset and limit; if a new item is inserted meanwhile, one item is shown twice. Cursor pagination asks for items after an opaque cursor that marks the last item seen, so insertions do not shift pages." xmlns="http://www.w3.org/2000/svg">
<style>
.a5e{ font-family:var(--sans),sans-serif; }
.a5e .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a5e .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a5e .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a5e .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a5e .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a5e .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a5e .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a5e .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a5e .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a5e .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a5e .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a5e .s{ fill:var(--text-dim); font-size:13px; }
.a5e .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a5e .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a5e .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a5e .c{ fill:var(--text-faint); font-size:12.5px; }
.a5e .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a5e .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a5e .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a5e .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a5e-a); }
.a5e .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a5e-a); marker-start:url(#a5e-s); }
.a5e .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a5e-g); }
.a5e .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a5e-a); }
.a5e .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a5e .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a5e .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a5e .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a5e .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a5e .ks-blue{ fill:#185FA5; font-size:13px; }
.a5e .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a5e .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5e .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a5e .kb-blue, :root[data-theme="dark"] .a5e .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a5e .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a5e .kh-blue{ fill:#85B7EB; }
.a5e .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a5e-blue); }
.a5e .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5e-blue); }
.a5e .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a5e .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a5e .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a5e .ks-teal{ fill:#0F6E56; font-size:13px; }
.a5e .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a5e .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5e .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a5e .kb-teal, :root[data-theme="dark"] .a5e .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a5e .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a5e .kh-teal{ fill:#5DCAA5; }
.a5e .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a5e-teal); }
.a5e .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5e-teal); }
.a5e .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a5e .k-coral{ fill:#FAECE7; stroke:#D85A30; stroke-width:1.6; }
.a5e .kb-coral{ fill:#712B13; font-size:13px; font-weight:700; }
.a5e .ks-coral{ fill:#993C1D; font-size:13px; }
.a5e .km-coral{ fill:#712B13; font-size:12.5px; font-family:var(--mono),monospace; }
.a5e .kh-coral{ fill:#993C1D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5e .k-coral{ fill:#712B13; stroke:#F0997B; }
:root[data-theme="dark"] .a5e .kb-coral, :root[data-theme="dark"] .a5e .km-coral{ fill:#FAECE7; }
:root[data-theme="dark"] .a5e .ks-coral{ fill:#F5C4B3; }
:root[data-theme="dark"] .a5e .kh-coral{ fill:#F0997B; }
.a5e .ar-coral{ stroke:#D85A30; stroke-width:2; fill:none; marker-end:url(#a5e-coral); }
.a5e .ad-coral{ stroke:#D85A30; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5e-coral); }
.a5e .ln-coral{ stroke:#D85A30; stroke-width:2; fill:none; }
.a5e .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a5e .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a5e .ks-red{ fill:#A32D2D; font-size:13px; }
.a5e .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a5e .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5e .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a5e .kb-red, :root[data-theme="dark"] .a5e .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a5e .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a5e .kh-red{ fill:#F09595; }
.a5e .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a5e-red); }
.a5e .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5e-red); }
.a5e .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
</style>
<defs><marker id="a5e-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a5e-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a5e-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a5e-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a5e-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a5e-coral" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#D85A30"/></marker><marker id="a5e-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker></defs>
<g class="a5e">
<text x="20" y="26" text-anchor="start" class="kh-blue">offset: ?offset=5&amp;limit=5</text>
<rect x="20" y="40" width="30" height="30" rx="4" class="k-blue"/>
<text x="35.0" y="59.5" text-anchor="middle" class="km-blue">1</text>
<rect x="54" y="40" width="30" height="30" rx="4" class="k-blue"/>
<text x="69.0" y="59.5" text-anchor="middle" class="km-blue">2</text>
<rect x="88" y="40" width="30" height="30" rx="4" class="k-blue"/>
<text x="103.0" y="59.5" text-anchor="middle" class="km-blue">3</text>
<rect x="122" y="40" width="30" height="30" rx="4" class="k-blue"/>
<text x="137.0" y="59.5" text-anchor="middle" class="km-blue">4</text>
<rect x="156" y="40" width="30" height="30" rx="4" class="k-blue"/>
<text x="171.0" y="59.5" text-anchor="middle" class="km-blue">5</text>
<rect x="190" y="40" width="30" height="30" rx="4" class="pnl"/>
<text x="205.0" y="59.5" text-anchor="middle" class="m">6</text>
<rect x="224" y="40" width="30" height="30" rx="4" class="pnl"/>
<text x="239.0" y="59.5" text-anchor="middle" class="m">7</text>
<rect x="258" y="40" width="30" height="30" rx="4" class="pnl"/>
<text x="273.0" y="59.5" text-anchor="middle" class="m">8</text>
<rect x="292" y="40" width="30" height="30" rx="4" class="pnl"/>
<text x="307.0" y="59.5" text-anchor="middle" class="m">9</text>
<rect x="326" y="40" width="30" height="30" rx="4" class="pnl"/>
<text x="341.0" y="59.5" text-anchor="middle" class="m">10</text>
<text x="380" y="60" text-anchor="start" class="s">page 1 = items 1 to 5</text>
<rect x="20" y="84" width="30" height="30" rx="4" class="k-coral"/>
<text x="35.0" y="103.5" text-anchor="middle" class="km-coral">new</text>
<rect x="54" y="84" width="30" height="30" rx="4" class="pnl"/>
<text x="69.0" y="103.5" text-anchor="middle" class="m">1</text>
<rect x="88" y="84" width="30" height="30" rx="4" class="pnl"/>
<text x="103.0" y="103.5" text-anchor="middle" class="m">2</text>
<rect x="122" y="84" width="30" height="30" rx="4" class="pnl"/>
<text x="137.0" y="103.5" text-anchor="middle" class="m">3</text>
<rect x="156" y="84" width="30" height="30" rx="4" class="pnl"/>
<text x="171.0" y="103.5" text-anchor="middle" class="m">4</text>
<rect x="190" y="84" width="30" height="30" rx="4" class="k-red"/>
<text x="205.0" y="103.5" text-anchor="middle" class="km-red">5</text>
<rect x="224" y="84" width="30" height="30" rx="4" class="k-blue"/>
<text x="239.0" y="103.5" text-anchor="middle" class="km-blue">6</text>
<rect x="258" y="84" width="30" height="30" rx="4" class="k-blue"/>
<text x="273.0" y="103.5" text-anchor="middle" class="km-blue">7</text>
<rect x="292" y="84" width="30" height="30" rx="4" class="k-blue"/>
<text x="307.0" y="103.5" text-anchor="middle" class="km-blue">8</text>
<rect x="326" y="84" width="30" height="30" rx="4" class="k-blue"/>
<text x="341.0" y="103.5" text-anchor="middle" class="km-blue">9</text>
<text x="380" y="104" text-anchor="start" class="kh-red">page 2 shows item 5 again</text>
<text x="20" y="160" text-anchor="start" class="kh-teal">cursor: ?after=eyJpZCI6NX0&amp;limit=5</text>
<rect x="20" y="174" width="30" height="30" rx="4" class="pnl"/>
<text x="35.0" y="193.5" text-anchor="middle" class="m">1</text>
<rect x="54" y="174" width="30" height="30" rx="4" class="pnl"/>
<text x="69.0" y="193.5" text-anchor="middle" class="m">2</text>
<rect x="88" y="174" width="30" height="30" rx="4" class="pnl"/>
<text x="103.0" y="193.5" text-anchor="middle" class="m">3</text>
<rect x="122" y="174" width="30" height="30" rx="4" class="pnl"/>
<text x="137.0" y="193.5" text-anchor="middle" class="m">4</text>
<rect x="156" y="174" width="30" height="30" rx="4" class="pnl"/>
<text x="171.0" y="193.5" text-anchor="middle" class="m">5</text>
<rect x="190" y="174" width="30" height="30" rx="4" class="k-teal"/>
<text x="205.0" y="193.5" text-anchor="middle" class="km-teal">6</text>
<rect x="224" y="174" width="30" height="30" rx="4" class="k-teal"/>
<text x="239.0" y="193.5" text-anchor="middle" class="km-teal">7</text>
<rect x="258" y="174" width="30" height="30" rx="4" class="k-teal"/>
<text x="273.0" y="193.5" text-anchor="middle" class="km-teal">8</text>
<rect x="292" y="174" width="30" height="30" rx="4" class="k-teal"/>
<text x="307.0" y="193.5" text-anchor="middle" class="km-teal">9</text>
<rect x="326" y="174" width="30" height="30" rx="4" class="k-teal"/>
<text x="341.0" y="193.5" text-anchor="middle" class="km-teal">10</text>
<line x1="186" y1="166" x2="186" y2="212" class="ln-teal"/>
<text x="380" y="194" text-anchor="start" class="kh-teal">next page starts after item 5, always</text>
<rect x="20" y="228" width="680" height="48" rx="7" class="pnl"/>
<text x="360.0" y="247.5" text-anchor="middle" class="s">offset: simple, can jump to page N, but drifts and gets slow on deep pages.</text>
<text x="360.0" y="265.5" text-anchor="middle" class="s">cursor: stable and fast, but only next and previous.</text>
</g>
</svg>
<figcaption>Large or fast-changing collections should use cursors. Small, stable ones are fine with offsets.</figcaption>
</figure>

There are two common pagination styles:

- **Offset pagination** (`offset=40&limit=20`) is simple and lets a client jump to any page. Its drawbacks: if items are added or removed between requests, pages shift and the client sees duplicates or misses items, and databases get slow skipping large offsets.
- **Cursor pagination** (`after=<cursor>&limit=20`) returns an opaque token that marks where the last page ended. Pages never shift, and lookups stay fast however deep you go, but clients can only move forward and back.

Either way, wrap the list in an object, `{"items": [...], "total": 57}`, and give the client the URL of the next page rather than making it calculate one. The Library API puts it in a standard `Link` header.

## Hypermedia and the maturity model

<figure class="diagram">
<svg viewBox="0 0 720 270" style="width:100%;height:auto;max-width:720px" role="img" aria-label="The Richardson maturity model: level 0 sends everything to one URL; level 1 introduces resources with their own URLs; level 2 uses HTTP methods and status codes properly; level 3 adds hypermedia links in responses that tell the client what it can do next." xmlns="http://www.w3.org/2000/svg">
<style>
.a5c{ font-family:var(--sans),sans-serif; }
.a5c .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a5c .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a5c .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a5c .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a5c .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a5c .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a5c .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a5c .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a5c .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a5c .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a5c .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a5c .s{ fill:var(--text-dim); font-size:13px; }
.a5c .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a5c .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a5c .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a5c .c{ fill:var(--text-faint); font-size:12.5px; }
.a5c .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a5c .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a5c .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a5c .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a5c-a); }
.a5c .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a5c-a); marker-start:url(#a5c-s); }
.a5c .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a5c-g); }
.a5c .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a5c-a); }
.a5c .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a5c .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a5c .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a5c .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a5c .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a5c .ks-blue{ fill:#185FA5; font-size:13px; }
.a5c .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a5c .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5c .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a5c .kb-blue, :root[data-theme="dark"] .a5c .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a5c .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a5c .kh-blue{ fill:#85B7EB; }
.a5c .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a5c-blue); }
.a5c .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5c-blue); }
.a5c .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a5c .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a5c .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a5c .ks-teal{ fill:#0F6E56; font-size:13px; }
.a5c .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a5c .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5c .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a5c .kb-teal, :root[data-theme="dark"] .a5c .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a5c .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a5c .kh-teal{ fill:#5DCAA5; }
.a5c .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a5c-teal); }
.a5c .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5c-teal); }
.a5c .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a5c .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a5c .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a5c .ks-purple{ fill:#534AB7; font-size:13px; }
.a5c .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a5c .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5c .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a5c .kb-purple, :root[data-theme="dark"] .a5c .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a5c .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a5c .kh-purple{ fill:#AFA9EC; }
.a5c .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a5c-purple); }
.a5c .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5c-purple); }
.a5c .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a5c .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a5c .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a5c .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a5c .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a5c .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a5c .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a5c .kb-gray, :root[data-theme="dark"] .a5c .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a5c .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a5c .kh-gray{ fill:#B4B2A9; }
.a5c .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a5c-gray); }
.a5c .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a5c-gray); }
.a5c .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a5c-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a5c-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a5c-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a5c-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a5c-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a5c-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a5c-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a5c">
<rect x="20" y="20" width="680" height="48" rx="7" class="k-purple"/>
<text x="360.0" y="48.5" text-anchor="middle" class="kb-purple">Level 3: hypermedia: responses include links to next actions</text>
<rect x="60" y="80" width="600" height="48" rx="7" class="k-teal"/>
<text x="360.0" y="108.5" text-anchor="middle" class="kb-teal">Level 2: HTTP methods and status codes used properly</text>
<rect x="100" y="140" width="520" height="48" rx="7" class="k-blue"/>
<text x="360.0" y="168.5" text-anchor="middle" class="kb-blue">Level 1: resources: one URL per thing</text>
<rect x="140" y="200" width="440" height="48" rx="7" class="k-gray"/>
<text x="360.0" y="228.5" text-anchor="middle" class="kb-gray">Level 0: one URL, one method: POST /api for everything</text>
<text x="360" y="262" text-anchor="middle" class="c">most good APIs aim for level 2; level 3 is rare in practice</text>
</g>
</svg>
<figcaption>A useful yardstick for how much an API uses the web's own machinery instead of reinventing it.</figcaption>
</figure>

Leonard Richardson described levels of "RESTfulness". Level 0 tunnels everything through one URL, as many older RPC-style APIs did. Level 1 gives each resource its own URL. Level 2 uses methods and status codes properly; this is where most well-designed APIs sit. Level 3, **hypermedia**, includes links in responses that tell the client what it can do next, the way a web page links to other pages. Fielding considers hypermedia essential to REST, but few public APIs fully adopt it. The pragmatic middle ground used in this book is to include links where they help, such as the next page of a collection or the `Location` of a new resource.

## Consistency above all

A good API feels as if one person designed it. Before building, write down the conventions and apply them everywhere:

- one naming style for fields (`snake_case` or `camelCase`) and URLs;
- one date format (ISO 8601, UTC);
- one error format;
- one pagination style;
- one way of expressing IDs and references between resources.

## Hands on: design before code

Here is the design for the Library API that Chapter 6 implements. Read it as a contract and check it against the rules in this chapter.

| Request | Body | Success | Errors |
|---|---|---|---|
| `GET /books?author=&year=&sort=&limit=&offset=` | none | `200` page of books, `Link` to next page | `422` bad parameter |
| `POST /books` | `title`, `author`, optional `year`, `isbn` | `201` book, `Location` | `422` invalid body |
| `GET /books/{id}` | none | `200` book | `404` |
| `PUT /books/{id}` | full book | `200` book | `404`, `422` |
| `PATCH /books/{id}` | any subset of fields | `200` book | `404`, `422` |
| `DELETE /books/{id}` | none | `204` | `404` |

As an exercise, extend the design with authors and reviews: decide the URLs, which ones nest, which methods each supports, and the status codes. Compare your answer with the resource tree at the start of this chapter.

## Summary

- Design **resources** first: nouns, plural collections, shallow nesting, opaque IDs.
- Map operations onto **methods**: `GET`, `POST` on collections; `GET`, `PUT`, `PATCH`, `DELETE` on items.
- Use **status codes** precisely and one **error format** everywhere.
- Model awkward actions as **state changes** or **new resources** before resorting to action endpoints.
- **Filter, sort, and paginate** with query parameters; always enforce a **maximum page size**; prefer **cursors** for large or changing data.
- **Consistency** matters more than any single rule.
