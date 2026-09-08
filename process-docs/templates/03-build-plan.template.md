---
doc: build-plan
feature: NNN-feature-slug
title: <Feature Name>
stage: 3
status: draft
owner: user
created: YYYY-MM-DD
updated: YYYY-MM-DD
approved_on: null
supersedes: null
---

# Build Plan (HLD) — <Feature Name>

Context: [PRD](./01-prd.md) · [Design](./02-design.md)

This document locks the high-level architecture. It also asks. Section 10 must
be answered by the user before approval.

## 1. Architecture summary
<Five sentences. What we are building, in what shape, on what.>

## 2. Component map
| Component | Responsibility | Talks to | New or existing |
|---|---|---|---|
| | | | |

<Diagram of the components and the calls between them.>

## 3. Data model
| Entity | Key fields | Owns | Lifecycle | Tenancy scope |
|---|---|---|---|---|
| | | | | |

Migrations required: <yes, listed / none>

## 4. API surface
| Endpoint or action | Method | Auth | Input | Output | Serves |
|---|---|---|---|---|---|
| | | | | | FR-1 |

## 5. Model and vendor choices
| Use | Choice | Why | Fallback | Est. cost per call | Latency budget |
|---|---|---|---|---|---|
| | | | | | |

Every number here is measured or labelled `estimate`.

## 6. Cross-cutting concerns
| Concern | Decision |
|---|---|
| Authentication | |
| Authorisation | |
| Tenant isolation | |
| Rate limits and quotas | |
| Cost controls | |
| Caching | |
| Observability | |
| Failure and retry | |
| Data retention and privacy | |

State the actual rule. "Same as elsewhere" is not an answer.

## 7. Alternatives considered
| Decision | Chosen | Alternatives | Why they lost | Reversibility |
|---|---|---|---|---|
| | | | | cheap / costly |

## 8. Architecture decisions to lock
| # | Decision | Status | Graduates to product/decisions |
|---|---|---|---|
| AD-1 | | proposed / locked | yes / no |

## 9. Risks
| Risk | Impact | Mitigation | Trigger to revisit |
|---|---|---|---|
| | | | |

## 10. Questions for the user
Answer before approval. Group by theme, state the recommendation.

| # | Question | Options | Recommendation | Answer |
|---|---|---|---|---|
| Q1 | | | | |

## Change log
| Date | Change | Why | Approved by |
|---|---|---|---|
