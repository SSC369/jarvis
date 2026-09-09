---
doc: epic
feature: 000-ai-gateway
title: AI Gateway and Usage
stage: 0
status: approved
owner: user
created: 2026-09-09
updated: 2026-09-09
approved_on: 2026-09-09
supersedes: null
---

# Epic — AI Gateway and Usage

> Written on 2026-09-09 as `00-context.md`, under the old intake contract: record
> the requirement, interpret it in the PRD. The stage 0 contract changed on
> 2026-09-09 to require pros, cons, best practices and alternatives. This
> document was renamed, not retrofitted, because the feature is already past this
> gate and through an approved PRD. New features use
> [the epic template](../templates/00-epic.template.md).

Full source as supplied:
[AI API Key Architecture](../product/intake/2026-09-09-ai-api-key-architecture.md).
Nothing is restated here that lives there.

## Requirement as stated

The user's principle, in their words:

> One Slashit-managed AI credential, many authenticated users, with usage tracked
> independently per user.

And the rule the whole epic exists to hold:

> The API key must never be stored in the app, sent to the client, returned in
> API responses, stored in normal application logs, or exposed to users.

## Product details supplied

| Topic | Detail | Source |
|---|---|---|
| Credential ownership | Slashit holds one provider key in the server environment. No per-user keys | §2, §4 |
| Request path | Authenticated request, identify user, check limits, then the gateway calls the provider | §3 |
| Gateway duties | Call providers, hold credentials, select model, handle requests and errors, track tokens and estimated cost | §6 |
| Usage record | user_id, provider, model, input tokens, output tokens, total, estimated cost, created_at | §7 |
| Users record | id, email, plan, created_at | §7 |
| Security boundary | Backend trusted and holds the key. Frontend untrusted and holds nothing | §8 |
| Deliberately later | Multiple providers, key pools, BYOK, model routing, cost optimisation | principle |

## Constraints given

- The frontend knows only Slashit APIs. It never learns a provider credential.
- One shared credential serves every user, so isolation is enforced by
  attribution and limits rather than by separate keys.
- The user will supply the actual key at implementation time. Nothing in this
  epic requires the real key to be planned or built.

## Anything the user said not to do

No BYOK, no provider pools, no model routing, no advanced cost optimisation in
V1. All named as later.

## Immediate unknowns

Carried into the PRD.

| # | Unknown |
|---|---|
| U1 | What the per-user limit actually is, and per what window |
| U2 | Whether `ai_usage` may ever hold prompt or response content |
| U3 | Whether streaming is needed, given extraction returns a record rather than prose |
| U4 | How estimated cost is computed on a tier that bills nothing |
| U5 | Whether `plan` carries more than one value in V1, given nothing is charged |
