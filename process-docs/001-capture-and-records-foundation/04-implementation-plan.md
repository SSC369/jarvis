---
doc: implementation-plan
feature: 001-capture-and-records-foundation
title: Capture and Records Foundation
stage: 4
status: approved
owner: user
created: 2026-09-13
updated: 2026-09-13
approved_on: 2026-09-13
supersedes: null
split: true
---

# Implementation Plan (LLD) — Capture and Records Foundation

> **Approved** by @user on 2026-09-13. Locked — changes require a change record (§7 of the rules).

Context: [PRD](./01-prd.md) · [Design](./02-design.md) · [Build plan](./03-build-plan.md)

The index is approved: the slicing, order and cross-slice contracts are locked.
Each sub-plan is still approved on its own before its own build starts, per §6
of the process rules.

## 1. Scope recap

Ships: commands-only capture into tasks, the records view for tasks, timezone
settings, the installed-app surfaces, and dark theme. Waits: every record type
past tasks, plain-language capture, cross-tab live sync, and any expiry on an
unanswered question — all deferred by the build plan or the PRD's own scope.

## 2. Split decision

| Trigger | Threshold | This feature |
|---|---|---|
| Tasks in the breakdown | more than 15 | ~28 across three slices |
| Files created or modified | more than 25 | ~55 |
| Independently shippable slices | more than one | 3 |
| Distinct boundaries touched | more than two | 4: data model, capture pipeline, records surface, installed-app/theme |
| Length of the drafted plan | more than 500 lines | Would be, undivided |

**Decision: split into 3 sub-plans.**

### Slices

| # | Sub-plan | What works when it lands | Depends on | Status |
|---|---|---|---|---|
| 1 | [04.1-capture-core.md](./04.1-capture-core.md) | Type a command in the Command Center and get a task, a question, or an honest refusal. Every capture outcome in the design's four flows | — | draft |
| 2 | [04.2-records-and-settings.md](./04.2-records-and-settings.md) | Open Records, see every task, filter, search, open one, edit or delete it. Change timezone in Settings | 1 | not started |
| 3 | [04.3-installed-app-and-theme.md](./04.3-installed-app-and-theme.md) | Install Slashit to a home screen, read records offline, get told when an update is ready. The app follows the device's light or dark setting everywhere | 2 | not started |

Slice 1 is capture without a way to browse what was captured, which is
demonstrable but incomplete on its own; slice 2 is what makes it a product.
Slice 3 is additive polish that touches no domain logic, which is why it comes
last and depends only on the UI slice 2 finishes.

## 3. File-by-file plan

Moved to the sub-plans. Slice order is section 2.

## 4. Interfaces and contracts

Only what crosses a **slice** boundary. Internal shapes live in each sub-plan.

### The `Task` GraphQL type and DTO, slice 1 to slice 2

Slice 1 creates it (`TaskCreated` carries one). Slice 2 is the first to query,
edit and delete it. The shape does not change between them.

```python
# app/domains/records/interfaces/dtos.py
@dataclass(frozen=True)
class TaskDTO:
    id: UUID
    user_id: UUID
    title: str
    due_at: datetime | None
    status: Literal["pending", "done"]
    is_overdue: bool          # computed in the repository query, build plan §3
    origin: Literal["command", "edit"]
    original_input: str | None
    created_at: datetime
    updated_at: datetime
```

```graphql
type Task {
  id: ID!
  title: String!
  dueAt: DateTime
  status: TaskStatus!
  isOverdue: Boolean!
  origin: RecordOrigin!
  originalInput: String
  createdAt: DateTime!
  updatedAt: DateTime!
}
```

### The port `capture` depends on, to reach `records`

Per backend repo-rules.md §6: the consumer (`capture`) declares the port in its
own words, the provider (`records`) publishes a service, the consumer's adapter
joins them. This crosses from slice 1 (which builds and calls it) toward slice
2 (which builds the rest of `records` behind the same published service).

```python
# app/domains/capture/interfaces/ports.py — capture's own vocabulary
class TaskCreationPort(Protocol):
    async def create_task(self, *, user_id: UUID, title: str, due_at: datetime | None,
                           origin: str, original_input: str) -> TaskDTO: ...

# app/domains/records/public.py — records' published surface
__all__ = ["RecordsService", "TaskDTO"]
```

Slice 1 builds only as much of `RecordsService` as creation needs. Slice 2
extends the same class; it does not create a second one.

### The `CaptureResult` union, fixed by the build plan §7

All ten members are slice 1's contract with the frontend. Slice 2 and 3 do not
add members to it.

## 5. Data and migrations

| Migration | Change | Reversible | Backfill | Slice |
|---|---|---|---|---|
| `0003_tasks` | Creates `tasks`, RLS enabled, policy scoped to `user_id`, grants to `authenticated` | yes | none, new table | 1 |
| `0004_pending_captures` | Creates `pending_captures`, RLS enabled, policy scoped to `user_id` | yes | none, new table | 1 |
| `0005_user_settings` | Creates `user_settings`, RLS enabled, policy scoped to `user_id` | yes | none, new table | 2 |

Numbering continues from epic 000's `0001_ai_usage` and `0002_ai_user_limit`,
the only migrations that exist yet.

## 6. State management

| State | Lives in | Lifetime | Invalidated by |
|---|---|---|---|
| Capture input, palette selection | React component state, `CaptureStore` (MobX) | One composition, cleared on submit | Submit, Escape |
| Tasks, pending captures | `RecordsStore`, `CaptureStore` (MobX) | Session, refetched on mount | A mutation response in the same tab, per build plan §4 |
| Settings (timezone) | `SettingsStore` (MobX) | Session, refetched on mount | `updateTimezone` response |
| Offline-cached records | Service worker cache (Cache API) | Until the next successful online fetch | A successful `records` query while online |
| Theme (light/dark) | Not stored. `tokens.css` defines both modes behind `@media (prefers-color-scheme: dark)` | n/a | The OS setting changing. Pure CSS: the browser re-evaluates the media query and swaps custom properties on its own, no JS listener needed |

## 7. Error handling

Moved to the sub-plans. Each slice's failures are its own; the nine-member
union in build plan §7 is the one shape all of slice 1's failures share, and is
covered there, not repeated per sub-plan.

## 8. Test plan

Only cases spanning slices.

| id | Level | Case | Covers |
|---|---|---|---|
| T-X.1 | e2e | A task created in slice 1's flow appears in slice 2's Records view without a reload | FR-13, build plan §4 |
| T-X.2 | e2e | Editing a task's title in Records (slice 2) and reopening it shows the edit, origin still reads "command" | FR-19, FR-22 |
| T-X.3 | integration | User A's task, pending capture and settings are all invisible to user B | FR-6, T7, one case per table |
| T-X.4 | e2e | With the network disabled, Records (slice 3's offline cache) still shows every task from the last online load | FR-40 |
| T-X.5 | e2e | The app opened with the OS in dark mode renders every slice 1 and slice 2 surface in dark tokens, no light-only element | proposed FR-42 baseline, product.md §10 |

## 9. Rollout

| Item | Decision |
|---|---|
| Feature flag | None. This is the first user-facing feature; there is nothing to flag against |
| Rollout stages | Slice 1 deploys and is usable stand-alone (capture with no way to browse it). Slice 2 follows, then slice 3 |
| Kill switch | Inherited: `GATEWAY_ENABLED=false` already refuses every capture at the gateway. No second switch needed here |
| Metrics to watch | Captures per day, refusals by `CaptureResult` member, share of captures answered via a pending question, per PRD §8 |
| Rollback plan | All three migrations are reversible. The application rolls back by redeploying the previous image; no data migration to undo |

## 10. Task breakdown

Moved to the sub-plans. Slice order is section 2.

## 11. Definition of done

The feature is done when every sub-plan is done and:

- [ ] All tasks shipped or explicitly dropped in the dev log, by id.
- [ ] The five cross-slice cases in section 8 pass.
- [ ] All three migrations applied, each table RLS-enabled with a policy.
- [ ] Implementation matches the approved design, or a change record explains why not.
- [ ] The metrics named in PRD §8 are instrumented.
- [ ] `index.md` updated to `shipped`.

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-13 | **Index approved.** §6's theme row corrected: no JS listener needed, a plain CSS media query does it | Slice 3's drafting caught the overstatement; user approved the index | user |
| 2026-09-13 | Created as the index, split into three slices | Build plan approved | pending |
