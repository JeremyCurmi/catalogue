---
name: linear-issue
description: Write or update a Linear issue the factory pipeline can actually build — the required lines, the labels, the template, and what each pipeline node reads. Use when filing, grooming, or rewriting a ticket that will be delegated to the agent (triage → planner → builder → qa → ready), when reshaping an existing issue into the template in place, or when a delegation failed for lack of context.
---

# Writing a Linear issue for the factory

A run starts when you **delegate the issue to the agent in Linear**, or prompt an existing agent
session again. Whatever you type in that prompt box is **discarded** — the worker dispatches with an
empty prompt. The description plus human comments are the entire brief, and the agent runs
**headless**: nobody answers a question posted mid-run, and the agent never edits your description.

One delegation = one dispatch of a fixed pipeline (`triage → planner → builder → qa → ready`, plus
a `scout` branch for hotfixes).

Two nodes read your words directly:

- **triage** classifies the ticket into `hotfix | bug | feature | chore` and resolves the target
  repo and branch name. The type is frozen on first pass and **routes the pipeline**.
- **planner** turns the ticket into an implementation plan (attached to the issue as
  `Implementation plan`). It treats the user story and acceptance criteria as **given** — it will
  not author them for you. Its job is only the *how*.

The **builder** then works test-first, one acceptance criterion at a time, from that plan. So the
quality ceiling of the whole run is set by your acceptance criteria.

## Before you file

**Dedupe.** Search open issues (`list_issues`) for the same symptom or component. If one already
exists, add your new evidence to it and stop. Two tickets for one symptom means two agents building
the same thing.

## Hard requirements

| Requirement | Why | What happens without it |
|---|---|---|
| `Target repo: owner/name` (or bare `name`) as a **bare line** | A Linear delegation carries no repo — the ticket is the only place it is named | The run **fails**, not stops |
| A title that reads as the change | First five words become the branch slug: `<type>/<id>-<slug>`, capped at 60 chars | A branch named after a vague title |
| At least one testable acceptance criterion | The builder drives one AC red-to-green at a time | The plan invents its own criteria; QA and review have nothing to check against |

**Bare line means bare line.** `Target repo:` and `Type:` are matched at the start of a line, with
nothing but whitespace allowed before the key. Bullet it or bold it and it is silently ignored — and
a missing target repo fails the run.

```markdown
GOOD  Target repo: my-service
GOOD  Target repo: `my-service`              (backticks on the value are fine)
GOOD  target repo: my-org/my-service         (case-insensitive)
BAD   - Target repo: my-service              (the "-" kills it)
BAD   **Target repo:** my-service            (so does the "*")
BAD   | Target repo | my-service |
```

Prerequisite, not a ticket field: the target repo must have **required status checks** configured.
Required checks are the only verification interface — a repo with none is a stop, because a build
nothing verified never reaches review.

## What the pipeline reads, and how to feed it

**Type** — resolved in this order, first hit wins: ledger (already classified) → a Linear label
(`hotfix`, `bug`, `feature`, `chore`; a `kind/feature`-style label works, the last segment is
read) → a `Type: <word>` line in the description → the triage agent reading the whole ticket.
Nothing has to be labelled, and the type is **frozen on the ledger after the first pass** —
relabelling mid-flight does not re-route the work. Get it right before the first delegation.

State the type when the routing matters, because:

- **`chore` skips the planner entirely.** No plan, straight to the builder. Right for a dep bump
  or a rename; wrong for anything where a reader could notice the result. Mislabel a feature as a
  chore and you get an unplanned build.
- **`hotfix` goes to the scout, not the planner.** The scout investigates read-only, attaches a
  `Hotfix investigation` report, labels the issue `hotfix:awaiting-approval`, and the run **ends**.
  A human swaps the label for `hotfix:approved` and prompts the session again; only then does it
  plan and build. Use `hotfix` only for production broken *now* — severity is the signal, not diff
  size.
- `bug` = expected result vs actual, on behaviour meant to work already. An enhancement to
  something that works is a `feature`, not a bug.

**Links and evidence** — a Slack permalink anywhere in the description, a comment, or an
attachment is parsed out and read as evidence (and replied to in-thread) by the scout. Trace,
dashboard, and incident links are read as prose. Paste them; don't summarise them away.

**Comments** — read by triage, the planner and the scout. Fine for adding architecture notes
after filing. Don't put the primary brief there; put it in the description.

**Attachments** — the planner reads the scout's report off the issue's attachments and plans the
fix a human approved rather than re-diagnosing. Your own design docs are best pasted or linked in
the description; the planner reads the description, not arbitrary attachments.

## Labels the factory reads

Five labels are the runtime's whole label contract on a Linear issue:

| Label | Written by | Removed by | Human action at this gate |
|---|---|---|---|
| `agent:ready` | **Human only** — never write this yourself; the runtime never applies it | Runtime, once it starts working the issue | Add it to queue an issue for the dispatcher |
| `agent:working` | Runtime, on a proceeding triage pass | Runtime, when the issue's PR merges or closes | None — informational |
| `blocked` | Human | Human | Remove it to release the block |
| `hotfix:awaiting-approval` | Runtime (the scout) | Runtime, on approval | Add `hotfix:approved` |
| `hotfix:approved` | Human | Runtime | Add it to approve the hotfix |

`agent:ready` and `agent:working` are Linear **workspace** labels — already usable on every
team's board, so filing on a new team needs no label setup for them. An issue carrying both is
**working**, not ready: `agent:working` wins. Don't add `agent:working` yourself; it is how the
runtime marks an issue as already in flight so nothing re-queues it.

## The template

Copy this into the Linear description. Delete sections that genuinely don't apply — don't leave
placeholders in.

```markdown
Type: feature
Target repo: my-service

## User story
As a <role>, I want <capability>, so that <outcome>.

## Context
Why now, and what a reader needs to know that the code doesn't say. Prior art, the ticket or
incident this came from, links to traces / dashboards / Slack threads / docs. Two to five
sentences — not a design doc.

## Acceptance criteria
- [ ] Given <state>, when <action>, then <observable result with a concrete value>.
- [ ] ...

## Technical notes
Where the change belongs — files, modules, endpoints, symbols. Constraints the agent cannot infer:
schema/API compatibility, auth boundaries, feature flags, config keys, expected load. Name a
preferred approach when you have one; the planner takes it as given rather than re-deciding.

## Out of scope
What this ticket deliberately does not do, and the follow-up it implies.

## Test plan
How each criterion is verified — unit, integration, e2e, or "verified by X" where a test adds no
signal (infra wiring, a migration, a UI layout). Name the required checks that must go green.
```

For a **bug or hotfix**, replace *User story* with:

```markdown
## Symptom
What is broken, for whom, since when. Expected vs actual.

## Evidence
Where it was seen — trace / log / dashboard / Slack link, first sighting, blast radius (how many
users, tenants, rows), and anything already tried that did not work.
```

## Updating an existing issue

Reshaping a ticket that already exists into this template is a **reformat, not a rewrite**. The
issue already carries the author's intent; your job is to move it into the template's shape and fill
the gaps the pipeline needs — never to change what the ticket asks for.

1. **Read it first** — `get_issue` (with `includeRelations` if the issue links others). Work from
   the actual current description, not your memory of it.
2. **Map, don't invent.** Every existing sentence lands in a template section: the goal → *User
   story* / *Symptom*, the background → *Context* / *Evidence*, each stated requirement → one
   *Acceptance criterion*, any file or constraint the author named → *Technical notes*. Preserve the
   author's own values, numbers, links, and repo — verbatim.
3. **Fill only what the pipeline requires**, and only where the existing text already implies it: a
   missing `Target repo:` bare line, a requirement written as prose turned into a testable AC bullet,
   an ambiguous expected value made concrete *if the ticket already says what it should be*. A gap
   you cannot fill from the existing text is a question for the human — leave a note, don't guess.
4. **Never** add a requirement, drop one, relax an expected value, or re-scope. If the ticket says
   "returns 401", it stays 401. If reshaping seems to need a behaviour the ticket never stated, that
   is a signal you're rewriting — stop.
5. **Write back** — `save_issue` with the issue `id` and the reshaped `description`. Editing the
   description is safe; it does not re-dispatch a run.

Two things a reformat cannot change after the first delegation: **type** (frozen on the ledger — a
`Type:` edit won't re-route) and, once the PR is open, the **branch** (the open PR's head branch wins
over any name recomputed from an edited title). Reshape the prose freely; know these two are settled.

## Writing acceptance criteria the builder can build

The builder writes **one failing test per criterion**, watches it fail, then writes the minimum
code to pass. So each criterion must be:

- **Individually testable** — one behaviour per bullet. A bullet with "and" in it is two.
- **Observable at the public interface** — a return value, an HTTP response, a row written, a
  metric moved. Not "the `_cache` dict is populated".
- **Concrete in its expected value** — `returns 422 with {"error": "expired"}`, not "handles it
  gracefully". A criterion whose expectation is computed by the code under test always passes.
- **Bounded** — if a criterion needs its own plan, it is its own ticket.

```markdown
BAD  - [ ] Webhook handling is more robust.
BAD  - [ ] Expired webhooks are rejected and logged and metrics are emitted.
GOOD - [ ] Given a webhook whose `timestamp` is older than 300s, when POSTed to `/gh`,
           then the response is 401 and no workflow dispatch is made.
```

## Sizing

Caps are per PR: **20 total actions, 3 CI-fix rounds, 5 review rounds.** A ticket that exceeds them
is blocked with the `blocked` label, not looped on. One ticket = one coherent PR a reviewer can
read in a sitting. Break an epic into tickets and let each one carry its own story and criteria.

## Asks that need saying explicitly

- **Evals**: the agent adds an eval example *only* if the ticket asks for it. Say so in the
  acceptance criteria, naming the dataset file the example belongs in. An unrequested eval is scope
  the agent was not given.
- **Repo choice** when the work could land in more than one — including the pipeline's own repo.
  One target repo per ticket.
- **Migrations, feature flags, config**: name the key or the migration, or the agent will invent one.

## Anti-patterns

- **Questions the agent is expected to answer before starting.** Nobody reads them mid-run. Decide,
  or state the assumption you want made.
- **A title or body that only makes sense with the Slack thread you didn't link.**
- **"Fix the failing test"** with no expected behaviour — the builder is forbidden from fixing the
  check instead of the cause, so a ticket with no stated correct behaviour goes nowhere.
- **Asking for a check to be skipped, `# noqa`'d, or a security finding waived.** The agent will
  refuse; a waiver is a human's call.
- **Multi-repo tickets.** One `target repo` per ticket. Split them and link the two.
- **Pasted logs and stack traces measured in screens.** Link them, or keep the ten relevant lines.
- **Relabelling the type after the first delegation.** It is frozen; you will be working the PR by
  hand. (Editing the *title* after the PR opens is safe — the open PR's head branch wins over any
  freshly computed name. The branch just stops matching the title.)

## Pre-delegation checklist

- [ ] `Target repo:` present as a bare line — not bulleted, not bold
- [ ] Type stated (or clearly inferable) — and `chore` / `hotfix` chosen deliberately
- [ ] Title reads as the change; its first five words make a sensible branch slug
- [ ] User story or symptom present
- [ ] Every acceptance criterion is one behaviour, observable, with a concrete expected value
- [ ] Technical notes name files/modules and any constraint the code cannot show
- [ ] Out of scope stated
- [ ] Evidence links pasted (Slack, trace, dashboard, incident) for bugs and hotfixes
- [ ] Eval asked for explicitly, if wanted
- [ ] Scope fits one PR
- [ ] Target repo has required status checks configured
- [ ] **If updating an existing issue:** every requirement, value, link and repo from the original
  survives the reshape — nothing added, dropped, or relaxed
