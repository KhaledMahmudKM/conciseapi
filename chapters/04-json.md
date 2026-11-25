# Chapter 4: JSON and Data Formats

HTTP moves bytes; the client and server still need to agree on what those bytes mean. For web APIs the answer is almost always **JSON**, JavaScript Object Notation. This chapter covers JSON's rules, the traps it sets, how to describe valid JSON with a schema, and the alternatives you will meet.

## JSON in one page

<figure class="diagram">
<svg viewBox="0 0 720 300" style="width:100%;height:auto;max-width:720px" role="img" aria-label="A JSON document and its value types: an object with string, number, boolean, null, array and nested object values. JSON has exactly six types: object, array, string, number, boolean and null." xmlns="http://www.w3.org/2000/svg">
<style>
.a4a{ font-family:var(--sans),sans-serif; }
.a4a .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a4a .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a4a .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a4a .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a4a .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a4a .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a4a .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a4a .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a4a .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a4a .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a4a .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a4a .s{ fill:var(--text-dim); font-size:13px; }
.a4a .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a4a .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a4a .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a4a .c{ fill:var(--text-faint); font-size:12.5px; }
.a4a .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a4a .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a4a .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a4a .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a4a-a); }
.a4a .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a4a-a); marker-start:url(#a4a-s); }
.a4a .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a4a-g); }
.a4a .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a4a-a); }
.a4a .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a4a .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a4a .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a4a .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a4a .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a4a .ks-blue{ fill:#185FA5; font-size:13px; }
.a4a .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a4a .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4a .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a4a .kb-blue, :root[data-theme="dark"] .a4a .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a4a .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a4a .kh-blue{ fill:#85B7EB; }
.a4a .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a4a-blue); }
.a4a .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4a-blue); }
.a4a .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a4a .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a4a .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a4a .ks-teal{ fill:#0F6E56; font-size:13px; }
.a4a .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a4a .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4a .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a4a .kb-teal, :root[data-theme="dark"] .a4a .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a4a .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a4a .kh-teal{ fill:#5DCAA5; }
.a4a .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a4a-teal); }
.a4a .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4a-teal); }
.a4a .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a4a .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a4a .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a4a .ks-amber{ fill:#854F0B; font-size:13px; }
.a4a .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a4a .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4a .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a4a .kb-amber, :root[data-theme="dark"] .a4a .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a4a .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a4a .kh-amber{ fill:#EF9F27; }
.a4a .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a4a-amber); }
.a4a .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4a-amber); }
.a4a .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a4a .k-coral{ fill:#FAECE7; stroke:#D85A30; stroke-width:1.6; }
.a4a .kb-coral{ fill:#712B13; font-size:13px; font-weight:700; }
.a4a .ks-coral{ fill:#993C1D; font-size:13px; }
.a4a .km-coral{ fill:#712B13; font-size:12.5px; font-family:var(--mono),monospace; }
.a4a .kh-coral{ fill:#993C1D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4a .k-coral{ fill:#712B13; stroke:#F0997B; }
:root[data-theme="dark"] .a4a .kb-coral, :root[data-theme="dark"] .a4a .km-coral{ fill:#FAECE7; }
:root[data-theme="dark"] .a4a .ks-coral{ fill:#F5C4B3; }
:root[data-theme="dark"] .a4a .kh-coral{ fill:#F0997B; }
.a4a .ar-coral{ stroke:#D85A30; stroke-width:2; fill:none; marker-end:url(#a4a-coral); }
.a4a .ad-coral{ stroke:#D85A30; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4a-coral); }
.a4a .ln-coral{ stroke:#D85A30; stroke-width:2; fill:none; }
.a4a .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a4a .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a4a .ks-purple{ fill:#534AB7; font-size:13px; }
.a4a .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a4a .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4a .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a4a .kb-purple, :root[data-theme="dark"] .a4a .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a4a .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a4a .kh-purple{ fill:#AFA9EC; }
.a4a .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a4a-purple); }
.a4a .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4a-purple); }
.a4a .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a4a .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a4a .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a4a .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a4a .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a4a .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4a .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a4a .kb-gray, :root[data-theme="dark"] .a4a .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a4a .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a4a .kh-gray{ fill:#B4B2A9; }
.a4a .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a4a-gray); }
.a4a .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4a-gray); }
.a4a .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a4a-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a4a-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a4a-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a4a-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a4a-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a4a-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a4a-coral" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#D85A30"/></marker><marker id="a4a-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a4a-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a4a">
<rect x="20" y="20" width="330" height="260" rx="8" class="pnl"/>
<text x="36" y="44" text-anchor="start" class="m">{</text>
<text x="51.0" y="66" text-anchor="start" class="m">"id": 42,</text>
<text x="51.0" y="88" text-anchor="start" class="m">"title": "Emma",</text>
<text x="51.0" y="110" text-anchor="start" class="m">"available": true,</text>
<text x="51.0" y="132" text-anchor="start" class="m">"rating": null,</text>
<text x="51.0" y="154" text-anchor="start" class="m">"tags": ["classic", "romance"],</text>
<text x="51.0" y="176" text-anchor="start" class="m">"author": {</text>
<text x="66.0" y="198" text-anchor="start" class="m">"name": "Jane Austen",</text>
<text x="66.0" y="220" text-anchor="start" class="m">"born": 1775</text>
<text x="51.0" y="242" text-anchor="start" class="m">}</text>
<text x="36" y="264" text-anchor="start" class="m">}</text>
<rect x="440" y="50" width="120" height="22" rx="4" class="k-blue"/>
<text x="500.0" y="65.5" text-anchor="middle" class="kb-blue">number</text>
<line x1="352" y1="61" x2="438" y2="61" class="ln-blue"/>
<rect x="440" y="72" width="120" height="22" rx="4" class="k-teal"/>
<text x="500.0" y="87.5" text-anchor="middle" class="kb-teal">string</text>
<line x1="352" y1="83" x2="438" y2="83" class="ln-teal"/>
<rect x="440" y="94" width="120" height="22" rx="4" class="k-amber"/>
<text x="500.0" y="109.5" text-anchor="middle" class="kb-amber">boolean</text>
<line x1="352" y1="105" x2="438" y2="105" class="ln-amber"/>
<rect x="440" y="116" width="120" height="22" rx="4" class="k-gray"/>
<text x="500.0" y="131.5" text-anchor="middle" class="kb-gray">null</text>
<line x1="352" y1="127" x2="438" y2="127" class="ln-gray"/>
<rect x="440" y="138" width="120" height="22" rx="4" class="k-purple"/>
<text x="500.0" y="153.5" text-anchor="middle" class="kb-purple">array</text>
<line x1="352" y1="149" x2="438" y2="149" class="ln-purple"/>
<rect x="440" y="160" width="120" height="22" rx="4" class="k-coral"/>
<text x="500.0" y="175.5" text-anchor="middle" class="kb-coral">object</text>
<line x1="352" y1="171" x2="438" y2="171" class="ln-coral"/>
<rect x="380" y="232" width="320" height="48" rx="7" class="pnl"/>
<text x="540.0" y="251.5" text-anchor="middle" class="s">No dates, no comments, no trailing commas,</text>
<text x="540.0" y="269.5" text-anchor="middle" class="s">strings in double quotes only</text>
</g>
</svg>
<figcaption>Six value types, nested freely. Anything else, such as a date, must be encoded as one of them.</figcaption>
</figure>

JSON has exactly six kinds of value:

- **object**: an unordered set of `"name": value` pairs in braces. Names are always strings in double quotes.
- **array**: an ordered list in square brackets.
- **string**: Unicode text in **double** quotes, with escapes such as `\"`, `\n`, and `é`.
- **number**: an integer or decimal, such as `42`, `-3.5`, `1e6`. There is no separate integer type, and no `NaN` or infinity.
- **boolean**: `true` or `false`.
- **null**: no value.

That is all. JSON has no dates, no comments, no trailing commas, and no single quotes. Every one of those is a syntax error, and a common source of "invalid JSON" bugs when people write JSON by hand.

## From objects to text and back

<figure class="diagram">
<svg viewBox="0 0 720 220" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Serialization and parsing: a Python dictionary on the server is serialized to JSON text, sent as bytes over HTTP, and parsed by the client into its own native structure, such as a JavaScript object or another Python dictionary." xmlns="http://www.w3.org/2000/svg">
<style>
.a4b{ font-family:var(--sans),sans-serif; }
.a4b .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a4b .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a4b .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a4b .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a4b .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a4b .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a4b .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a4b .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a4b .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a4b .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a4b .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a4b .s{ fill:var(--text-dim); font-size:13px; }
.a4b .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a4b .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a4b .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a4b .c{ fill:var(--text-faint); font-size:12.5px; }
.a4b .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a4b .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a4b .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a4b .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a4b-a); }
.a4b .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a4b-a); marker-start:url(#a4b-s); }
.a4b .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a4b-g); }
.a4b .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a4b-a); }
.a4b .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a4b .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a4b .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a4b .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a4b .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a4b .ks-blue{ fill:#185FA5; font-size:13px; }
.a4b .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a4b .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4b .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a4b .kb-blue, :root[data-theme="dark"] .a4b .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a4b .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a4b .kh-blue{ fill:#85B7EB; }
.a4b .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a4b-blue); }
.a4b .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4b-blue); }
.a4b .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a4b .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a4b .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a4b .ks-teal{ fill:#0F6E56; font-size:13px; }
.a4b .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a4b .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4b .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a4b .kb-teal, :root[data-theme="dark"] .a4b .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a4b .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a4b .kh-teal{ fill:#5DCAA5; }
.a4b .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a4b-teal); }
.a4b .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4b-teal); }
.a4b .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a4b .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a4b .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a4b .ks-amber{ fill:#854F0B; font-size:13px; }
.a4b .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a4b .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4b .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a4b .kb-amber, :root[data-theme="dark"] .a4b .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a4b .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a4b .kh-amber{ fill:#EF9F27; }
.a4b .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a4b-amber); }
.a4b .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4b-amber); }
.a4b .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
</style>
<defs><marker id="a4b-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a4b-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a4b-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a4b-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a4b-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a4b-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker></defs>
<g class="a4b">
<rect x="20" y="60" width="160" height="64" rx="7" class="k-teal"/>
<text x="100.0" y="87.5" text-anchor="middle" class="kb-teal">Python dict</text>
<text x="100.0" y="105.5" text-anchor="middle" class="km-teal">{'id': 42}</text>
<rect x="280" y="60" width="160" height="64" rx="7" class="k-amber"/>
<text x="360.0" y="87.5" text-anchor="middle" class="kb-amber">JSON text</text>
<text x="360.0" y="105.5" text-anchor="middle" class="km-amber">{"id": 42}</text>
<rect x="540" y="60" width="160" height="64" rx="7" class="k-blue"/>
<text x="620.0" y="87.5" text-anchor="middle" class="kb-blue">JavaScript object</text>
<text x="620.0" y="105.5" text-anchor="middle" class="km-blue">{id: 42}</text>
<line x1="182" y1="92" x2="278" y2="92" class="ar"/>
<line x1="442" y1="92" x2="538" y2="92" class="ar"/>
<text x="230" y="80" text-anchor="middle" class="a">serialize</text>
<text x="490" y="80" text-anchor="middle" class="a">parse</text>
<text x="230" y="112" text-anchor="middle" class="c">json.dumps</text>
<text x="490" y="112" text-anchor="middle" class="c">JSON.parse</text>
<text x="360" y="168" text-anchor="middle" class="c">UTF-8 bytes on the wire, labelled Content-Type: application/json</text>
</g>
</svg>
<figcaption>JSON is the neutral middle. Each side converts to and from its own language's data structures.</figcaption>
</figure>

Turning a data structure into JSON text is **serialisation** (or encoding); turning text back into a structure is **parsing** (or decoding). In Python, `json.dumps()` and `json.loads()` do both. The mapping between Python and JSON is close but not exact:

| Python | JSON |
|---|---|
| `dict` | object |
| `list`, `tuple` | array |
| `str` | string |
| `int`, `float` | number |
| `True`, `False` | `true`, `false` |
| `None` | `null` |

A JSON body travels as UTF-8 bytes, labelled with `Content-Type: application/json`.

## Hands on: JSON pitfalls

`json_demo.py` shows the surprises worth knowing:

```bash
python json_demo.py
```

```text
serialized: {"id": 1, "title": "Dune", "tags": ["sf", "classic"], "in_stock": true, "rating": null}
datetime fails: Object of type datetime is not JSON serializable
ISO 8601 works: {"when": "2026-11-15T09:30:00+00:00"}
big int as number: {"id": 9007199254740993}  as string: {"id": "9007199254740993"}
```

Three lessons:

1. **Dates.** JSON has no date type, so an API must choose a string format. Use **ISO 8601** with a time zone, such as `2026-11-15T09:30:00Z` (`Z` means UTC). Never send local times without an offset, and avoid ambiguous formats like `11/12/2026`.
2. **Large numbers.** JavaScript stores every number as a 64-bit float, which represents integers exactly only up to 2^53. A database ID such as `9007199254740993` silently becomes `9007199254740992` in a browser. APIs that use very large IDs, including several large social networks, send them as **strings**.
3. **Money.** Floating-point numbers cannot represent most decimal fractions exactly (`0.1 + 0.2` is not `0.3`). Send money as an integer number of the smallest unit (`1999` cents) or as a decimal string (`"19.99"`), with a separate currency code.

### Naming and shape conventions

JSON allows any names, so APIs agree on conventions. Pick one and use it everywhere:

- **Field names** in `snake_case` (`created_at`) or `camelCase` (`createdAt`). Both are common; mixing them is not.
- **Absent versus null.** Decide whether a missing field and `"field": null` mean the same thing. In a `PATCH` request they usually do not: missing means "leave unchanged", `null` means "clear it".
- **Collections in an envelope.** Return `{"items": [...], "total": 57}` rather than a bare array, so you can add pagination information later without breaking clients.

## Describing valid JSON: JSON Schema

How does a client know what a valid request looks like, or a server check that it received one? **JSON Schema** is a vocabulary for describing JSON documents: which fields exist, their types, which are required, and constraints such as lengths, ranges, and patterns.

<figure class="diagram">
<svg viewBox="0 0 720 250" style="width:100%;height:auto;max-width:720px" role="img" aria-label="Validating with a schema: an incoming JSON payload is checked against a JSON Schema that requires a non-empty title string and an optional integer year. A valid payload passes to the application; an invalid one is rejected with a list of errors." xmlns="http://www.w3.org/2000/svg">
<style>
.a4d{ font-family:var(--sans),sans-serif; }
.a4d .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a4d .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a4d .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a4d .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a4d .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a4d .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a4d .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a4d .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a4d .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a4d .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a4d .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a4d .s{ fill:var(--text-dim); font-size:13px; }
.a4d .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a4d .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a4d .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a4d .c{ fill:var(--text-faint); font-size:12.5px; }
.a4d .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a4d .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a4d .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a4d .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a4d-a); }
.a4d .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a4d-a); marker-start:url(#a4d-s); }
.a4d .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a4d-g); }
.a4d .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a4d-a); }
.a4d .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a4d .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a4d .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a4d .k-amber{ fill:#FAEEDA; stroke:#BA7517; stroke-width:1.6; }
.a4d .kb-amber{ fill:#633806; font-size:13px; font-weight:700; }
.a4d .ks-amber{ fill:#854F0B; font-size:13px; }
.a4d .km-amber{ fill:#633806; font-size:12.5px; font-family:var(--mono),monospace; }
.a4d .kh-amber{ fill:#854F0B; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4d .k-amber{ fill:#633806; stroke:#EF9F27; }
:root[data-theme="dark"] .a4d .kb-amber, :root[data-theme="dark"] .a4d .km-amber{ fill:#FAEEDA; }
:root[data-theme="dark"] .a4d .ks-amber{ fill:#FAC775; }
:root[data-theme="dark"] .a4d .kh-amber{ fill:#EF9F27; }
.a4d .ar-amber{ stroke:#BA7517; stroke-width:2; fill:none; marker-end:url(#a4d-amber); }
.a4d .ad-amber{ stroke:#BA7517; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4d-amber); }
.a4d .ln-amber{ stroke:#BA7517; stroke-width:2; fill:none; }
.a4d .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a4d .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a4d .ks-purple{ fill:#534AB7; font-size:13px; }
.a4d .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a4d .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4d .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a4d .kb-purple, :root[data-theme="dark"] .a4d .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a4d .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a4d .kh-purple{ fill:#AFA9EC; }
.a4d .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a4d-purple); }
.a4d .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4d-purple); }
.a4d .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a4d .k-green{ fill:#EAF3DE; stroke:#639922; stroke-width:1.6; }
.a4d .kb-green{ fill:#27500A; font-size:13px; font-weight:700; }
.a4d .ks-green{ fill:#3B6D11; font-size:13px; }
.a4d .km-green{ fill:#27500A; font-size:12.5px; font-family:var(--mono),monospace; }
.a4d .kh-green{ fill:#3B6D11; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4d .k-green{ fill:#27500A; stroke:#97C459; }
:root[data-theme="dark"] .a4d .kb-green, :root[data-theme="dark"] .a4d .km-green{ fill:#EAF3DE; }
:root[data-theme="dark"] .a4d .ks-green{ fill:#C0DD97; }
:root[data-theme="dark"] .a4d .kh-green{ fill:#97C459; }
.a4d .ar-green{ stroke:#639922; stroke-width:2; fill:none; marker-end:url(#a4d-green); }
.a4d .ad-green{ stroke:#639922; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4d-green); }
.a4d .ln-green{ stroke:#639922; stroke-width:2; fill:none; }
.a4d .k-red{ fill:#FCEBEB; stroke:#E24B4A; stroke-width:1.6; }
.a4d .kb-red{ fill:#791F1F; font-size:13px; font-weight:700; }
.a4d .ks-red{ fill:#A32D2D; font-size:13px; }
.a4d .km-red{ fill:#791F1F; font-size:12.5px; font-family:var(--mono),monospace; }
.a4d .kh-red{ fill:#A32D2D; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4d .k-red{ fill:#791F1F; stroke:#F09595; }
:root[data-theme="dark"] .a4d .kb-red, :root[data-theme="dark"] .a4d .km-red{ fill:#FCEBEB; }
:root[data-theme="dark"] .a4d .ks-red{ fill:#F7C1C1; }
:root[data-theme="dark"] .a4d .kh-red{ fill:#F09595; }
.a4d .ar-red{ stroke:#E24B4A; stroke-width:2; fill:none; marker-end:url(#a4d-red); }
.a4d .ad-red{ stroke:#E24B4A; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4d-red); }
.a4d .ln-red{ stroke:#E24B4A; stroke-width:2; fill:none; }
</style>
<defs><marker id="a4d-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a4d-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a4d-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a4d-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#BA7517"/></marker><marker id="a4d-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a4d-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#639922"/></marker><marker id="a4d-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#E24B4A"/></marker></defs>
<g class="a4d">
<rect x="20" y="80" width="170" height="80" rx="7" class="k-amber"/>
<text x="105.0" y="104.5" text-anchor="middle" class="kb-amber">incoming JSON</text>
<text x="105.0" y="124.5" text-anchor="middle" class="km-amber">{"title": "",</text>
<text x="105.0" y="144.5" text-anchor="middle" class="km-amber"> "year": "1815"}</text>
<rect x="260" y="60" width="200" height="120" rx="7" class="k-purple"/>
<text x="360.0" y="91.5" text-anchor="middle" class="kb-purple">JSON Schema</text>
<text x="360.0" y="113.5" text-anchor="middle" class="km-purple">title: string,</text>
<text x="360.0" y="135.5" text-anchor="middle" class="km-purple">  minLength 1</text>
<text x="360.0" y="157.5" text-anchor="middle" class="km-purple">year: integer</text>
<rect x="530" y="40" width="170" height="60" rx="7" class="k-green"/>
<text x="615.0" y="65.5" text-anchor="middle" class="kb-green">valid</text>
<text x="615.0" y="83.5" text-anchor="middle" class="ks-green">to your code</text>
<rect x="530" y="140" width="170" height="70" rx="7" class="k-red"/>
<text x="615.0" y="161.5" text-anchor="middle" class="kb-red">invalid: 422</text>
<text x="615.0" y="179.5" text-anchor="middle" class="ks-red">title too short;</text>
<text x="615.0" y="197.5" text-anchor="middle" class="ks-red">year not integer</text>
<line x1="192" y1="120" x2="258" y2="120" class="ar"/>
<line x1="462" y1="100" x2="528" y2="70" class="ar-green"/>
<line x1="462" y1="140" x2="528" y2="170" class="ar-red"/>
</g>
</svg>
<figcaption>A schema turns "the API expects a title" into something a machine can check, generate documentation from, and enforce.</figcaption>
</figure>

You rarely write JSON Schema by hand. In Python, a **Pydantic** model generates it:

```python
from pydantic import BaseModel, Field

class Book(BaseModel):
    id: int
    title: str = Field(min_length=1, max_length=200)
    year: int | None = Field(default=None, ge=0, le=2100)
    tags: list[str] = []
```

`Book.model_json_schema()` produces the schema (shortened):

```json
{
  "title": "Book",
  "type": "object",
  "properties": {
    "id":    {"type": "integer"},
    "title": {"type": "string", "minLength": 1, "maxLength": 200},
    "year":  {"anyOf": [{"type": "integer", "minimum": 0, "maximum": 2100}, {"type": "null"}]},
    "tags":  {"type": "array", "items": {"type": "string"}, "default": []}
  },
  "required": ["id", "title"]
}
```

And the same model validates input:

```python
Book.model_validate_json('{"id": "seven", "title": ""}')
# ValidationError: id: Input should be a valid integer; title: String should have at least 1 character
```

FastAPI uses exactly this mechanism: the models you declare validate every request, and their schemas become part of the API's OpenAPI document (Chapter 7).

## Other formats

<figure class="diagram">
<svg viewBox="0 0 720 290" style="width:100%;height:auto;max-width:720px" role="img" aria-label="The same book in four formats: JSON, compact and universal for web APIs; XML, verbose with tags and attributes; YAML, readable and used for configuration files and OpenAPI documents; and Protocol Buffers, a binary format that needs a schema and is much smaller." xmlns="http://www.w3.org/2000/svg">
<style>
.a4c{ font-family:var(--sans),sans-serif; }
.a4c .box{ fill:var(--bg-soft); stroke:var(--border); stroke-width:1.5; }
.a4c .pnl{ fill:var(--panel); stroke:var(--border); stroke-width:1.5; }
.a4c .hov{ fill:var(--panel-hover); stroke:var(--border); stroke-width:1.5; }
.a4c .acc{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.6; }
.a4c .dark{ fill:var(--accent); stroke:var(--accent); stroke-width:1.6; }
.a4c .out{ fill:none; stroke:var(--accent); stroke-width:2; }
.a4c .dash{ fill:none; stroke:var(--accent); stroke-width:1.6; stroke-dasharray:6 4; }
.a4c .zone{ fill:none; stroke:var(--border); stroke-width:1.5; stroke-dasharray:6 4; }
.a4c .tint{ fill:var(--accent-dim); stroke:var(--accent); stroke-width:1.2; opacity:0.28; }
.a4c .h{ fill:var(--text); font-size:15px; font-weight:700; }
.a4c .b{ fill:var(--text); font-size:13px; font-weight:700; }
.a4c .s{ fill:var(--text-dim); font-size:13px; }
.a4c .a{ fill:var(--accent); font-size:13px; font-weight:700; }
.a4c .m{ fill:var(--text); font-size:12.5px; font-family:var(--mono),monospace; }
.a4c .ma{ fill:var(--accent); font-size:12.5px; font-family:var(--mono),monospace; }
.a4c .c{ fill:var(--text-faint); font-size:12.5px; }
.a4c .on{ fill:var(--bg); font-size:13px; font-weight:700; }
.a4c .ln{ stroke:var(--border); stroke-width:1.5; fill:none; }
.a4c .lk{ stroke:var(--text-faint); stroke-width:2.2; fill:none; }
.a4c .ar{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a4c-a); }
.a4c .ar2{ stroke:var(--accent); stroke-width:2; fill:none; marker-end:url(#a4c-a); marker-start:url(#a4c-s); }
.a4c .ag{ stroke:var(--text-faint); stroke-width:1.8; fill:none; marker-end:url(#a4c-g); }
.a4c .ad{ stroke:var(--accent); stroke-width:1.8; fill:none; stroke-dasharray:6 4; marker-end:url(#a4c-a); }
.a4c .gd{ stroke:var(--text-faint); stroke-width:1.6; fill:none; stroke-dasharray:4 4; }
.a4c .x{ stroke:var(--text-faint); stroke-width:2.4; fill:none; }
.a4c .bad{ stroke:var(--text); stroke-width:3; fill:none; }
.a4c .k-blue{ fill:#E6F1FB; stroke:#378ADD; stroke-width:1.6; }
.a4c .kb-blue{ fill:#0C447C; font-size:13px; font-weight:700; }
.a4c .ks-blue{ fill:#185FA5; font-size:13px; }
.a4c .km-blue{ fill:#0C447C; font-size:12.5px; font-family:var(--mono),monospace; }
.a4c .kh-blue{ fill:#185FA5; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4c .k-blue{ fill:#0C447C; stroke:#85B7EB; }
:root[data-theme="dark"] .a4c .kb-blue, :root[data-theme="dark"] .a4c .km-blue{ fill:#E6F1FB; }
:root[data-theme="dark"] .a4c .ks-blue{ fill:#B5D4F4; }
:root[data-theme="dark"] .a4c .kh-blue{ fill:#85B7EB; }
.a4c .ar-blue{ stroke:#378ADD; stroke-width:2; fill:none; marker-end:url(#a4c-blue); }
.a4c .ad-blue{ stroke:#378ADD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4c-blue); }
.a4c .ln-blue{ stroke:#378ADD; stroke-width:2; fill:none; }
.a4c .k-teal{ fill:#E1F5EE; stroke:#1D9E75; stroke-width:1.6; }
.a4c .kb-teal{ fill:#085041; font-size:13px; font-weight:700; }
.a4c .ks-teal{ fill:#0F6E56; font-size:13px; }
.a4c .km-teal{ fill:#085041; font-size:12.5px; font-family:var(--mono),monospace; }
.a4c .kh-teal{ fill:#0F6E56; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4c .k-teal{ fill:#085041; stroke:#5DCAA5; }
:root[data-theme="dark"] .a4c .kb-teal, :root[data-theme="dark"] .a4c .km-teal{ fill:#E1F5EE; }
:root[data-theme="dark"] .a4c .ks-teal{ fill:#9FE1CB; }
:root[data-theme="dark"] .a4c .kh-teal{ fill:#5DCAA5; }
.a4c .ar-teal{ stroke:#1D9E75; stroke-width:2; fill:none; marker-end:url(#a4c-teal); }
.a4c .ad-teal{ stroke:#1D9E75; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4c-teal); }
.a4c .ln-teal{ stroke:#1D9E75; stroke-width:2; fill:none; }
.a4c .k-purple{ fill:#EEEDFE; stroke:#7F77DD; stroke-width:1.6; }
.a4c .kb-purple{ fill:#3C3489; font-size:13px; font-weight:700; }
.a4c .ks-purple{ fill:#534AB7; font-size:13px; }
.a4c .km-purple{ fill:#3C3489; font-size:12.5px; font-family:var(--mono),monospace; }
.a4c .kh-purple{ fill:#534AB7; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4c .k-purple{ fill:#3C3489; stroke:#AFA9EC; }
:root[data-theme="dark"] .a4c .kb-purple, :root[data-theme="dark"] .a4c .km-purple{ fill:#EEEDFE; }
:root[data-theme="dark"] .a4c .ks-purple{ fill:#CECBF6; }
:root[data-theme="dark"] .a4c .kh-purple{ fill:#AFA9EC; }
.a4c .ar-purple{ stroke:#7F77DD; stroke-width:2; fill:none; marker-end:url(#a4c-purple); }
.a4c .ad-purple{ stroke:#7F77DD; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4c-purple); }
.a4c .ln-purple{ stroke:#7F77DD; stroke-width:2; fill:none; }
.a4c .k-gray{ fill:#F1EFE8; stroke:#888780; stroke-width:1.6; }
.a4c .kb-gray{ fill:#444441; font-size:13px; font-weight:700; }
.a4c .ks-gray{ fill:#5F5E5A; font-size:13px; }
.a4c .km-gray{ fill:#444441; font-size:12.5px; font-family:var(--mono),monospace; }
.a4c .kh-gray{ fill:#5F5E5A; font-size:13px; font-weight:700; }
:root[data-theme="dark"] .a4c .k-gray{ fill:#444441; stroke:#B4B2A9; }
:root[data-theme="dark"] .a4c .kb-gray, :root[data-theme="dark"] .a4c .km-gray{ fill:#F1EFE8; }
:root[data-theme="dark"] .a4c .ks-gray{ fill:#D3D1C7; }
:root[data-theme="dark"] .a4c .kh-gray{ fill:#B4B2A9; }
.a4c .ar-gray{ stroke:#888780; stroke-width:2; fill:none; marker-end:url(#a4c-gray); }
.a4c .ad-gray{ stroke:#888780; stroke-width:2; fill:none; stroke-dasharray:6 4; marker-end:url(#a4c-gray); }
.a4c .ln-gray{ stroke:#888780; stroke-width:2; fill:none; }
</style>
<defs><marker id="a4c-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker><marker id="a4c-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10 z" fill="var(--accent)"/></marker><marker id="a4c-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="var(--text-faint)"/></marker><marker id="a4c-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#378ADD"/></marker><marker id="a4c-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#1D9E75"/></marker><marker id="a4c-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#7F77DD"/></marker><marker id="a4c-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#888780"/></marker></defs>
<g class="a4c">
<rect x="20" y="20" width="330" height="110" rx="7" class="k-teal"/>
<text x="185.0" y="55.5" text-anchor="middle" class="kb-teal">JSON</text>
<text x="185.0" y="79.5" text-anchor="middle" class="km-teal">{"id":42,"title":"Emma"}</text>
<text x="185.0" y="103.5" text-anchor="middle" class="ks-teal">web APIs</text>
<rect x="370" y="20" width="330" height="110" rx="7" class="k-gray"/>
<text x="535.0" y="55.5" text-anchor="middle" class="kb-gray">XML</text>
<text x="535.0" y="79.5" text-anchor="middle" class="km-gray">&lt;book id="42"&gt;&lt;title&gt;Emma&lt;/title&gt;&lt;/book&gt;</text>
<text x="535.0" y="103.5" text-anchor="middle" class="ks-gray">SOAP, older systems</text>
<rect x="20" y="150" width="330" height="110" rx="7" class="k-purple"/>
<text x="185.0" y="185.5" text-anchor="middle" class="kb-purple">YAML</text>
<text x="185.0" y="209.5" text-anchor="middle" class="km-purple">id: 42  /  title: Emma</text>
<text x="185.0" y="233.5" text-anchor="middle" class="ks-purple">config, OpenAPI files</text>
<rect x="370" y="150" width="330" height="110" rx="7" class="k-blue"/>
<text x="535.0" y="185.5" text-anchor="middle" class="kb-blue">Protocol Buffers</text>
<text x="535.0" y="209.5" text-anchor="middle" class="km-blue">08 2a 12 04 45 6d 6d 61</text>
<text x="535.0" y="233.5" text-anchor="middle" class="ks-blue">gRPC: binary</text>
</g>
</svg>
<figcaption>JSON won for web APIs because it is readable, compact enough, and native to browsers. Protobuf wins where size and speed matter.</figcaption>
</figure>

| Format | Where you meet it | Strengths | Weaknesses |
|---|---|---|---|
| **JSON** | Almost all web APIs | Readable, universal, native in browsers | Verbose, no dates or binary data |
| **XML** | SOAP, older enterprise APIs, RSS | Schemas, namespaces, mature tooling | Very verbose, complex |
| **YAML** | Configuration files, OpenAPI documents | Very readable, allows comments | Indentation-sensitive, surprising edge cases |
| **Protocol Buffers** | gRPC | Small, fast, strongly typed | Binary: needs the schema to read |
| **Form encoding** | HTML forms, OAuth token requests | Simple key-value pairs | Flat: no nesting |

Binary data such as images is usually not put inside JSON at all. APIs upload files with `multipart/form-data`, or return a link to a separate download URL. When small binary values must go inside JSON, they are **Base64**-encoded, which makes them about a third larger.

## Summary

- JSON has **six types**: object, array, string, number, boolean, null. No dates, comments, or trailing commas.
- Send **dates** as ISO 8601 strings with a time zone, **big IDs** as strings, and **money** as integers or decimal strings.
- Choose consistent **naming** and wrap collections in an **envelope**.
- **JSON Schema** describes valid documents; **Pydantic** models generate schemas and validate input.
- **XML**, **YAML**, **Protocol Buffers**, and **form encoding** each have their place; JSON dominates web APIs.

## Check your understanding

Choose the best answer for each question, then check your answers in [Answers to Chapter Questions](answers.md#chapter-4-json-and-data-formats).

**1. How many value types does JSON have?**

- A. Four
- B. Six
- C. Five
- D. Eight

**2. Which is valid JSON?**

- A. {'name': 'Ada'}
- B. {"name": "Ada",}
- C. {"name": "Ada"}
- D. {name: "Ada"}

**3. How should an API send a date and time?**

- A. As an ISO 8601 string with a time zone
- B. As a number of days
- C. As a localised string, like 11/25/26
- D. JSON has a date type

**4. Why do some APIs send very large IDs as strings?**

- A. JavaScript numbers are exact only up to 2^53, so larger IDs can silently change
- B. Strings are faster
- C. JSON forbids large numbers
- D. To hide the IDs

**5. How should money be represented?**

- A. As a float such as 19.99
- B. As a boolean
- C. As an integer in the smallest unit, or a decimal string
- D. As a percentage

**6. Why wrap a collection in an envelope such as {"items": [...]}?**

- A. It is required by JSON
- B. It leaves room to add fields such as a total or next-page link without breaking clients
- C. It makes the response smaller
- D. It encrypts the data

**7. What does JSON Schema describe?**

- A. How to compress JSON
- B. The order of fields
- C. How to convert JSON to XML
- D. Which JSON documents are valid: types, required fields and limits

**8. Which format is binary and schema-first, and used by gRPC?**

- A. YAML
- B. Protocol Buffers
- C. XML
- D. Form encoding
