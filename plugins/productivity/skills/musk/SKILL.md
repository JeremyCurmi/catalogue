---
name: musk
description: "Triage a critical question or incident that just landed on a team lead — read the situation, fire the few questions that actually change the next move, and make the call. Use for /musk, \"P1 just landed\", \"the model is returning gibberish\", \"prod is down and I need to lead this\", \"an engineer is asking me X — what do I ask back\", \"help me triage this fast\"."
---

# musk

Something just landed on the lead mid-flow and it is critical. Your job is not to solve it — it is to get them *oriented in seconds* and asking the questions that collapse the uncertainty fastest. Named for the first-principles habit: question the requirement, cut what isn't load-bearing, decide, move.

Speed is the feature. Output the block in **one pass** — short enough to read standing up. No preamble, no "great question", no restating what they told you.

## 1. Read it

Classify before you ask anything. The playbook diverges hard.

| What landed | What wins |
|---|---|
| **Broken now** — outage, P1, bad output in prod | Stop the bleeding *before* root cause. Diagnosis is not the job yet. |
| **Fork in the road** — build/buy, rewrite, migrate | Reversibility sets your speed. Question the requirement before optimising the answer. |
| **Blocked person** — engineer stuck, needs a ruling | Unblock in one move now, fix the reason it reached you later. |

Then read three dials, one line total: **blast radius** (who's hit, is it growing), **clock** (how fast it worsens), **door** (two-way = reversible, decide now; one-way = slow down).

## 2. Ask

The whole skill is here. **Only ask what changes the next move.** If both answers lead to the same action, the question is noise — cut it. Cap at five, ranked by how much each one moves the decision.

Give each as: *question — who to ask — what it changes.* Whoever you name must have seen it themselves.

The ones that usually earn their place:

- **Ground truth** — who has observed this with their own eyes, and what exactly did they see? Separate observed from inferred from relayed.
- **Delta** — what changed? Deploy, config, data, upstream, traffic, provider. This is the answer most of the time.
- **Blast radius** — how many affected, since when, growing or flat?
- **Rollback** — can we revert, how fast, and what does it cost us?
- **Requirement** — whose requirement is this, by name? (A department is not a name.) The fastest fix is the work you delete.

Do not ask what you can look up yourself, what only matters for the postmortem, or anything phrased so vaguely it returns a status update.

`references/question-bank.md` has scenario-specific sets — model/LLM output, service down, data pipeline, security, vendor outage, big technical bets. Read it when the situation matches one.

## 3. Move while you wait

Nobody idles on an open question. Every strand gets **one name and a checkback time** — an action without a name attached does not happen. Mitigation, investigation and comms run in parallel, not in sequence.

The lead stays the lead. If they're deep in a stack trace, nobody is steering.

## 4. Call it

Decide at ~70% information. State the decision, the assumption holding it up, and what would reverse it. If it genuinely can't be called yet, say which answer unlocks it — never leave it hanging.

## Output

```
READ   <type · blast radius · clock · door>
ASK    1. <question> — @who — <what it changes>
       2. …
NOW    <parallel action> — @who, by <time>
CALL   <decision, or "on Q1"> · assumes <x> · reverses if <y>
```

Anything not paste-able into Slack in one go is too long.

## When answers come back

They'll paste replies. Re-run it: drop what's answered, fold it into READ, re-rank what's left, sharpen or make the CALL. Kill any question the answers made irrelevant instead of asking it out of habit.

## Hold the line

- Don't debug it yourself — that's the lead's classic failure mode.
- Mitigate first. Root cause is a postmortem, and the postmortem is not now.
- Question the requirement before optimising the solution.
- Never guess a fact and present it as one. "Unknown — @who by 14:00" is a legitimate line.
