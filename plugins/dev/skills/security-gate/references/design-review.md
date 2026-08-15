# Reviewing a design, before anyone writes code

Read this when the target is an RFC, an architecture proposal, a spec, a ticket, or someone
describing an approach in a message.

Code review catches a missing check. Design review catches the reason the check will be missing
everywhere, forever. The findings here are structural: trust placed in the wrong tier, a tenant key
chosen too late, an audit trail nobody designed, a blast radius nothing can contain. None of them
are visible in a diff — by then the shape is already load-bearing.

## The questions to put back to the architect

A design that cannot answer these is not finished. Asking them *is* a valid output — do not invent
answers on the architect's behalf to have something to review.

**Identity & authorization**
- Who calls this — an end user, another service, a partner, an unauthenticated visitor?
- Where does the caller's identity come from, and who verified it? A header from the gateway is a
  claim; a verified token is evidence.
- What is the authorization *unit* — user, account, tenant, organisation? Who owns each object?
- Where is that decision enforced — handler, service, repository, database? One layer only, or does
  every new endpoint have to remember?

**Data & tenancy**
- Which fields are PII, financial, or regulated? Who is allowed to read each?
- In a shared database, what stops tenant A reading tenant B — a `WHERE` clause developers must
  remember, or a mechanism (RLS, per-tenant credentials, a repository that takes tenant from context)?
- Retention and deletion: how long is it kept, and what does "delete my account" actually do?

**Integration**
- What crosses the network, to whom, over what, authenticated how?
- Inbound webhooks or callbacks: how is the sender proven, and what happens on replay?
- Which third parties see the data, and what do they retain?

**Secrets**
- What new secrets does this need, where do they live, who can read them, how are they rotated, and
  what is the procedure the day one leaks?

**Failure & abuse**
- What happens when a dependency is down — does it fail closed, or open? (An auth check that fails
  open under load is a design decision; make it a conscious one.)
- What is the most expensive request someone can send, and what bounds it?
- Which operations are irreversible, and what stops them being replayed or raced?

**Operations & audit**
- Who can access production data, through what path, and is that access logged?
- If this were abused, what in the logs would prove it — who, what, when, and is that log tamper-evident?

## Design-stage anti-patterns

Each is a *shape*, not a bug — spot it in prose and it never reaches code.

| In the doc it reads like | Why it is broken |
|---|---|
| "the frontend only shows the button to admins" | authz in the client; the API is the boundary, and it is open |
| "it's on the internal network / behind the VPN, so it doesn't need auth" | flat trust — one SSRF, one compromised pod, one contractor laptop and everything inside is reachable |
| "the service passes `tenant_id` down to the query" | isolation by convention; correct until the one handler that forgets |
| "we'll add rate limiting / audit logging later" | never lands, and retrofitting an audit trail means the history you needed is gone |
| "each customer gets an API key" (no rotation, no revocation, no expiry) | a leak is permanent and there is no lever to pull on the day it happens |
| "we encrypt it at rest" (no key ownership stated) | the key sits beside the data; the property claimed is not the property delivered |
| one database user, full access, shared by every service | every service inherits the blast radius of the loudest one |
| "the ID is a UUID so it can't be guessed" | ids are not secrets — they leak via logs, referrers, support tickets, exports |
| a feature flag or an unlinked URL used as the access control | obscurity, discoverable by anyone reading the bundle |
| "the client sends the price / the score / the role" | server-authoritative values crossing an untrusted boundary |
| a token in a URL, a redirect, or a QR code | lands in logs, proxies, history |
| PII copied into analytics, logs and a model provider "for debugging" | three new places to breach, each with its own retention you do not control |
| one shared service account across tenants or environments | staging can reach production; no attribution in any audit log |
| "the model decides whether the action is allowed" | probabilistic access control; the check has to be deterministic and outside the model |

## Blast radius — the question worth asking on any design

*Assume one component is fully compromised. What does the attacker reach next?*

Run it for the most exposed component and for the one with the widest credentials. If the answer is
"everything", the finding is not a missing check — it is the absence of a segmentation boundary, and
that is far cheaper to add on a whiteboard than after launch.

Look for: credentials scoped wider than the job needs, a service that can reach every other service,
a token that works in every environment, backups readable by the same role that writes them.

## Writing the output

Design-stage findings are **constraints**, not patches. Write each so it can be pasted into the
ticket and later verified by a code reviewer who was not in this conversation:

> - [ ] `tenant_id` is derived from the verified access token inside the repository layer; no handler
>       accepts it from the request
> - [ ] the payout endpoint requires re-authentication and is rate limited to 5/hour/account
> - [ ] provider webhooks verify the HMAC over the raw body before parsing, and reject timestamps
>       older than 5 minutes
> - [ ] the export job runs as a read-only DB role with a 30s statement timeout

Then say which decision, if it goes the other way, would force the whole design to be reworked
later. That is the one worth arguing about now.
