---
doc: decision
id: 0001
title: Google Gemini free tier as the V1 model provider
status: superseded
created: 2026-09-08
updated: 2026-09-09
supersedes: null
superseded_by: ./0006-model-provider-gemini-paid-tier.md
origin: user direction, 2026-09-08
---

# 0001 — Google Gemini free tier as the V1 model provider

> **Superseded** on 2026-09-09 by
> [decision 0006](./0006-model-provider-gemini-paid-tier.md). Gemini remains the
> provider. The free tier does not: the saving was around one dollar a month per
> hundred users, against data-handling terms this product cannot defend and a
> shared rate limit any one user could exhaust. Obligations 2 to 5 below still
> bind and are carried forward by 0006.

## Context

Every capture in Slashit runs through a model: classifying plain language into a
record type, and extracting the fields for that type. That makes the model a
per-request dependency on the product's hottest path, not an occasional call.
V1 needs a provider before the first build plan can be written.

## Decision

V1 uses Google Gemini free-tier models, called with a single API key held in the
server environment and shared across all users.

## Alternatives

| Option | Why it lost |
|---|---|
| A paid tier on any provider | Costs money before the product has proven anyone wants it |
| Per-user API keys | Asks the user to obtain a key before they can capture anything, which kills the first-run experience |
| Local or self-hosted model | Infrastructure cost and operational work out of proportion to a V1 |

## Consequences

| Good | Bad |
|---|---|
| Zero marginal cash cost per capture | The constraint moves from spend to quota, which is harder to reason about and hits everyone at once |
| No billing plumbing needed in V1 | One shared key means one shared rate limit. A single heavy user can exhaust the quota for every user |
| Fast to start, nothing to procure | Free-tier terms on data handling are generally weaker than paid terms. This product holds passport details, finances and family information |
| Provider choice stays reversible | Free-tier models and limits change without notice, and a deprecation is not ours to schedule |

## Obligations this creates

These are not optional. They belong in the first build plan that calls a model.

1. **Read the free-tier terms before launch, not after.** Specifically whether
   free-tier inputs may be used to improve the provider's products. If they may,
   either the tier changes or the user is told plainly before they type their
   first memory. Open as Q10 in the product brief.
2. **Decide the quota-exhaustion behaviour.** Queue, degrade to a
   non-model path, or refuse with an honest message. Silence is not an option
   on a capture the user believes succeeded. Open as Q11.
3. **Keep the provider behind a boundary.** Nothing above that boundary knows
   which provider is in use, so swapping to a paid tier or another vendor is a
   configuration change, not a rewrite.
4. **Instrument quota, not cost.** Requests against the limit, and how close the
   shared key is to exhaustion, per day.
5. **Have a non-model fast path for unambiguous commands where possible.**
   `/add-task Buy milk tomorrow` should not necessarily spend a model call.
   This is a build plan question, and it directly buys quota headroom.

## Reversibility

Cheap, if obligation 3 holds. Moving to a paid Gemini tier is a key and a
configuration change. Moving to another vendor is a new adapter behind the same
boundary. Costly if model calls are scattered through the codebase, which is
exactly what obligation 3 prevents.

## Scope

Binds every feature that calls a model. First applies at epic 001.
