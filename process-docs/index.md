# Feature Registry

Every feature, its current gate, and where it stands. Updated in the same commit
as any stage change.

Product context: [product](./product/product.md) ·
[V1 features](./product/v1-features.md) ·
[tech stack](./tech-stack.md) ·
[V1 intake](./product/intake/2026-09-08-personal-jarvis-v1.md)

Code rulesets, binding once a feature reaches stage 5:
[backend](../backend/.claude/rules/repo-rules.md) ·
[frontend](../frontend/rules/repo-rules.md)

Settled: named Slashit, web, one account per user, commands-only capture, in-app
and email notifications, no charging in V1, no deadline. The stack, auth and
model provider are in [the tech stack](./tech-stack.md).

## Legend

| Stage | Meaning |
|---|---|
| 0 Epic | Feature argued out: requirements, pros, cons, alternatives |
| 1 PRD | Requirements locked |
| 2 Design | Screens and design system in progress or fixed |
| 3 Build plan | HLD drafted or locked |
| 4 Implementation plan | LLD drafted or approved |
| 5 Dev | Building |
| Shipped | Live, dev log closed |

Status values: `draft`, `in-review`, `approved`, `blocked`, `shipped`,
`superseded`.

## Active

| # | Feature | Priority | Stage | Status | Waiting on | Updated |
|---|---|---|---|---|---|---|
| 000 | [AI Gateway and Usage](./000-ai-gateway/) | P0, platform | 5 Dev | slices 1, 2 and 3 built, CI green, billing re-linked (RPD 10,000 confirmed) | A billing budget alert at a real spend threshold (Tier 1's built-in 250 USD cap is not an alert). Deferred: Docker (D-1), a real database for integration tests in CI, Langfuse (not needed until epic 001 calls the gateway) | 2026-09-13 |
| 001 | [Capture and Records Foundation](./001-capture-and-records-foundation/) | P0 | 5 Dev | in-review | All four slices shipped, verified end to end, including a real backend/frontend/Supabase manual pass for slice 4. `RecordEditForm` has no due-date control, logged but not fixed. No sign-in screen exists yet anywhere in the product; a dev-only console workaround stands in | 2026-09-14 |
| 002 | [Authentication](./002-authentication/) | P0, blocking | 2 Design | draft | Design in progress, now including Google sign-in and rate-limit states. Account-linking (Google vs. manual, same email) and exact lockout thresholds are open, see the PRD and design open questions | 2026-09-14 |

## Planned

Confirmed in [V1 features](./product/v1-features.md), not yet opened.

| # | Epic | Priority | Depends on |
|---|---|---|---|
| 003 | Reminders and Notifications | P0 | 001, 002 |
| 004 | Persistent Memory | P0 | 001, 002 |
| 005 | Personal Search and Context | P0 | 001, 002, 004 |
| 006 | Expenses | P1 | 001, 002 |
| 007 | Events | P1 | 001, 002 |
| 008 | Goals and Projects | P1 | 001, 002, 005 |
| 009 | Notes | P1 | 001, 002 |
| 010 | Daily Control | P1 | 001, 002, 003, 006, 007, 008 |
| 011 | Proactive Slashit | P2 | 005, 010 |

## Shipped

| # | Feature | Shipped | Dev log |
|---|---|---|---|
| — | — | — | — |
