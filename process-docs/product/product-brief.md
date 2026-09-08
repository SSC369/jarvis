---
doc: product-brief
title: Jarvis Product Brief
status: draft
owner: user
created: 2026-09-08
updated: 2026-09-08
---

# Jarvis — Product Brief

The standing context every feature inherits. Read this before drafting any PRD.

> **Status: skeleton.** Only what the user has stated is recorded below. Every
> gap is an open question in section 8, not a guess. Fill this before the first
> feature PRD.

## 1. What Jarvis is
Jarvis is an AI SaaS application.

> Assumption: nothing further has been stated yet. The one-paragraph definition
> lands here once section 8 is answered.

## 2. Who it is for
| Segment | Who they are | What they are trying to do | Why today is hard |
|---|---|---|---|
| — | Not yet defined | | |

## 3. Product pillars
The three or four things Jarvis must be good at. Every feature should serve at
least one. A feature serving none is a signal to reconsider it.

| # | Pillar | What it means | What it rules out |
|---|---|---|---|
| P1 | | | |

## 4. Principles
Standing rules that apply to every feature, so each PRD does not restate them.

| # | Principle |
|---|---|
| 1 | The user can always see what the assistant did and why. |
| 2 | No silent failure. Every error state is designed, not defaulted. |
| 3 | Model cost and latency are product decisions, budgeted per feature. |
| 4 | Tenant data never crosses a tenant boundary, in storage or in a prompt. |

> These four are proposed defaults. Confirm or replace them.

## 5. Platform baseline
| Area | Decision |
|---|---|
| Surfaces | Not yet decided |
| Stack | Not yet decided |
| Auth and tenancy | Not yet decided |
| Model providers | Not yet decided |
| Data stores | Not yet decided |
| Hosting | Not yet decided |

Each of these becomes a decision record in `decisions/` once settled.

## 6. Business model
| Question | Answer |
|---|---|
| Pricing shape | Not yet decided |
| Free tier | Not yet decided |
| Unit of value | Not yet decided |
| Cost ceiling per user per month | Not yet decided |

## 7. Out of scope for the product
Product-level non-goals. Feature PRDs inherit these.

- Not yet defined.

## 8. Open questions
Answer these before the first feature PRD. They shape every downstream doc.

| # | Question | Blocks |
|---|---|---|
| Q1 | What does Jarvis do for a user in one sentence? | every PRD |
| Q2 | Who is the first customer segment, and how do we reach them? | PRD, design |
| Q3 | What is the first end-to-end job a user completes in Jarvis? | first feature |
| Q4 | Which surfaces ship first: web app, API, extension, mobile? | design, HLD |
| Q5 | Which model providers are in play, and is there a cost ceiling per user? | HLD |
| Q6 | Single tenant per account, or workspaces with multiple members? | HLD, data model |
| Q7 | What is the pricing shape, and what is the metered unit? | PRD, HLD |
| Q8 | Which compliance regimes apply, if any? | HLD |
| Q9 | What does Jarvis deliberately not do? | product non-goals |

## Change log
| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-08 | Created as skeleton | Process bootstrap | pending |
