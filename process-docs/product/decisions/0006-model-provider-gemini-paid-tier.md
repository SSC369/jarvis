---
doc: decision
id: 0006
title: Google Gemini paid tier as the V1 model provider
status: accepted
created: 2026-09-09
updated: 2026-09-09
supersedes: ./0001-model-provider-gemini-free-tier.md
origin: user direction, 2026-09-09
---

# 0006 — Google Gemini paid tier as the V1 model provider

## Context

[Decision 0001](./0001-model-provider-gemini-free-tier.md) chose the Gemini free
tier and immediately opened an obligation against itself: read the free-tier
data-handling terms before launch, because free-tier terms generally permit a
provider to use inputs to improve its products. That became Q10 in the product
brief, marked as blocking launch, and it has stayed open.

Slashit holds passport details, finances and family information. On 2026-09-09
the user confirmed the product is intended for real users. The question stopped
being theoretical.

The arithmetic settled it. The free tier was not saving a meaningful amount of
money, and it was buying a data-handling risk and a shared rate limit that any
one user could exhaust for everyone.

## Decision

V1 uses Google Gemini Flash on a paid tier, called with a single Slashit-held
API key in the server environment, behind the gateway of
[epic 000](../../features/000-ai-gateway/).

The provider and the model family are unchanged from decision 0001. The tier is
not.

## The arithmetic

> `estimate`. Derived from published Gemini Flash pricing as recalled on
> 2026-09-09, not read from a vendor page. Confirm before relying on it.

| Input | Assumption |
|---|---|
| Tokens in per capture | 500, being the prompt, the type schema, and the user's text |
| Tokens out per capture | 150, being one extracted record |
| Input price | 0.10 USD per million tokens |
| Output price | 0.40 USD per million tokens |

| Result | Value |
|---|---|
| Cost per capture | about 0.0001 USD |
| A heavy user at 100 captures a month | about 0.01 USD |
| One hundred such users | about 1 USD a month |

The saving the free tier offered was on this order. The risk it carried was the
product's most sensitive data.

## Alternatives

| Option | Why it lost |
|---|---|
| Stay on the free tier | Costs almost nothing to leave and carries data-handling terms this product cannot defend to a user. Also one shared rate limit, exhaustible by one person |
| A paid tier on another vendor | No reason to move. The gateway boundary keeps this cheap to revisit if Gemini disappoints on quality or price |
| Free tier now, paid before launch | The migration is a key and a configuration change either way, so the only thing deferral buys is the chance of forgetting. It also means every pre-launch capture, including the user's own real data during development, runs under the weaker terms |
| Per-user API keys | Unchanged from decision 0001. Asks a user to obtain a key before capturing anything |
| Local or self-hosted model | Unchanged from decision 0001. Infrastructure out of proportion to a V1 |

## Consequences

| Good | Bad |
|---|---|
| Paid-tier data-handling terms are defensible to a user holding passports in the product | A billing relationship, a payment method, and a bill that can surprise |
| Rate limits are per project and far above V1 volume, so one user exhausting capture for everyone stops being the likely failure | The constraint moves from quota to spend, so a runaway user or a retry loop now costs money rather than returning an error |
| Cost per user becomes a real measured number rather than a shadow price, which matters for the pricing question the brief defers as Q5 | The product now has a marginal cost per user, which the business model section recorded as zero |
| Quota headroom stops being the metric that decides whether the product can carry its users | Epic 000 was written around a shared free quota. Parts of it now describe a problem that has changed shape. See below |

## What this changes in epic 000

The gateway's mechanisms all survive. Their purpose shifts.

| Element | Was | Becomes |
|---|---|---|
| Per-user caps, FR-8 and FR-10 | Protect the shared free quota from one heavy user | Protect the bill from a runaway user or a retry loop |
| Goal G4, free tier carries the load | Whether the quota holds | Whether cost per user is sustainable |
| Estimated cost, FR-11 and Q3 | A shadow price on a tier that bills nothing | A real charge, reconcilable against the provider's invoice |
| Refusal on exhaustion, FR-18 | Shared quota exhausted | Per-user cap reached, or provider outage |

The epic 000 PRD is approved, so these are recorded there as a change entry and
not rewritten here.

## Obligations this creates

Obligations 2 to 5 of decision 0001 carry over unchanged and are restated only
by reference. Obligation 1 is replaced.

1. **Read the paid-tier data-handling terms before launch.** Weaker terms are no
   longer the expectation, but "better than free tier" is not the same as
   "read". Q10 in the product brief narrows to this and stays open.
2. **Keep the provider behind a boundary**, per decision 0001 obligation 3. This
   record depends on it.
3. **Instrument spend as well as quota.** Decision 0001 said to instrument quota
   and not cost. That is now backwards. Both.
4. **Set a billing alert at the provider before the first real user.** A cap on
   the account is the only defence that works while nobody is watching.

## Reversibility

Cheap, as long as the gateway boundary of decision 0001 obligation 3 holds.
Moving between Gemini tiers is a key and a configuration change. Moving to
another vendor is a new adapter behind the same boundary. Returning to the free
tier is equally cheap and would reopen Q10 in its original, blocking form.

## Scope

Binds every feature that calls a model. First applies at
[epic 000](../../features/000-ai-gateway/).

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-09 | Created, superseding decision 0001 | User accepted the recommended stack, which moved the model provider to a paid tier | user |
