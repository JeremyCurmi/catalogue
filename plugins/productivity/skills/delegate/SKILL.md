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

| Unit | Agent type |
|---|---|
| Needs this chat's context | fork |
| Build / edit / multi-step | general-purpose |
| Find code, sweep files | Explore |
| Design an approach | planner |
| Verify a change works | qa |
| External research | researcher |
| Live incident, read-only | sre |

## Hold the line
- Step out of the orchestrator role only to ask the user a blocking question you can't resolve.
- Send rework back to a subagent the same way — don't patch its output inline.
