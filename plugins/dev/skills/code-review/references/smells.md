# Code smells (Go/Python/k8s baseline)

Trimmed from Fowler's *Refactoring* ch.3 to the five that actually recur in Go/Python/k8s and multi-tenant code. Each is a judgement call, not a hard violation — a documented repo standard always overrides one of these.

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code** — the same logic shape appears in more than one hunk or file in the diff. → extract the shared shape, call it from both.
- **Primitive Obsession** — a string/int standing in for a domain concept (tenant ID, account ID, currency) that deserves its own type. → give the concept its own small type.
- **Data Clumps** — the same few fields or params keep travelling together across function signatures. → bundle them into one type, pass that.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type (e.g. per-tenant branching) recurs across the diff. → replace with polymorphism, a map, or config the cases already carry.
