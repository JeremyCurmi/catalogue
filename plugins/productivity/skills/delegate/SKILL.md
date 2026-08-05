---
name: delegate
description: Fan independent tasks out to subagents and stay the orchestrator. Use for "/delegate", "delegate this to an agent team", "split these across agents", or a big task / list of tasks you want run by a team instead of inline.
---

# delegate

You are the orchestrator. Do none of the task work yourself — decompose, spawn, synthesize. Delegating as much as possible is the whole point of invoking this.

## Steps

1. **Split.** Break the request into the smallest units that stand alone. A single big task ⇒ split into sub-tasks. An explicit list ⇒ one unit per item.
2. **Map dependencies.** Mark which units need another's output. Independent units run together; dependent ones wait for their input.
3. **Pick an agent per unit** (table below). Write each a self-contained brief — it cannot see this chat, so give it the goal, the files/paths, and what "done" returns.
4. **Spawn.** All independent units in ONE message (multiple Agent calls) so they run concurrently. Dependent units go in the next round, fed the prior output.
5. **Synthesize.** Collect results, resolve conflicts, report back. Relay what matters — subagent output never reaches the user on its own.

## Pick the agent

Read the agent types this session actually offers before you route anything — they differ per project and setup. Then match each unit by what it needs:

| Unit | Route to |
|---|---|
| Needs this chat's context | an agent that forks the conversation, if one is offered — otherwise write the context into the brief |
| Find code, sweep files | the read-only search agent |
| Everything else | the general-purpose one |

Where the session defines a specialist that fits — a planner, a verifier, a researcher, an on-call reader — prefer it over the general-purpose fallback.

## Hold the line
- Step out of the orchestrator role only to ask the user a blocking question you can't resolve.
- Send rework back to a subagent the same way — don't patch its output inline.
