# Feature Registry

Every feature, its current gate, and where it stands. Updated in the same commit
as any stage change.

Product context: [product brief](./product/product-brief.md) ·
[V1 epic map](./product/v1-epic-map.md) ·
[V1 intake](./product/intake/2026-09-08-personal-jarvis-v1.md) ·
[decisions](./product/decisions/)

Settled: web, one account per user, commands-only capture, in-app and email
notifications, no charging in V1, no deadline. Stack and model provider are
[decisions 0001 and 0002](./product/decisions/).

## Legend

| Stage | Meaning |
|---|---|
| 0 Intake | Requirement captured, not yet interpreted |
| 1 PRD | Epic PRD drafted or approved |
| 2 Design | Screens and design system in progress or fixed |
| 3 Build plan | HLD drafted or locked |
| 4 Implementation plan | LLD drafted or approved |
| 5 Dev | Building |
| Shipped | Live, dev log closed |

Status values: `draft`, `in-review`, `approved`, `blocked`, `shipped`,
`superseded`.

> **Name is open.** Slash is a working name only, see
> [decision 0003](./product/decisions/0003-product-name-and-mark.md).

## Active

| # | Feature | Priority | Stage | Status | Waiting on | Updated |
|---|---|---|---|---|---|---|
| 000 | [AI Gateway and Usage](./features/000-ai-gateway/) | P0, platform | 3 Build plan | PRD approved 2026-09-09, no design stage | Build plan | 2026-09-09 |
| 001 | [Capture and Records Foundation](./features/001-capture-and-records-foundation/) | P0 | 2 Design | in-review | User review of the design canvas | 2026-09-09 |

## Planned

Confirmed in the [V1 epic map](./product/v1-epic-map.md), not yet opened.

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
| 010 | Proactive Slash | P2 | 004, 009 |

## Shipped

| # | Feature | Shipped | Dev log |
|---|---|---|---|
| — | — | — | — |
