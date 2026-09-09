---
doc: prd
feature: 000-ai-gateway
title: AI Gateway and Usage
stage: 1
status: approved
owner: user
created: 2026-09-09
updated: 2026-09-09
approved_on: 2026-09-09
supersedes: null
---

# Epic PRD — AI Gateway and Usage

> **Approved** by @user on 2026-09-09. Locked — changes require a change record (§7 of the rules).

Context: [Intake](./00-context.md) · [Product brief](../../product/product-brief.md) · [Decision 0001](../../product/decisions/0001-model-provider-gemini-free-tier.md) · [Decision 0002](../../product/decisions/0002-v1-technology-stack.md)

> **This is a platform epic and it breaks the vertical-slice rule on purpose.**
> Every other epic ends with something a person can do. This one ends with
> something no person sees. It is proven by epic 001's first successful capture,
> not by a screen. Recorded as an exception rather than pretended away, because
> the alternative, folding it into 001's build plan, would bury a security
> boundary inside another epic's architecture section.

## 1. Problem

Every capture in Slash runs through a model. `/add-task Finish docs tomorrow`
is worthless unless something resolves "tomorrow", so the model sits on the
product's hottest path rather than at its edges.

That creates three problems at once, and they have one answer between them.

The credential is the first. One provider key belongs to Slash, not to users,
and a key that reaches a browser is a key that is gone. It cannot appear in the
client, in a response, in a log, or in an error message, and none of those
happen by accident once rather than repeatedly.

The sharing is the second. One key serves everyone, so the provider sees one
customer where there are many. Nothing about the provider's own limits protects
one user from another. If one person's usage exhausts the quota, everybody's
capture fails, and there is no natural boundary to stop it.

The blindness is the third. With a shared credential and no attribution, there
is no way to answer who used what, whether the free tier can carry the product,
or which user to talk to when it cannot.

## 2. Users and jobs

| User | Job to be done | Today's workaround |
|---|---|---|
| The person capturing | Have their capture understood, and be told honestly when it cannot be | None. Without this epic there is no capture at all |
| The operator, which is you | Know whether the shared quota can carry the users on it, before it fails | None |
| Every other epic | Call a model without knowing which provider, holding a credential, or writing its own limit logic | Each epic reinventing it, badly and differently |

## 3. Goals

| # | Goal | What we measure |
|---|---|---|
| G1 | The credential never leaves the backend | Occurrences of the key outside the server environment. The only acceptable number is zero |
| G2 | Every model call is attributable to one authenticated user | Share of provider calls with a recorded user attribution |
| G3 | One user cannot exhaust the shared quota for everyone | Times the shared quota was exhausted, and by whom |
| G4 | The operator can see whether the free tier carries the load | Requests and tokens per user per day, and headroom against the provider limit |

No targets, consistent with the product brief. Instrument and read.

## 4. Non-goals

- **BYOK.** Users never supply their own key. Named as later by the source.
- **Multiple providers, key pools, model routing.** One provider, one key, one
  model choice per call site. Later.
- **Advanced cost optimisation.** Later.
- **Billing, plans and tiers.** Nothing is charged in V1. `plan` exists with one
  value so the column does not have to be added later.
- **A usage screen for end users.** The operator reads usage directly. If a user
  ever needs to see their own usage, that is its own epic.
- **Prompt or response content in the usage record.** See FR-10. This is a
  non-goal in the strongest sense.
- **Rate limiting the API generally.** This epic limits model calls. HTTP rate
  limiting is a build-plan concern for the API as a whole.

## 5. User stories

- **US-1.** As the person capturing, my input is understood, so that a command becomes a record.
- **US-2.** As the person capturing, I am told plainly when the model cannot serve me and why, so that I do not think Slash is broken or silently lost my input.
- **US-3.** As the operator, I see usage per user, so that I know whether the free tier carries the product before it stops.
- **US-4.** As the operator, I cap one user's usage, so that one person cannot take the product down for everyone.
- **US-5.** As another epic, I ask for a structured extraction and get one, without knowing the provider or holding a credential.

## 6. Functional requirements

### The credential

| id | Requirement | Priority | Story |
|---|---|---|---|
| FR-1 | The provider credential is read from the server environment only. It is never checked into the repository, never in the client bundle, and never in a configuration file the client can fetch. | must | — |
| FR-2 | No API response, error body, or error message returned to a client contains the credential, in whole or in part. | must | — |
| FR-3 | No application log, at any level, records the credential. Provider errors are logged with the credential removed. | must | — |
| FR-4 | The client never sends a provider credential. A request carrying one is treated as a client error, not as a credential to use. | must | — |
| FR-5 | Only the gateway holds or uses the credential. No other component reads it, and no other component calls a provider directly. | must | US-5 |

### Attribution and limits

| id | Requirement | Priority | Story |
|---|---|---|---|
| FR-6 | Every model call is made on behalf of exactly one authenticated user, identified by `user_id`. | must | US-3 |
| FR-7 | An unauthenticated request never reaches a provider. | must | — |
| FR-8 | Each model call is checked against that user's limit before the provider is called, not after. | must | US-4 |
| FR-9 | A user over their limit is refused with an honest message saying they are over their limit and when it resets. The refusal is distinguishable from a provider outage and from an exhausted shared quota. | must | US-2 |
| FR-10 | The per-user limit is configurable without a code change or a deploy. | should | US-4 |

### Usage

| id | Requirement | Priority | Story |
|---|---|---|---|
| FR-11 | Every model call records: user, provider, model, input tokens, output tokens, total tokens, estimated cost, and when it happened. | must | US-3 |
| FR-12 | A usage record never contains prompt content, response content, or any part of the user's captured text. Counts only. | must | US-3 |
| FR-13 | A call that fails is recorded too, with its outcome, so failures are visible rather than absent. | must | US-3 |
| FR-14 | The operator can read usage per user and in total, over a period, including requests against the provider's own limit. | must | US-3 |
| FR-15 | Usage is recorded even when recording it fails to complete cleanly, or the failure is itself surfaced. Usage data is never silently lost. | should | US-3 |

### Serving other epics

| id | Requirement | Priority | Story |
|---|---|---|---|
| FR-16 | A caller asks the gateway for a structured extraction and receives either a result or a typed failure. The caller never names a provider, holds a credential, or parses a provider-specific response. | must | US-5 |
| FR-17 | Provider and model are configuration, changeable without touching a caller. | must | US-5 |
| FR-18 | Provider failures are distinguished from each other and surfaced as distinct outcomes: unavailable, timed out, shared quota exhausted, per-user limit reached, and a malformed result. Callers act on the difference. | must | US-2 |
| FR-19 | A call that exceeds its time budget is abandoned rather than left hanging, and reported as timed out. | must | US-2 |
| FR-20 | A failed call is retried only where retrying is safe and useful, and a retry never doubles a recorded usage entry. | should | US-3 |

## 7. Non-functional requirements

| id | Requirement | Number | How it is measured |
|---|---|---|---|
| NFR-1 | The credential does not appear outside the server environment. | Zero occurrences | Secret scanning on the repository and on log output, in CI |
| NFR-2 | Gateway overhead is small against the provider call it wraps. | Under 50 ms at p95, excluding provider time | Server timing around the provider call |
| NFR-3 | Every provider call carries a user attribution. | 100% | Count of provider calls against count of usage records |
| NFR-4 | A model call has a bounded lifetime. | Timeout set in the build plan, enforced always | Calls exceeding the budget, which should be zero after abandonment |
| NFR-5 | Usage recording does not slow the user's capture. | Under 10 ms added at p95 | Timing with and without recording |
| NFR-6 | Usage data survives a process restart. | No loss | Reconciliation of provider calls against stored records |

## 8. Success metrics

Instrumented from launch, no targets.

| Metric | Instrumented by | What it tells us |
|---|---|---|
| Requests and tokens per user per day | Usage records | Whether the free tier carries the load |
| Headroom against the provider's own limit | Requests against the published limit | How close the shared key runs to the edge |
| Refusals by cause | FR-18 outcomes | Whether users hit their own limit, the shared quota, or outages |
| Share of calls that are retried | Retry outcomes | Whether the provider is reliable enough to build on |
| Distribution of usage across users | Usage records | Whether one user dominates the shared credential |

## 9. Dependencies

| Dependency | Type | Owner | Status |
|---|---|---|---|
| Google Gemini free tier | vendor | user | Settled, [decision 0001](../../product/decisions/0001-model-provider-gemini-free-tier.md) |
| The actual API key | vendor | user | Supplied at implementation, by the user's statement. Nothing here needs it |
| Auth provider, so `user_id` exists | platform | user | Provider chosen, which one is open |
| FastAPI, PostgreSQL, AWS EC2 | platform | user | Settled, [decision 0002](../../product/decisions/0002-v1-technology-stack.md) |
| Gemini free-tier rate limits, read from current documentation | vendor | Claude | Not started, needed for the build plan |
| Gemini free-tier data handling terms | vendor | user | Not read. Blocks launch |

## 10. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| The key leaks through a log line, a stack trace, or an error returned to a client | medium | severe | FR-2, FR-3 and NFR-1 with secret scanning in CI. A leak is not recoverable by patching, it is recoverable only by rotating |
| One user consumes the shared quota and every other user's capture fails | high | high | FR-8 checks before calling, FR-10 makes the cap tunable without a deploy, FR-9 makes the refusal legible, G3 measures it |
| Prompt content reaches the usage table, putting passports and finances in an analytics store | medium | severe | FR-12 forbids it outright. This is the single most likely way the product leaks user data into a place nobody thought of as sensitive |
| Attribution is skipped on some path, so usage looks lower than it is | medium | medium | NFR-3 reconciles provider calls against usage records rather than trusting the code |
| The gateway becomes the place every future feature adds a special case | medium | medium | FR-16 keeps the caller contract narrow. A caller asks for extraction, not for a provider |
| Cost estimation gives false comfort, since a free tier bills nothing | high | low | Cost is recorded as an estimate. Quota headroom is the number that matters in V1, per G4 |

## 11. Open questions

| # | Question | Blocks | Owner | Answer |
|---|---|---|---|---|
| Q1 | What is the per-user limit, and over what window: requests per day, per hour, tokens per month? | FR-8, FR-10 | user | |
| Q2 | Is streaming needed in V1? Extraction returns a record, not prose, so there may be nothing to stream. Dropping it removes real complexity from the gateway. | FR-16, scope | user | |
| Q3 | How is estimated cost computed on a tier that bills nothing: the paid-tier rate card as a shadow price, or zero? A shadow price tells you what the product would cost if it grew. Zero tells you nothing. | FR-11 | user | |
| Q4 | How long are `ai_usage` rows kept? They are small, they accumulate per capture, and they are the record that proves attribution. | FR-11, HLD | user | |
| Q5 | Does the operator read usage through a screen, a query, or a periodic report? A query is free, a screen is an epic. | FR-14 | user | |
| Q6 | When the shared quota is exhausted, epic 001 refuses honestly. Should the gateway also alert the operator, and how? | FR-18 | user | |
| Q7 | Which auth provider, since `user_id` originates there? | FR-6, HLD | user | |

## 12. Out of scope

Everything in the product non-goals, plus BYOK, provider pools, model routing,
cost optimisation, billing, plan tiers, a user-facing usage screen, and general
HTTP rate limiting.

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-09 | Created from the AI API key architecture | User supplied the architecture and asked for it as an epic | user |
| 2026-09-09 | **PRD approved.** Seven open questions carried to the build plan; none blocked approval. | User said proceed | user |
