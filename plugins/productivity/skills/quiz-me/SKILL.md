---
name: quiz-me
description: "Quiz the user on a source — a PR, blog post, paper, or YouTube video — to verify they actually understood it, graded question by question. Runs in the terminal by default, or as an interactive multiple-choice artifact when they ask. Use for /quiz-me, \"quiz me on this PR\", \"test my understanding of X\", \"do I get this paper\", \"make me an interactive quiz on X\", or before signing off on agent-generated code they skimmed."
---

# quiz-me

Verify the user actually understood the source — catch where they'd rubber-stamp agent code or skim a paper. The questions are the product: one they can answer without having understood is wasted.

## 1. Ingest

Get the source from the invocation. Read it in full before writing a question — a question built from a summary tests the summary, not the source.

| Source | How |
|---|---|
| PR | `gh pr view <n>` + `gh pr diff <n>` — description *and* the diff |
| Blog / paper URL | WebFetch |
| YouTube | fetch the transcript (`yt-dlp --skip-download --write-auto-subs`, or a transcript site) |
| Local file / current branch | Read / `git diff` |

## 2. Write the questions

Default 5; honour a different count if they ask. Grounded in this source only.

- Test reasoning, not recall. "Why does X deny table funcs?" beats "what does X do?" — recall he passes without understanding.
- For a PR, aim where review goes soft: why the change is correct, what breaks without it, the edge case the diff handles, what the agent got subtly wrong.
- One question per load-bearing idea. Skip the trivia.

## 3. Run

**Terminal** (default) — ask Q1, wait, grade, then Q2. He must not see later questions while answering. Make him produce the answer, no options. Grade each as it lands: right / partial / wrong + the one thing he missed. On a miss, give the correct answer and why the wrong take was tempting. Grade what he wrote — don't lead him to it.

**Interactive** — when he asks to click or arrow through it ("interactive", "multiple choice", "as an artifact"): build one self-contained HTML artifact, reading `artifact-design` first. All questions, multiple choice, keyboard-driven (↑↓ select, Enter answer, → next). On answer the chosen box goes green if right / red if wrong, the correct one is marked, and its explanation shows; end on a score + per-question recap. Distractors carry the weight — same length and shape as the answer, or the formatting is the tell.

## Done

Every question asked and graded. Close with a score and the gaps worth re-reading.
