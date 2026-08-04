# Prompt template — annotated skeleton + worked examples

Reference for the `prompt` skill. The skeleton below is the canonical Anthropic
element order. Fill what serves the task; delete elements that don't apply.
XML tag names are Anthropic's suggested conventions.

## Annotated skeleton

```
You are <role>. <One-sentence overarching goal.>                         ← 1. Role / task context

<Tone: e.g. "Be terse and technical. No filler.">                        ← 2. Tone context (optional)

<instructions>                                                           ← 3. Task description & rules
Your task is to <specific task>.

Rules:
- <explicit rule — state what TO do>
- <constraint, with the WHY when non-obvious>
- Only do what is asked; avoid over-engineering.
</instructions>

<examples>                                                               ← 4. Examples (3–5, diverse)
<example>
Input: <representative input>
Output: <the ideal response for that input>
</example>
<example>
Input: <a DIFFERENT-shaped input — edge case, other format>
Output: <ideal response>
</example>
</examples>

<document>                                                               ← 5. Input data (long data → keep high)
<the data / text / code to operate on>
</document>

<Restate the exact request here, in one or two sentences.>              ← 6. Immediate request (near the end)

Think through this carefully before you answer.                         ← 7. Think step by step (optional)

<Output: state the exact format. e.g. "Return only valid JSON matching     ← 8. Output formatting
this shape: {…}. No prose." OR "Respond in flowing prose paragraphs.">
```

Ordering rules that matter:
- **Long documents go near the TOP** (before instructions/request) — up to ~30% quality gain on multi-doc inputs.
- **The restated request goes near the BOTTOM** — it's what Claude answers.
- Short data can sit inline where shown (element 5).

---

## Worked example A — vague dump

**Dump (user input):**
> need a prompt that summarizes customer support tickets, want it short, pull
> out the main issue and how angry they are

**Generated prompt:**
```
You are a customer-support triage assistant. Your goal is to compress a raw
support ticket into a fast, scannable triage summary.

<instructions>
Summarize the ticket below. Extract exactly three things:
- issue: the core problem in one sentence
- sentiment: one of [calm, frustrated, angry] — judged by tone and word choice
- urgency: one of [low, medium, high] — judged by business impact and language
Do not restate the whole ticket. Do not invent details not present.
</instructions>

<examples>
<example>
Ticket: "Hi, the export button on the reports page hasn't worked since the
update this morning. Not urgent but wanted to flag it. Thanks!"
Output: {"issue": "Export button on reports page broken since morning update",
"sentiment": "calm", "urgency": "low"}
</example>
<example>
Ticket: "This is the THIRD time I've emailed. Your billing charged me twice and
nobody has responded. I want this fixed today or I'm cancelling."
Output: {"issue": "Double-charged on billing, no prior response after multiple
contacts", "sentiment": "angry", "urgency": "high"}
</example>
</examples>

<ticket>
{paste the support ticket here}
</ticket>

Summarize the ticket in <ticket> tags.

Return only valid JSON: {"issue": "...", "sentiment": "...", "urgency": "..."}.
No other text.
```

Why this shape: the dump was tone/format-sensitive, so **examples do the heavy
lifting** — one calm/low, one angry/high, to span the range. Categories are
enumerated (not free-text) so output is machine-usable. Request restated above
the format spec; format stated affirmatively as strict JSON.

---

## Worked example B — "optimize this prompt"

**Dump (existing prompt to improve):**
> "Write a blog post about our new feature. Don't make it boring. Don't use too
> much jargon."

**Generated prompt:**
```
You are a product marketing writer for a developer-tools company.

Tone: energetic and concrete. Write for working engineers — assume technical
fluency but explain our own product's specifics.

<instructions>
Write a blog post announcing <feature name>. 
- Open with the specific problem the reader has today, not a generic intro.
- Show the feature through one concrete before/after code or workflow example.
- Keep sentences short and active. Prefer plain words over marketing abstractions,
  because the audience distrusts hype and will stop reading.
- Length: 500–700 words.
</instructions>

<feature_details>
{paste: what the feature does, who it's for, the key benefit, one example}
</feature_details>

Write the announcement post based on <feature_details>.

Structure it as: a hook, the problem, the before/after example, then a short
"how to try it" close. Return the post as flowing prose with a single H1 title.
```

Why this shape: replaced both negatives ("don't be boring", "don't use jargon")
with **affirmative directives** ("short active sentences", "plain words") plus
the **why** ("audience distrusts hype"). Added the missing role, a concrete
structure, and a slot for the feature details the original prompt assumed but
never provided.
