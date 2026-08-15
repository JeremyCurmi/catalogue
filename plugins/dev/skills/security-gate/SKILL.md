---
name: security-gate
description: "Security review at any stage — an architecture proposal, an RFC, a spec, a PR diff, or a deploy config. Models the trust boundaries first, then hunts vulnerabilities against a class catalogue, and reports every finding with a concrete attack an attacker would actually run, the blast radius, and the fix. Use for /security-gate, \"is this design secure\", \"any security holes in this plan\", \"threat model this\", \"security review this PR / this terraform / this endpoint\", \"what could an attacker do here\", or before shipping anything that touches auth, money, tenants, uploads, or PII."
---

# security-gate

Find the vulnerability while it is still a sentence in a design doc. That is the only point where
it costs nothing. A review that starts at the PR is already arguing about a decision someone made
three weeks ago.

Two failure modes to avoid, both fatal to being listened to again: a wall of theoretical findings
nobody can act on, and a finding without an attack attached. Every finding here names an attacker,
a request they send, and what they walk away with.

## 1. What stage is this?

| Stage | Input | A finding means |
|---|---|---|
| **Design** | RFC, architecture, diagram, a Slack message describing an approach | a decision that makes a vuln class unavoidable later — output is *constraints*, not code |
| **Plan / spec** | ticket, plan.md, acceptance criteria | a control that is missing from the plan and so will not get built |
| **Code** | PR, branch, working tree | an exploitable path that exists right now |
| **Deploy** | terraform, k8s manifests, CI workflow, IAM policy | a misconfiguration reachable from outside the cluster |

Nothing named ⇒ review the current branch diff. Design or plan stage ⇒ read
[`references/design-review.md`](references/design-review.md) before step 2; it holds the questions
to put back to the architect and the structural anti-patterns code review can never catch.

## 2. Model it before hunting

You cannot find what you cannot see. Answer these **in writing** before the first finding — half a
screen, no more:

1. **Assets** — what is worth stealing or breaking here. Name the table, the money path, whose PII,
   which secret. "The system" is not an asset.
2. **Actors** — anonymous internet · authenticated user · a *different tenant* · support/insider ·
   a compromised dependency · the model's own output, if an LLM is in the loop.
3. **Entry points** — every place untrusted data arrives: HTTP handler, webhook, queue consumer,
   file upload, CLI flag, env var, third-party callback, tool result fed back to an agent.
4. **Trust boundaries** — where data crosses from less trusted to more trusted.

Draw the flow, boundaries marked `╎`:

```
 internet  ╎  api gateway      ╎  service            ╎  data
 attacker ─╎─▶ authn (JWT)  ───╎─▶ handler ──────────╎─▶ postgres (all tenants)
           ╎   ✗ no authz      ╎   tenant_id from body   ← boundary crossed unchecked
```

Every boundary owes three checks — **authn** (who is this), **authz** (are they allowed *this
object*), **validation** (is the data shaped and sized as expected). A boundary missing one is a
finding, not a note.

Design stage and the doc cannot answer 1–4 ⇒ those unanswered questions *are* the deliverable. Send
them back. An architect who cannot say where `tenant_id` comes from has not finished the design.

## 3. Hunt

Per entry point and per boundary, run the STRIDE prompts:

| | The question it asks |
|---|---|
| **S**poofing | can I claim to be someone else — another user, another service, another tenant? |
| **T**ampering | can I change data in flight, on disk, or a field the server assumed was server-set? |
| **R**epudiation | if I do this, is there a log that proves it was me, and can I erase it? |
| **I**nfo disclosure | what leaks — in a response, an error, a log, a timing difference, a redirect? |
| **D**oS | what is unbounded — a query, a loop, an upload, a regex, a retry? |
| **E**levation | can a user become an admin, a tenant become another tenant, an input become code? |

Then work the class catalogue in [`references/vulns.md`](references/vulns.md) — read it, do not work
from memory. It carries a minimal vulnerable snippet, the attack, and the fix per class, so a
finding can be recognised rather than guessed at. Bias the pass by what the target touches:

| Target touches | Sections to hit hardest |
|---|---|
| user-supplied IDs, multi-tenant data | A. Authorization — this is where real breaches live |
| a database, a shell, a template, HTML | B. Injection |
| login, tokens, sessions, password reset | C. Identity |
| URLs, uploads, imports, deserialization | D. Server-side data |
| keys, hashing, PII | E. Secrets & crypto |
| money, balances, counters, webhooks | F. Abuse & races |
| an LLM, tools, MCP, RAG | G. AI & agents |
| terraform, k8s, CI, IAM | H. Infra & deploy |

**No finding without a path.** Name every hop from an untrusted input to the asset. Cannot name the
hops ⇒ it is not a finding, it goes in the *Hardening* list at the bottom.

**Then verify, before writing it up.** Code ⇒ read the middleware, the caller, the policy layer that
would have stopped it, and say you read it. Design ⇒ state the assumption that has to hold for the
attack to work. Skipping this is how a security reviewer gets muted.

Large target (a whole service, a 1000-line diff) ⇒ spawn one `general-purpose` sub-agent per trust
boundary in a single message, each with the model from step 2 and one catalogue section. Small
target ⇒ one pass, no fan-out.

## 4. Report — every finding carries a working attack

Ordered strictly by exploitability × blast radius. Never alphabetical, never file order.

> ### 1. Any user can read any tenant's payouts — **Critical** · Broken object-level authz (OWASP A01)
>
> **Where** `handlers/payout.go:48`
> **Attack** — sign up as a free-tier user, take my own payout link, decrement the id:
> ```
> curl -H "Authorization: Bearer $MY_TOKEN" https://api.example.com/v1/payouts/8814
> → 200 {"tenant_id": 3, "amount": 41200, "iban": "MT84…"}
> ```
> **Why it works** — the handler authenticates the JWT and then loads by primary key. Nothing ever
> compares the row's `tenant_id` to the caller's.
> **Blast radius** — every payout of every tenant, enumerable in one loop. IBANs and amounts.
> **Fix**
> ```go
> - row, err := db.GetPayout(ctx, id)                       // authenticated ≠ authorized
> + row, err := db.GetPayoutForTenant(ctx, id, claims.TenantID)
> ```
> **The rule** — authentication says *who*; authorization says *which rows*. Any query keyed on a
> client-supplied id needs the tenant/owner in the `WHERE`, not in an `if` after the fetch.

Severity, anchored — not vibes:

| | Reachability × impact |
|---|---|
| **Critical** | unauthenticated, or trivially authenticated → RCE, cross-tenant data, money movement, full credential theft |
| **High** | authenticated attacker → other users' data, privilege escalation, secret disclosure |
| **Medium** | needs a precondition (a role, a race, a specific config) or the loss is bounded |
| **Low** | defence in depth; no attacker path today, but one bad refactor away |

Rules for the write-up:

- The **Attack** line is a real request, payload, or sequence. "An attacker could manipulate the
  parameter" is not an attack, it is a shrug.
- The **Fix** is a vulnerable → fixed pair at code stage; at design stage it is one constraint
  sentence, written so it can be pasted into the ticket as an acceptance criterion.
- **The rule** stays, always. The point is that the class gets spotted unaided next time.
- Say what you checked and found **clean** — a review with no clean list reads as if it looked
  everywhere, and reviews that claim that get trusted for the wrong reasons.
- Cap it at five findings plus the hardening list. More than five at design stage means the design
  is wrong at the root; say that in one paragraph instead of enumerating symptoms.

## 5. Verdict

One line: **BLOCK** (do not build/ship this shape) · **FIX FIRST** (ship after the named findings)
· **SHIP** (hardening only). Then the single thing most likely to be the actual breach, and — at
design or plan stage — the constraint list the implementer has to satisfy, phrased as acceptance
criteria so it goes straight into the ticket:

> - [ ] every payout query filters by `tenant_id` from the verified token, never from the request body
> - [ ] webhook handler verifies the HMAC signature before parsing the payload
> - [ ] the export endpoint is rate limited per tenant and paginated with a hard max

## Done

- boundaries drawn, each with a verdict against it
- every finding has an attack a person could run, a blast radius, and a fix
- clean list stated, hardening filed separately from exploitable findings
- verdict given, and at design stage the constraints are ticket-ready
