# Card format

## The bar Jeremy set

> * visualizes content that can be visualised
> * uses bullet points
> * is super minimal and short
> * keeps only the relevant information even if it is not made up of content that is
>   grammatically / punctually correct

Grammar is optional. Density is not.

## What got rejected first

A faithful prose digest — headed sections, full sentences, every step of the source covered in
order. Verdict: *"still way too much jargon"*. It was ~700 words and read like the article.

| Rejected | Why |
|---|---|
| `**1. Your score is partly about your judge.**` then four sentences | a paragraph wearing a bullet's clothes |
| "the industry moved to API calls almost overnight" | the source's framing, not a fact he needs |
| covering all six steps evenly | the source's structure, not the useful shape |
| "faithfulness / trajectory-level / component-level" left bare | terms he now has to go look up |
| a follow-up offer per section | he asked for less, not more |

The fix in one line: **stop transcribing the argument, start posting the conclusions.**

## Shapes

Flow — a gate, a pipeline, a decision path. Fail branches go right, the happy path goes down:

```
agent opens a change
        │
        ▼
  ① tests / types / schema  ──fail──▶ closed
        │ pass
        ▼
  ② was the path clean?     ──messy─▶ closed
        │ yes
        ▼
      merge
```

Bars — tiers, magnitudes, how-much-of-each. Width carries the meaning:

```
easy to undo, small   ██████  open first
easy to undo, wide    ███     needs checks
hard to undo          ─       never opens
```

Nesting — layers that contain each other. The indentation is the point:

```
┌─ HARNESS ── what the model can touch ─────────────────┐
│  tools · files · memory · sandbox · permissions       │
│   ┌─ GRAPH ── what's allowed to run next ─────────┐   │
│   │    ┌─ LOOP ── try → check → fix → repeat ─┐   │   │
│   │    └──────────────────────────────────────┘   │   │
│   └───────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────┘
```

Table — symptom → fix, X vs Y, when to reach for which:

| symptom | fix here |
|---|---|
| can't do the thing · forgets · too much access | harness |
| quits early · never quits · doesn't check its work | loop |

Keep diagrams under ~70 columns so they survive a narrow terminal. Use `·` as an inline separator
inside a box, `→` for turns into, `▶` for a branch out.

## Gold example

Source: *Eval Engineering: build the gate that lets your agents merge without you* — 1,746 words in,
~320 out.

---

# 1 · Eval Engineering
*build the gate that merges agent work without you*

```
agent opens a change
        │
        ▼
  ① tests / types / schema  ──fail──▶ closed
        │ pass
        ▼
  ② was the path clean?     ──messy─▶ closed
        │ yes
        ▼
  ③ rolled back here before? ──often─▶ closed
        │ no
        ▼
      merge                    agent's own "I'm confident"
                               ▶ counts least. it's the one
                                 input the model can game
```

**which changes are even allowed in the gate**

```
easy to undo, small   ██████  open first   (copy, tests, isolated fn)
easy to undo, wide    ███     needs ①+②    (shared util, new schema)
hard to undo          ─       never opens  (migrations, deletes, money, prod data)
```

**the rest, short**

- your judge is not neutral. same outputs → one judge said 93%, another said 40%
- models over-score their own family. so judge with a different vendor. panel for big calls
- anything a script can check → script, not a judge
- a score on a dashboard changes nothing. thermometer vs thermostat
- "agent stopped calling tools" ≠ "task finished". only an outside check knows
- grade 3 things: did it work · was the route sane · which tool broke
- best test cases are already in your logs → clean run · run the user corrected · tool returned
  empty · same tool called twice with same args · external timeout
- traces show what it *did*, never what it *should* have. answer key comes from elsewhere
- test your checker first: feed it one obviously right + one plausibly wrong answer
- pin the judge version, log it with every score. silent upgrade = last month's numbers are noise
- rubric = one line: "pass if <thing> actually happened"
- never score length, keywords, or looks-like-the-reference → it learns to look right, not be right
- 500+ cases. run shorter than a coffee break or it becomes a quarterly ritual
- turn it on in shadow first: scores everything, merges nothing
- fully green suite + broken product is normal. green is evidence, not proof

> you're not building trust in the agent. you're building a constraint tight enough that trust
> stops being the question

---

Note what the card does *not* have: no intro, no section per source-step, no "the author argues
that", no closing summary of the summary. The pull-quote is the only full sentence in it.
