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
split: false
---

# Implementation Plan (LLD) — <Feature Name>

Context: [PRD](./01-prd.md) · [Design](./02-design.md) · [Build plan](./03-build-plan.md)

No code is written before this is approved.

## 1. Scope recap
<Three sentences. What ships in this pass, what waits.>

## 2. Split decision
Check the thresholds. Under all of them, keep one document and delete the slice
table below.

| Trigger | Threshold | This feature |
|---|---|---|
| Tasks in the breakdown | more than 15 | |
| Files created or modified | more than 25 | |
| Independently shippable slices | more than one | |
| Distinct boundaries touched | more than two | |
| Length of the drafted plan | more than 500 lines | |

**Decision:** single document / split into N sub-plans.

### Slices
Only when split. Vertical slices, each ending in something that works end to
end. Split by slice, never by layer.

| # | Sub-plan | What works when it lands | Depends on | Status |
|---|---|---|---|---|
| 1 | [04.1-<slug>.md](./04.1-<slug>.md) | | — | draft |
| 2 | [04.2-<slug>.md](./04.2-<slug>.md) | | 1 | not started |

When split, this document is the index. Sections 3, 7 and 8 below move into the
sub-plans. Sections 4, 5, 6, 9 and 11 stay here, because they are shared.

## 3. File-by-file plan
Single-document mode only. When split, this lives in each sub-plan.

| Path | Action | Purpose |
|---|---|---|
| | created / modified / deleted | |

## 4. Interfaces and contracts
Type signatures and schemas for anything crossing a boundary. When split, this
section carries only what crosses a **slice** boundary. Contracts internal to
one slice belong in its sub-plan.

```ts
// module boundary, request and response shapes, events
```

## 5. Data and migrations
| Migration | Change | Reversible | Backfill | Slice |
|---|---|---|---|---|
| | | yes / no | | |

## 6. State management
| State | Lives in | Lifetime | Invalidated by |
|---|---|---|---|
| | | | |

## 7. Error handling
Single-document mode only. When split, this lives in each sub-plan.

| Failure | Detected by | User sees | System does |
|---|---|---|---|
| | | | |

## 8. Test plan
Name the cases, not the intent. Single-document mode only. When split, each
sub-plan carries its own cases and this section states only the end-to-end cases
that span slices.

| id | Level | Case | Covers |
|---|---|---|---|
| T-1 | unit / integration / e2e | | FR-1 |

## 9. Rollout
| Item | Decision |
|---|---|
| Feature flag | |
| Rollout stages | |
| Kill switch | |
| Metrics to watch | |
| Rollback plan | |

## 10. Task breakdown
Single-document mode only. When split, each sub-plan carries its own tasks and
this section is replaced by the slice order in section 2.

| # | Task | Size | Depends on | Acceptance check |
|---|---|---|---|---|
| T-1 | | S / M / L | | |

## 11. Definition of done
The feature is done when every sub-plan is done and:

- [ ] All tasks shipped or explicitly dropped in the dev log.
- [ ] Test plan cases pass, including the cross-slice cases in section 8.
- [ ] Implementation matches the approved design, or a change record explains why not.
- [ ] Observability in place for the metrics named in the PRD.
- [ ] `index.md` updated to `shipped`.

## Change log
| Date | Change | Why | Approved by | Sub-plans re-opened |
|---|---|---|---|---|
