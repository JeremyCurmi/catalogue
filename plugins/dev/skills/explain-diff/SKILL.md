---
name: explain-diff
description: "Walk the user through a PR's diff before they approve it — why the PR exists, then the change grouped and explained — as an HTML artifact, then a graded quiz. Use for /explain-diff, \"explain this PR\", \"walk me through PR #123\", \"what does this diff do\", \"help me understand this change before I approve it\"."
---

# explain-diff

The point is that the user approves nothing they can't explain back. Explain the diff from the code, never from the PR description alone — a description that lies about the diff is exactly what this catches.

## 1. Get the change

| Source | How |
|---|---|
| PR number / URL | `gh pr view <n>` + `gh pr diff <n>` — description *and* diff |
| Current branch | `git diff <base>...HEAD`, base usually `main` |

Ambiguous which PR ⇒ ask. One question, then move.

## 2. Understand — fan out to fresh agents

Split the diff into logical slices (by feature/directory, off `git diff --stat`). Spawn one subagent per slice so the code-reading burns *their* context, not the main thread's. Each reads its hunks plus the code around them — callers, tests, data model — and returns a digest, not raw code:
- **What** changed, one line.
- **Why** it exists / how the code behaved **before**.
- **Risk** — the line a reviewer would miss, with file:line.

Small PR ⇒ one agent. The description says what the author *meant*; the diff says what changed — when they disagree, trust the diff and flag it. Main keeps only the digests.

## 3. Build the artifact

From the digests, not by re-reading the code. Reconcile any risk that spans slices — each agent was blind to the others. Read the `artifact-design` skill, write the HTML to the scratchpad, publish with `Artifact`. Structure:

| Section | Holds |
|---|---|
| Why this PR | the problem, beginner-approachable, 3–4 sentences |
| Intuition | the change as one before/after, a toy example, HTML/CSS diagram — never ASCII |
| The change | grouped by idea, not file-by-file — file:line refs, not full diff dumps |
| Watch for | the risk, the edge case, what the author may have got subtly wrong |

Approachable prose over exhaustive. He can open the diff himself; the artifact earns its place by making it *click*.

## 4. Quiz

Post the URL, wait for him to read it, then invoke the `quiz-me` skill on the same PR — 3 questions, graded. Terminal by default: producing the answer is what proves he understood the diff, not recognising it. If he'd rather stay in the artifact, quiz-me's interactive mode serves the same questions as a clickable HTML quiz — offer it.

## Done

URL posted, quiz-me run and scored, gaps named. If he missed a load-bearing question, say plainly he's not ready to approve yet.
