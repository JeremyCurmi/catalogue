---
name: html-doc
description: "Produce a beautiful, repeatable HTML document — a PR write-up, an AI-concept explainer, or any content meant for a human to read — published as a claude.ai Artifact in one locked house style. It makes a standalone reference doc to keep and share: not a graded quiz (that's quiz-me) and not an approval walkthrough (that's explain-diff). Fire whenever the user wants a polished, shareable HTML doc/page/write-up instead of terminal text or a plain markdown reply: 'make an HTML doc for this', 'write this up as a page', 'document this PR beautifully', 'explain this concept as a readable page', '/html-doc'."
---

# html-doc

Turn content into a document a human actually wants to read, and make it look the same every single time. The locked house style is the whole point — apply it, don't redesign.

## 1. Gather

| Source | How |
|---|---|
| PR number / URL | `gh pr view <n>` + `gh pr diff <n>` — description *and* the real diff |
| Concept / topic | Read the source you were given; if none, use what you already know, no fabricated facts |
| Pasted content | Use it as-is — HTML-escape it when you insert it (see step 3) |

Ambiguous what to document ⇒ ask once, then move.

## 2. Structure

Show, don't tell — lead each point with the interface, a diagram, or a comparison from the visual kit (before/after chips, compare bars, flow steps, code, table). Words are captions, not paragraphs; cut any sentence a visual already makes. A TL;DR card is always mandatory — first for a generic doc, right after Aim for a PR.

**PR docs — always this fixed order:** Aim → TL;DR → Design/architecture → Interface + visuals → Flags & rollback → Testing.
**Anything else** — generic shape: kicker → title → subtitle → TL;DR → sections → footer.

Fixed PR flow, visual-kit markup, and full component list are in the reference.

## 3. Build

Read [`references/house-style.md`](references/house-style.md). Paste its `<style>` block verbatim and reuse its component markup; order the sections per step 2 (the skeleton shows the generic order — for a PR, lead with Aim). Escape `&` `<` `>` in any code or text you insert (especially inside `<pre><code>`) so source shows literally instead of being parsed as markup. Write the HTML to the scratchpad. Do not invent a new palette, font, or layout — re-deriving the look each run is exactly the failure this skill exists to prevent. `artifact-design` calibration is already spent, this house style is its output; if `Artifact` prompts you to load it, change nothing.

## 4. Publish

Call `Artifact` on the scratchpad file: `favicon` `📄` (or one topic emoji), `title` = the doc title, one-line `description`. Self-contained only — no external fonts, scripts, or remote images. Post the returned URL.

## Done

URL posted. Reads clean top-to-bottom, TL;DR present, theme-aware in light and dark, nothing scrolls the page sideways.
