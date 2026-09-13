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
| 000 | [AI Gateway and Usage](./000-ai-gateway/) | P0, platform | 5 Dev | slices 1, 2 and 3 built, CI green | Deferred per user direction: re-linking billing (D-12, account on free-tier RPD 20 for now, single-user only), spend cap/billing alert, Docker (D-1), a real database for integration tests in CI. Deferred as not yet needed: Langfuse, since nothing calls the gateway until epic 001 builds | 2026-09-13 |
| 001 | [Capture and Records Foundation](./001-capture-and-records-foundation/) | P0 | 2 Design | in-review | User review of the design canvas | 2026-09-09 |

## Planned

Confirmed in [V1 features](./product/v1-features.md), not yet opened.

| # | Epic | Priority | Depends on |
|---|---|---|---|
| 002 | Reminders and Notifications | P0 | 001 |
| 003 | Persistent Memory | P0 | 001 |
| 004 | Personal Search and Context | P0 | 001, 003 |
| 005 | Expenses | P1 | 001 |
| 006 | Events | P1 | 001 |
| 007 | Goals and Projects | P1 | 001, 004 |
| 008 | Notes | P1 | 001 |
| 009 | Daily Control | P1 | 001, 002, 005, 006, 007 |
| 010 | Proactive Slashit | P2 | 004, 009 |

## Shipped

| # | Feature | Shipped | Dev log |
|---|---|---|---|
| — | — | — | — |
