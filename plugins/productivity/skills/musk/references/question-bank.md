# Question bank

Starting sets by scenario. Pick the three or four that change the next move here — never fire the whole list. Ordered roughly by how often they crack the case.

## Model / LLM output is wrong, gibberish or degraded

1. Show me one bad output and the exact input that produced it. (No paraphrase — the raw pair.)
2. What changed in the last 24h — model version, prompt, temperature, retrieval index, provider-side deprecation?
3. Is it every request or a slice? Which slice — tenant, language, prompt length, tool path?
4. Does the previous version reproduce it on the same input? (Isolates model from everything around it.)
5. Is bad output *reaching users*, or is it caught upstream?
6. Do we have a pinned version to fall back to, and how fast can we point at it?

Note: a provider silently rerouting or deprecating a model is a delta even when nothing on your side moved.

## Service down / hard outage

1. Who is seeing it — synthetic checks, real users, one region, one customer?
2. What deployed, migrated or rotated most recently? Any expiring cert, token or quota?
3. Is it degrading, flat, or recovering on its own?
4. Is the dependency ours or someone else's? What does their status page say?
5. Can we roll back right now, and does rollback lose data?
6. Who is talking to customers, and what have they been told so far?

## Data pipeline / bad numbers

1. Which specific number is wrong, and what should it be? (No answer to this = no incident yet.)
2. Since when — first bad partition or run?
3. Did upstream schema, volume or timing change?
4. Is it wrong in the source, in the transform, or only in the dashboard?
5. Who has already acted on the wrong numbers, and what did they decide?
6. Can we backfill, or is the original data gone?

## Security / suspected breach

Escalate on the security path before you ask around. These questions run alongside that, never instead of it.

1. What exactly was seen, in which log, at what timestamp?
2. What could this credential or path reach — data, environments, other systems?
3. Is access still live?
4. Do we need to preserve evidence before anything is changed or restarted?
5. Who legally or contractually has to be told, and on what clock?

## Vendor / third-party outage

1. Confirmed on their status page, or just our inference?
2. What of ours degrades gracefully vs fails hard?
3. Is there a fallback provider or cached path, and has it ever been exercised?
4. What's their stated ETA — and what do we do if it's wrong by 5×?
5. Is this the second time? Then the real question is contractual, not technical.

## Big technical bet — rewrite, migrate, build vs buy

Slower and more deliberate: this is a one-way door, so the requirement itself is the target.

1. Whose requirement is this — the person, by name? What happens to them if we do nothing?
2. What breaks at 10× that doesn't break today? Is 10× actually coming?
3. What's the smallest version that tests the risky assumption this quarter?
4. Which part can we delete rather than build? (Every deleted part costs zero and never breaks.)
5. What does it cost to undo in six months?
6. What would have to be true for this to be the wrong call — and can we check that now?
