---
name: prompt
description: "Turn a rough brain dump into a well-structured, optimized prompt using Anthropic's canonical prompt structure — instead of acting on the dump directly. Takes messy, half-formed input (a goal, some context, scattered requirements) and produces a clean, copy-pasteable prompt with role, task, rules, examples, input data, and output format in the right order. Use when the user pastes a dump and says 'turn this into a prompt', 'make a prompt out of this', 'write me a prompt for X', 'optimize this prompt', 'clean this prompt up', 'prompt for X', or invokes /prompt. The DEFAULT assumption when this skill fires is: produce the prompt, do NOT perform the task the dump describes."
---

# Prompt — brain dump → optimized prompt

Transform a rough brain dump into a professionally structured prompt using Anthropic's canonical prompt-engineering guidance. The output is a **prompt the user will paste elsewhere**, not the result of running that prompt.

## The one hard rule

**Produce a prompt. Do NOT execute the task the dump describes.**

If the dump says "write a Python script that dedupes a CSV", you output a *prompt that asks for that script* — you do not write the script. This is the entire reason the skill exists: the user keeps accidentally getting the work done instead of getting a reusable, optimized prompt. When in doubt, you are writing a prompt.

The only exception: if the user explicitly says "and then run it" / "and do it" after generating, you may proceed to execute in a separate step — but generate and show the prompt first.

## Inputs

- A **brain dump**: any messy, unstructured description — goal, context, constraints, examples, all jumbled.
- Optional: an **existing prompt to improve** ("optimize this prompt").
- Optional target: which model/tool the prompt is for (Claude chat, an agent, an API call). Default: Claude chat.

## Workflow

```
Parse dump → Detect missing critical elements → Ask (only if blocking) → Assemble in canonical order → Output prompt + one-line rationale
```

1. **Parse** the dump. Extract whatever maps to the canonical elements below. Most dumps have a goal + scattered context and little else.
2. **Detect gaps.** Two elements are load-bearing and worth asking about if truly absent:
   - **Goal / success criteria** — what does a good result look like, and how is it judged? Anthropic treats this as a precondition to prompting at all. If the dump has no discernible goal, ask.
   - **Examples** — the single highest-leverage element. If none exist and the task is open-ended (tone, format, style-sensitive), ask if the user can supply 1–3, or offer to draft illustrative ones for them to approve.
   - Ask via `AskUserQuestion`, batched, **only when genuinely blocking.** If the dump is rich enough to produce a strong prompt, skip questions and generate — note any assumptions you made instead.
3. **Assemble** the prompt in the canonical order (below), using XML tags to separate sections.
4. **Output** the finished prompt in a copy-pasteable block, then a 2–3 line rationale of the key choices (see Output format).

## Canonical structure (Anthropic)

Order matters. Long input data goes high; the restated request goes last. Not every prompt needs every element — include what serves the task, drop the rest.

| # | Element | Include when | Note |
|---|---------|--------------|------|
| 1 | **Role / task context** | almost always | One or two sentences: who Claude is, the overarching goal. Even one sentence measurably helps. |
| 2 | **Tone context** | tone/voice matters | e.g. "terse and technical", "warm and plain-language". |
| 3 | **Detailed task description & rules** | always | The specific task + explicit rules and constraints. State what TO do. |
| 4 | **Examples** | whenever possible | 3–5, diverse, wrapped in `<example>` tags. Highest-leverage element — push hard for these. |
| 5 | **Input data / documents** | there's data to process | Wrap in XML (`<document>`, `<data>`). If long (many pages), place ABOVE the request — up to ~30% quality gain on multi-doc inputs. |
| 6 | **The immediate request** | always | Restate the exact ask, near the END. This is what Claude answers. |
| 7 | **Think step by step** | reasoning/analysis tasks | Ask it to reason before answering. Prefer general ("think through this carefully") over a rigid step list. |
| 8 | **Output formatting** | format matters | State the exact desired format affirmatively; optionally an XML output tag. |

Prefill (a former element #9) is deliberately omitted: it is API-only and errors on current Claude models. To constrain output, use element 8 or add "Respond directly, no preamble."

The full annotated skeleton and worked before/after examples live in [`references/template.md`](references/template.md) — read it when assembling.

## High-leverage techniques to apply

Apply these while assembling — they are what separates an optimal prompt from a merely tidy one:

- **Clarity, zero assumed context.** Write for "a brilliant new employee who lacks context on your norms." If a colleague with no background would be confused, so will Claude.
- **Give the *why*.** Motivation generalizes. Not "never use ellipses" but "this is read aloud by TTS, so never use ellipses — it can't pronounce them."
- **Examples > instructions.** 3–5 diverse, relevant examples in `<example>` tags steer format/tone/structure more reliably than any description. Offer to draft or self-critique them.
- **Affirmative format control.** Say what TO do ("write flowing prose paragraphs") not what to avoid ("don't use markdown"). Match the prompt's own style to the output you want.
- **XML tags** to separate instructions / context / examples / data unambiguously.
- **Curb over-eagerness (Claude 4.x).** For scoped work add "Only do what's requested; avoid over-engineering." Soften imperatives — "Use this tool when…" beats "You MUST ALWAYS use this tool," which now over-triggers.
- **Action vs. suggestion.** "Change X to improve Y" acts; "Can you suggest changes to X" only suggests. Match the verb to intent.

## Output format

1. The prompt itself in a fenced code block (so it's cleanly copy-pasteable):

   ```
   <the assembled prompt>
   ```

2. Then, briefly (per CLAUDE.md — verdict-first, one screen):
   - **Assumptions made** — anything you filled in that the dump left implicit.
   - **Why it's shaped this way** — 2–3 bullets on the key structural choices (e.g. "examples first because tone is the hard part here", "request restated at the end for the long doc").
   - **To strengthen it** — the one change with the most leverage (usually: add/expand examples).

## Boundaries

- This skill writes prompts. It does not run them (see the hard rule).
- For a system prompt / agent instructions specifically, still use the same structure — role and rules carry more weight there; examples and immediate-request less.
- Keep the generated prompt in plain text/XML. Don't wrap it in markdown headers unless the target output is itself markdown (style bleeds into output).
