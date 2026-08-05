---
name: code-review
description: Review a GitHub PR across six angles — security, code smells, over-engineering, tech debt/hardcoding, spec compliance, correctness — one parallel sub-agent per angle. Use when the user says "review this PR", "review PR #123", asks for a PR review, or wants a second opinion before merging.
---

Fetch context: `gh pr view <n> --json title,body,url` for the description, `gh pr diff <n>` for the diff. If the user names a branch instead of a PR number, resolve it with `gh pr view <branch>` first.

Look for the spec: an issue link in the PR body (`Closes #`, `Fixes #`, etc.) fetched via `gh issue view`. None found → the Spec sub-agent reports "no spec, skipped" — don't block the other five on it.

Spawn all six as `general-purpose` sub-agents in **one message** so they run in parallel and don't pollute each other's context. Every sub-agent gets the diff, the PR description, and this shared brief:

> Report only what's actually wrong — file:line, what's wrong, why it matters. Skip anything lint/CI already catches. Under 250 words.

Angle-specific addition to the shared brief:

| Angle | On top of the shared brief |
|---|---|
| Security | Injection, auth/authz gaps, secrets in code, unvalidated input at boundaries, unsafe deserialization. |
| Code smells | Check against `references/smells.md` — read it before writing the brief. |
| Over-engineering | Abstraction, config, or flexibility the diff doesn't need yet. Name what to delete or inline. |
| Tech debt / hardcoding | Hardcoded values that should be config/env, magic numbers/URLs, shortcuts that break at 10x scale or a second tenant. |
| Spec compliance | Diff vs. the linked issue: missing requirements, undone scope creep, requirements that look done but aren't. Skip if no spec. |
| Correctness | Logic errors, edge cases, race conditions, off-by-one — actual bugs, not style. |

Aggregate: one `##` heading per angle, findings underneath verbatim. Don't merge, re-rank, or pick one worst issue across angles — each angle catches a failure mode a merged list would bury. End with a one-line count per angle.
