---
name: tldr
description: "Compress an article, X thread, paper or long doc into a terse visual card Jeremy can read in under 2 minutes — ASCII diagrams, bullet fragments, plain words, no jargon. Use when he pastes a link and says tldr, \"summarise this\", \"what does this say\", \"help me consume this\", or drops something long he does not want to read. Reaches x.com articles that WebFetch cannot. For a source he hands over — not for the conversation itself; restating something already said here is `summarize`."
---

# tldr

The deliverable is a **card**, not a summary. If it has to be read start to finish, it failed.

## 1. Get the full text

| Source | How |
|---|---|
| `x.com/*/status/*` | `scripts/fetch-source.py <url>` — WebFetch gets 402 from X, and an X Article is not in the page HTML |
| Any other URL | WebFetch, asking for the full text verbatim |
| PDF, local file | Read |
| Pasted text | already here |

Behind a paywall or a bot wall ⇒ say so and stop. A card built from search snippets is fiction
with a confident voice, and he cannot tell the difference by looking at it.

## 2. Cut to the load-bearing part

Keep claims, numbers, names, rules, and the shape of any process.
Cut setup, hedging, why-this-matters, the author's plug, and every restatement.

2000 words in ⇒ ~300 out. Not 10× smaller means not done cutting.

## 3. Draw whatever has a shape

Prose describing a flow is a diagram he has to render in his head. Draw it instead.

| Content | Shape |
|---|---|
| pipeline, gate, decision path | vertical ASCII flow, `▼` between stages, fail branches to the right |
| layers containing layers | nested boxes |
| tiers, magnitudes, rankings | bar row — `██████` · `███` · `─` |
| symptom → fix, X vs Y, when-to-use | table |

## 4. Write it

- fragments over sentences. `judge ≠ neutral` beats `it is worth noting that judges are not neutral`
- one fact per bullet, no bullet past two lines
- plain words. an unavoidable term gets defined inline in three words
- keep the numbers, they are the evidence — `one judge 93%, another 40%` earns its space
- one pull-quote, the single line worth remembering
- say it when a stat has no named source behind it

Read [`references/format.md`](references/format.md) before writing the first card — it holds the
two cards Jeremy signed off and the shapes to copy.

Terminal markdown by default. HTML artifact only when he wants to keep it.

## Done

Card posted. Reads in under two minutes. Every section is a bullet list, a table or a diagram.
