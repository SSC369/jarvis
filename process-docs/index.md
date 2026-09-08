# Feature Registry

Every feature, its current gate, and where it stands. Updated in the same commit
as any stage change.

Product context: [product brief](./product/product-brief.md) ·
[V1 epic map](./product/v1-epic-map.md) ·
[V1 intake](./product/intake/2026-09-08-personal-jarvis-v1.md)

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

## Active

| # | Feature | Priority | Stage | Status | Waiting on | Updated |
|---|---|---|---|---|---|---|
| 001 | [Capture and Records Foundation](./features/001-capture-and-records-foundation/) | P0 | 1 PRD | in-review | User review of the PRD | 2026-09-08 |

## Planned

Proposed in the [V1 epic map](./product/v1-epic-map.md), not yet opened.

| # | Epic | Priority | Depends on |
|---|---|---|---|
| 002 | Persistent Memory | P0 | 001 |
| 003 | Personal Search and Context | P0 | 001, 002 |
| 004 | Expenses | P1 | 001 |
| 005 | Events | P1 | 001 |
| 006 | Goals and Projects | P1 | 001, 003 |
| 007 | Notes and Life Inbox | P1 | 001 |
| 008 | Daily Control | P1 | 001, 004, 005, 006 |
| 009 | Proactive Jarvis | P2 | 003, 008 |

## Shipped

| # | Feature | Shipped | Dev log |
|---|---|---|---|
| — | — | — | — |
