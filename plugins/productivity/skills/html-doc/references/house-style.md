# html-doc house style

The locked look. Paste the `<style>` block verbatim, then fill the skeleton. Do **not** invent a new palette, font, or layout per run — the sameness *is* the product. This style already encodes the artifact fundamentals (theme-aware, responsive, self-contained), so apply it directly; you don't need to re-derive a design.

Identity: sans headings + serif body on cool paper, one restrained teal accent, monospace only for kickers/metadata/code. Readability first — ~72ch measure, generous leading.

Show, don't tell. Lead each point with the interface, a diagram, or a comparison — the visual kit below (before/after chips, compare bars, flow steps) beats a paragraph. Words are captions, not prose. Cut any sentence a visual already makes.

## The generic structure

One shape fits every doc (PR write-up, concept explainer, anything):

1. **Kicker** — mono metadata strip: doc type · date · source (PR ref, repo, topic).
2. **Title** + one-sentence **subtitle**.
3. **TL;DR card** — mandatory. 2–4 sentences; the keep-if-you-read-nothing-else.
4. **Sections** (`<h2>`) — tight prose, one idea per paragraph. Reach for a table, callout, or code block whenever it beats a paragraph.
5. **Footer** — source / generated note.

## The style block

```html
<style>
  :root{
    --bg:#FAFAF8; --surface:#FFFFFF; --text:#1B1A18; --muted:#6C6A64;
    --border:#E6E3DC; --accent:#0F766E; --accent-soft:#E4F1EF;
    --warn:#B4530A; --warn-soft:#FBEEE1; --code-bg:#F4F2EC;
    --measure:44rem;
    --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
    --mono:ui-monospace,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
  }
  @media (prefers-color-scheme:dark){:root{
    --bg:#141413; --surface:#1C1C1A; --text:#ECEAE3; --muted:#9C988E;
    --border:#2E2D2A; --accent:#4FD1C5; --accent-soft:#16302D;
    --warn:#E0975A; --warn-soft:#2A2015; --code-bg:#211F1C;
  }}
  :root[data-theme="light"]{
    --bg:#FAFAF8; --surface:#FFFFFF; --text:#1B1A18; --muted:#6C6A64;
    --border:#E6E3DC; --accent:#0F766E; --accent-soft:#E4F1EF;
    --warn:#B4530A; --warn-soft:#FBEEE1; --code-bg:#F4F2EC;
  }
  :root[data-theme="dark"]{
    --bg:#141413; --surface:#1C1C1A; --text:#ECEAE3; --muted:#9C988E;
    --border:#2E2D2A; --accent:#4FD1C5; --accent-soft:#16302D;
    --warn:#E0975A; --warn-soft:#2A2015; --code-bg:#211F1C;
  }
  *{box-sizing:border-box}
  body{background:var(--bg);color:var(--text);font-family:var(--serif);
    font-size:1.125rem;line-height:1.7;margin:0;
    -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
  .doc{max-width:var(--measure);margin:0 auto;padding:4rem 1.5rem 6rem}

  .doc-kicker{font-family:var(--mono);font-size:.7rem;letter-spacing:.14em;
    text-transform:uppercase;color:var(--accent);margin:0 0 1rem;
    display:flex;flex-wrap:wrap;gap:.5rem 1rem}
  .doc-kicker span{color:var(--muted)}
  h1{font-family:var(--sans);font-weight:800;font-size:2.6rem;line-height:1.08;
    letter-spacing:-.02em;margin:0 0 .6rem}
  .doc-sub{font-family:var(--sans);font-weight:400;font-size:1.2rem;
    color:var(--muted);margin:0 0 1.6rem;line-height:1.4}
  .doc-rule{height:3px;width:100%;background:var(--accent);border:0;margin:0 0 2.5rem;opacity:.9}

  .tldr{background:var(--surface);border:1px solid var(--border);
    border-left:4px solid var(--accent);border-radius:10px;padding:1.25rem 1.4rem;margin:0 0 2.5rem}
  .tldr h2{font-family:var(--mono);font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;
    color:var(--accent);margin:0 0 .5rem;border:0;padding:0}
  .tldr>:last-child{margin-bottom:0}

  h2{font-family:var(--sans);font-weight:700;font-size:1.6rem;letter-spacing:-.01em;line-height:1.2;
    margin:3rem 0 1rem;padding-top:1.4rem;border-top:1px solid var(--border)}
  h3{font-family:var(--sans);font-weight:650;font-size:1.2rem;margin:2rem 0 .6rem}
  p,ul,ol{margin:0 0 1.15rem}
  ul,ol{padding-left:1.3rem}
  li{margin:.35rem 0}
  a{color:var(--accent);text-underline-offset:2px;text-decoration-thickness:1px}

  .note,.tip,.warn{border:1px solid var(--border);border-radius:10px;
    padding:1rem 1.2rem;margin:1.6rem 0;font-size:1rem;background:var(--surface)}
  .note{border-left:4px solid var(--accent);background:var(--accent-soft)}
  .tip{border-left:4px solid var(--accent)}
  .warn{border-left:4px solid var(--warn);background:var(--warn-soft)}
  .note>.label,.tip>.label,.warn>.label{font-family:var(--mono);font-size:.68rem;
    letter-spacing:.12em;text-transform:uppercase;display:block;margin-bottom:.35rem}
  .note>.label,.tip>.label{color:var(--accent)}
  .warn>.label{color:var(--warn)}
  .note>:last-child,.tip>:last-child,.warn>:last-child{margin-bottom:0}

  code{font-family:var(--mono);font-size:.9em;background:var(--code-bg);padding:.12em .38em;border-radius:5px}
  pre{background:var(--code-bg);border:1px solid var(--border);border-radius:10px;
    padding:1.1rem 1.2rem;overflow-x:auto;margin:1.6rem 0;font-size:.92rem;line-height:1.55}
  pre code{background:none;padding:0;font-size:inherit}

  .table-wrap{overflow-x:auto;margin:1.6rem 0;border:1px solid var(--border);border-radius:10px}
  table{border-collapse:collapse;width:100%;font-size:.98rem;font-family:var(--sans)}
  th,td{text-align:left;padding:.7rem .9rem;border-bottom:1px solid var(--border)}
  th{font-weight:650;font-size:.8rem;letter-spacing:.03em;text-transform:uppercase;color:var(--muted)}
  tr:last-child td{border-bottom:0}

  blockquote{margin:1.6rem 0;padding:.2rem 0 .2rem 1.2rem;border-left:3px solid var(--border);
    color:var(--muted);font-style:italic}
  img{max-width:100%;height:auto;border-radius:8px}

  figure{margin:1.8rem 0}
  figcaption{font-family:var(--mono);font-size:.7rem;letter-spacing:.06em;text-transform:uppercase;
    color:var(--muted);margin-top:.55rem}
  .chip{display:inline-block;font-family:var(--mono);font-size:.74rem;background:var(--code-bg);
    border:1px solid var(--border);border-radius:6px;padding:.2rem .5rem;margin:.15rem .3rem .15rem 0}
  .chip.off{opacity:.45;text-decoration:line-through}

  .ba{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:0}
  .ba-col{border:1px solid var(--border);border-radius:10px;padding:1rem 1.1rem;background:var(--surface)}
  .ba-col.before{border-top:3px solid var(--warn)}
  .ba-col.after{border-top:3px solid var(--accent)}
  .ba-col .lbl{font-family:var(--mono);font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;
    color:var(--muted);display:block;margin-bottom:.6rem}

  .bars{display:flex;flex-direction:column;gap:.6rem;margin:0}
  .bar{display:grid;grid-template-columns:6rem 1fr auto;align-items:center;gap:.8rem;
    font-family:var(--sans);font-size:.9rem}
  .bar .k{color:var(--muted);text-align:right}
  .bar .track{background:var(--code-bg);border:1px solid var(--border);border-radius:6px;height:1.5rem;overflow:hidden}
  .bar .fill{display:block;height:100%;border-radius:6px 0 0 6px;background:var(--accent)}
  .bar.big .fill{background:var(--warn)}
  .bar .v{font-family:var(--mono);font-size:.82rem;white-space:nowrap}

  .flow{display:flex;flex-wrap:wrap;gap:.6rem;margin:0}
  .flow .step{flex:1 1 8rem;border:1px solid var(--border);border-radius:10px;
    padding:.75rem .9rem;background:var(--surface);font-size:.92rem}
  .flow .step .n{font-family:var(--mono);font-size:.66rem;letter-spacing:.1em;color:var(--accent);
    display:block;margin-bottom:.3rem}
  @media (max-width:640px){.ba{grid-template-columns:1fr}.bar{grid-template-columns:4.5rem 1fr auto}}

  .doc-foot{margin-top:4rem;padding-top:1.4rem;border-top:1px solid var(--border);
    font-family:var(--mono);font-size:.72rem;color:var(--muted);display:flex;flex-wrap:wrap;gap:.4rem 1rem}

  @media (max-width:640px){.doc{padding:2.5rem 1.15rem 4rem}h1{font-size:2rem}body{font-size:1.06rem}}
  @media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
  :focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:3px}
</style>
```

## The skeleton

**Write punctuation as HTML entities** — `&middot;` `&mdash;` `&ndash;` `&times;` `&rarr;` `&hellip;`. The body-only file declares no charset of its own, so raw multibyte characters can render as mojibake.

**Escape interpolated source** — before dropping a PR diff, code, or pasted text into the HTML, replace `&` with `&amp;`, `<` with `&lt;`, `>` with `&gt;` (especially inside `<pre><code>`). Otherwise `<Component>` or `a && b` is parsed as markup and vanishes, or injects elements.

This skeleton is the **generic** order (subtitle → TL;DR → sections). For a PR, reorder to the PR flow below — Aim first, then the TL;DR card.

```html
<article class="doc">
  <p class="doc-kicker">PR Write-up <span>&middot; 2026-07-31</span> <span>&middot; repo/name #482</span></p>
  <h1>Concise, specific title</h1>
  <p class="doc-sub">One sentence framing what this is and why it matters.</p>
  <hr class="doc-rule">

  <section class="tldr">
    <h2>TL;DR</h2>
    <p>2&ndash;4 sentences. If the reader keeps one thing, it is this.</p>
  </section>

  <h2>A section</h2>
  <p>Tight prose, one idea per paragraph.</p>

  <div class="note"><span class="label">Note</span><p>Context pulled out of the flow.</p></div>
  <div class="warn"><span class="label">Watch out</span><p>The risk a reader would miss.</p></div>

  <div class="table-wrap"><table>
    <thead><tr><th>Thing</th><th>Detail</th></tr></thead>
    <tbody><tr><td>&hellip;</td><td>&hellip;</td></tr></tbody>
  </table></div>

  <pre><code>// code scrolls horizontally inside its own box</code></pre>

  <footer class="doc-foot"><span>Generated with html-doc</span><span>2026-07-31</span></footer>
</article>
```

## Visual kit

Reach for these before a paragraph. Set bar `width` inline; that is allowed, only scripts are blocked.

```html
<figure>
  <div class="ba">
    <div class="ba-col before"><span class="lbl">Before</span>
      <span class="chip">tool_a</span><span class="chip">tool_b</span></div>
    <div class="ba-col after"><span class="lbl">After &middot; flag off</span>
      <span class="chip off">tool_a</span><span class="chip off">tool_b</span></div>
  </div>
  <figcaption>What moved, in one line.</figcaption>
</figure>

<figure>
  <div class="bars">
    <div class="bar big"><span class="k">Before</span><span class="track"><span class="fill" style="width:100%"></span></span><span class="v">27 KB</span></div>
    <div class="bar"><span class="k">After</span><span class="track"><span class="fill" style="width:2%"></span></span><span class="v">565 B &middot; 48&times; smaller</span></div>
  </div>
  <figcaption>Payload size, staging.</figcaption>
</figure>

<figure>
  <div class="flow">
    <div class="step"><span class="n">01</span>First gate</div>
    <div class="step"><span class="n">02</span>Second gate</div>
    <div class="step"><span class="n">03</span>Third gate</div>
  </div>
  <figcaption>Order of operations.</figcaption>
</figure>
```

## PR flow — always this order

For a PR write-up, the body sections are fixed:

1. **Aim** — why this PR exists, the problem it solves (context, kept tight).
2. **TL;DR** — the concise summary card.
3. **Design / architecture** — the main change, shown with a before/after or diagram.
4. **Interface + visuals** — the schema/code that changed, plus the visual that makes it click.
5. **Flags & rollback** — any new feature flag, and how to roll the change back.
6. **Testing** — how it was verified.

Non-PR docs use the generic shape (kicker → title → subtitle → TL;DR → sections → footer).

## Publish

Write the file to the scratchpad, then call `Artifact`:
- `favicon` — `📄` by default, or one topic emoji; keep it stable if you redeploy the same doc.
- `title` — the doc title.
- `description` — one sentence for the gallery card.

Self-contained only: no external fonts, scripts, stylesheets, or remote images — the CSP blocks them. Embed any image as a `data:` URI.
