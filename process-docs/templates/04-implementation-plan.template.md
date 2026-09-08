---
doc: implementation-plan
feature: NNN-feature-slug
title: <Feature Name>
stage: 4
status: draft
owner: user
created: YYYY-MM-DD
updated: YYYY-MM-DD
approved_on: null
supersedes: null
---

# Implementation Plan (LLD) — <Feature Name>

Context: [PRD](./01-prd.md) · [Design](./02-design.md) · [Build plan](./03-build-plan.md)

No code is written before this is approved.

## 1. Scope recap
<Three sentences. What ships in this pass, what waits.>

## 2. File-by-file plan
| Path | Action | Purpose |
|---|---|---|
| | created / modified / deleted | |

## 3. Interfaces and contracts
Type signatures and schemas for anything crossing a boundary.

```ts
// module boundary, request and response shapes, events
```

## 4. Data and migrations
| Migration | Change | Reversible | Backfill |
|---|---|---|---|
| | | yes / no | |

## 5. State management
| State | Lives in | Lifetime | Invalidated by |
|---|---|---|---|
| | | | |

## 6. Error handling
| Failure | Detected by | User sees | System does |
|---|---|---|---|
| | | | |

## 7. Test plan
Name the cases, not the intent.

| id | Level | Case | Covers |
|---|---|---|---|
| T-1 | unit / integration / e2e | | FR-1 |

## 8. Rollout
| Item | Decision |
|---|---|
| Feature flag | |
| Rollout stages | |
| Kill switch | |
| Metrics to watch | |
| Rollback plan | |

## 9. Task breakdown
Ordered. Each task independently verifiable.

| # | Task | Size | Depends on | Acceptance check |
|---|---|---|---|---|
| 1 | | S / M / L | | |

## 10. Definition of done
- [ ] All tasks shipped or explicitly dropped in the dev log.
- [ ] Test plan cases pass.
- [ ] Implementation matches the approved design, or a change record explains why not.
- [ ] Observability in place for the metrics named in the PRD.
- [ ] `index.md` updated to `shipped`.

## Change log
| Date | Change | Why | Approved by |
|---|---|---|---|
