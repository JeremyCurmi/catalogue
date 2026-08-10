---
name: code-review
description: "Review a GitHub PR across six angles — security, code smells, over-engineering, tech debt/hardcoding, spec compliance, correctness. An optional first arg picks who reviews: claude (default, one parallel sub-agent per angle), or an external agent like codex or grok, so a different model challenges code Claude wrote. Use when the user says \"review this PR\", \"review PR #123\", \"review this with codex\", asks for a PR review, or wants a second opinion before merging."
---

Args: `[<agent>] [<pr>] [--comment]` — e.g. `code-review`, `code-review codex 123`, `code-review grok --comment`. Agent defaults to `claude`. `--comment` defaults off; on, the review gets posted to the PR as one comment.

## Context

Fetch context: `gh pr view <n> --json title,body,url` for the description, `gh pr diff <n>` for the diff. If the user names a branch instead of a PR number, resolve it with `gh pr view <branch>` first.

Look for the spec: an issue link in the PR body (`Closes #`, `Fixes #`, etc.) fetched via `gh issue view`. None found → the Spec angle reports "no spec, skipped" — don't block the other five on it.

## The six angles

Whoever reviews gets the diff, the PR description, and this shared brief:

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

## Run it — `claude` (default)

Spawn all six as `general-purpose` sub-agents in **one message** so they run in parallel and don't pollute each other's context.

No sub-agent tool available — you are Codex or another host reading this file directly — → one self-contained pass per angle instead, and don't let a later angle lean on an earlier one's findings. Ignore the next section; you *are* the external agent.

## Run it — external agent (`codex`, `grok`, …)

The point is that a different model challenges code Claude wrote. So don't review it yourself: drive the CLI, then check what it claims.

1. **Binary check.** Not on `PATH` → say `<agent> is not installed` and stop. Don't silently fall back to Claude.
2. **Throwaway worktree at the PR head.** These CLIs sandbox without network, so the diff must be on disk, and the main checkout must stay untouched:
   ```bash
   git fetch origin <headRefName>
   git worktree add --detach <repo-root>/.worktrees/<agent>-review-pr-<n> FETCH_HEAD
   ```
   Write the PR title + body to `pr-<n>.md` in there, plus the spec issue text if any.
3. **Prompt**, written to `prompt.txt` in the worktree:
   - The PR URL, and: this diff was written by Claude Code, not a human — assume it is plausible-looking and wrong somewhere; falsify it, don't praise it.
   - No network; everything is local: `git diff <base>...HEAD`, `./pr-<n>.md`, the spec file or "no spec — skip that angle and say so".
   - 2–4 lines of repo context pulled from `CLAUDE.md` — conventions a stranger would otherwise flag wrongly. Skip this and the review wastes findings on house style.
   - The six angles above, plus the shared brief. Agent already has this skill → say `Use $code-review on <PR URL>` instead of restating them: `~/.codex/skills/code-review` for Codex (`ln -s <repo>/plugins/dev/skills/code-review ~/.codex/skills/code-review`), a `[skills] paths` entry in `~/.grok/config.toml` for Grok (it also installs this marketplace directly).
   - `Review only. Do not modify any files.`
   - Close with `BLOCK` or `SHIP`, the single most likely defect, and "name anything this Claude-written diff got right in a way that looks wrong, so I don't 'fix' it back into a bug."
4. **Invoke, read-only, from the worktree** — never a bypass-sandbox or full-access flag, this is a read:

   | Agent | Command |
   |---|---|
   | codex | `codex exec -s read-only --skip-git-repo-check - < prompt.txt` |
   | grok | `grok --prompt-file prompt.txt --permission-mode plan --output-format plain` |
   | other | `<agent> --help` for its headless + read-only flags |
5. **Verify.** The external model is *different*, not *more correct*. Per finding, check the actual code and mark `holds` or `wrong, because …`. Misreading a repo convention is the usual failure; the repo is the tiebreak, not the model.
6. `git worktree remove <path> --force`.

## Aggregate

One `##` heading per angle, findings underneath verbatim. Don't merge, re-rank, or pick one worst issue across angles — each angle catches a failure mode a merged list would bury. End with a one-line count per angle. External agent → its output verbatim, then your `holds` / `wrong` line per finding.

## `--comment`

Off → don't touch the PR; mention it's available.

On → one comment via `gh pr comment <n> --body-file <file>`: the review verbatim, headed by which model produced it, with the verification verdict attached to each finding. Never post a finding as fact without that verdict, and never edit the reviewer's words to make them look right.
