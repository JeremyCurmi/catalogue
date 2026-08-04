---
name: handoff
description: "Compact the current conversation into a handoff document another agent can pick up cold. Use when you are out of context, switching sessions, or handing work to someone else."
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

# Handoff

Write a handoff document summarising this conversation so a fresh agent can continue the work. Save it to the OS temp directory — **never** the workspace.

Args from the user describe what the next session is for. Aim the whole document at that.

## What goes in

Summarise the conversation. Length follows the work — a one-file fix needs a few lines, an agreed plan needs the plan.

Two things are easy to lose and worth stating outright:

- **What was decided, and what was ruled out and why.** The next agent cannot see the conversation. Without this it re-opens choices you already settled.
- **What is still open** — unresolved questions, assumptions you made, anything a human must confirm.

End with a **Suggested skills** section naming the skills the next agent should invoke.

## Rules

- **Redact** API keys, passwords, PII.
- **Link, don't paste.** Specs, plans, ADRs, issues, commits and diffs already exist — reference them by path or URL.

## Kickoff prompt

Print the absolute path, then this in a fenced block (not in the file):

```text
Pick up the work at: <ABSOLUTE_PATH>

Read the whole file first — you cannot see the conversation it came from.
Build only what it scopes. If you must deviate, stop and say why.
Report back: files changed, test results, deviations, anything a human must look at.
```

If the doc is research or design talk rather than a build, swap the middle two lines for: *read it, then continue from the open questions.*

Add below: *if the agent cannot read local files, paste the file contents above this prompt.*
