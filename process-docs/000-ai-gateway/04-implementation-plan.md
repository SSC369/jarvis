---
doc: implementation-plan
feature: 000-ai-gateway
title: AI Gateway and Usage
stage: 4
status: approved
owner: user
created: 2026-09-12
updated: 2026-09-12
approved_on: 2026-09-12
supersedes: null
split: true
---

# Implementation Plan (LLD) — AI Gateway and Usage

> **Approved** by @user on 2026-09-12. Locked — changes require a change record (§7).

Context: [PRD](./01-prd.md) · [Build plan](./03-build-plan.md)

No design stage. This epic has no screen.

**This document is the index.** It holds what the slices share. Each slice holds
its own files, contracts, errors, tests and tasks.

No code is written before this index and the relevant sub-plan are both approved.

## 1. Scope recap

This pass builds the backend from nothing to a working AI gateway: a runnable
FastAPI application, Supabase identity with Row Level Security proven by test,
and a gateway that calls Gemini under a per-user limit and records every call.

What waits: any caller. The gateway has no user of its own, and epic 001's first
capture is what proves it in production. The PRD records this as a deliberate
exception to the vertical-slice rule.

## 2. Split decision

| Trigger | Threshold | This feature |
|---|---|---|
| Tasks in the breakdown | more than 15 | ~20 |
| Files created or modified | more than 25 | **52** |
| Independently shippable slices | more than one | **3** |
| Distinct boundaries touched | more than two | **3**: HTTP and process, database and identity, external vendor |
| Length of the drafted plan | more than 500 lines | would exceed it |

**Decision: split into 3 sub-plans.** Every threshold is crossed.

### Slices

| # | Sub-plan | What works when it lands | Depends on | Status |
|---|---|---|---|---|
| 1 | [04.1-api-skeleton.md](./04.1-api-skeleton.md) | `GET /health` returns 200 from a running app that loaded its configuration from `.env`, and `/graphql` serves an empty schema | — | drafted |
| 2 | [04.2-identity-and-isolation.md](./04.2-identity-and-isolation.md) | An authenticated request resolves to a `user_id`, opens a transaction carrying that identity, and a test proves user A reading user B's row gets nothing | 1 | drafted |
| 3 | `04.3-the-gateway.md` | A call to `extract()` is allowance-checked, sent to Gemini under a timeout, recorded in `ai_usage`, and returns a typed union member | 2 | not started |

Each slice ends in something a person can run. Slice 1 is thin on purpose: it
exists so that slice 2 has somewhere to land and so the deploy path is proven
before there is anything worth deploying.

**Slice 3 is proven by an integration test against the real provider, not by a
screen.** That is the consequence of this being a platform epic, and it is the
honest statement of it.

## 3. File-by-file plan

Moved to the sub-plans. See section 2.

## 4. Interfaces and contracts

Only what crosses a slice boundary. Contracts inside one slice live in its
sub-plan.

### Request context, slice 2 to slice 3

```python
@dataclass
class Context(BaseContext):       # strawberry.fastapi.BaseContext
    user_id: UUID | None          # None on an unauthenticated request
    session: AsyncSession         # already carries SET LOCAL identity
    request_id: str
```

> **Changed 2026-09-12, during slice 2.** Originally `@dataclass(frozen=True)`
> and inheriting nothing. Strawberry accepts only `BaseContext` or a plain
> dictionary as a resolver context, and it assigns `request` and `response` onto
> that object at runtime, which a frozen dataclass rejects. Immutability was
> never the mechanism behind FR-6: the guarantee is that `user_id` is set only
> in `build_context`, from a verified token, and no code path takes it from
> caller input. Slice 3 is unaffected; it reads `user_id` and does not write it.

Slice 2 builds it. Slice 3 consumes it and never reads `user_id` from anywhere
else, which is the mechanism behind FR-6.

### Domain error base, slice 2 to slice 3

```python
class DomainError(Exception):
    gql_type: ClassVar[type]
    def __init__(self, message: str) -> None: ...
    def to_gql(self): ...           # builds gql_type from its own fields
```

Slice 2 defines it and the `@map_errors` decorator. Slice 3 subclasses it.
Matches [the backend ruleset](../../backend/rules/repo-rules.md) section 8.

### The gateway's published surface, slice 3 outward

```python
# app/domains/gateway/public.py
__all__ = ["ExtractionService", "ExtractionResult", "ExtractionRequest"]
```

The only names another domain may import. Epic 001 will define its own port and
adapter against this, per [the backend ruleset](../../backend/rules/repo-rules.md)
section 6. **Changing this list is a change record here**, because it is the
contract every later epic depends on.

### The extraction result union, slice 3 outward

```python
ExtractionResult = Annotated[
    Union[
        Extraction,              # success
        UserLimitReached,        # FR-9
        SharedQuotaExhausted,    # FR-18
        ProviderUnavailable,     # FR-18
        ProviderTimeout,         # FR-19
        MalformedResult,         # FR-18
    ],
    strawberry.union("ExtractionResult"),
]
```

Six members, one per FR-18 outcome. A caller switches on all six. Adding a
seventh is a change record here, not a quiet addition in slice 3.

## 5. Data and migrations

| Migration | Change | Reversible | Backfill | Slice |
|---|---|---|---|---|
| `0001_ai_usage` | Create `ai_usage`. Enable RLS, add policy on `user_id`. Index `(user_id, created_at)` | yes | none | 2 |
| `0002_ai_user_limit` | Create `ai_user_limit`. Enable RLS, add policy on `user_id`. Seed nothing | yes | none | 2 |

**Both migrations enable RLS and add the policy in the same file that creates the
table.** Rule T2. A migration that creates a table without a policy fails review,
and slice 2 carries a test that asserts `relrowsecurity` on every table in the
schema.

Migrations live in slice 2 rather than slice 3 because slice 2's boundary test
needs tables to prove isolation against.

## 6. State management

This is a backend. There is no client state. What exists is request-scoped and
dies with the request.

| State | Lives in | Lifetime | Invalidated by |
|---|---|---|---|
| `user_id`, verified | `Context` | One request | End of request |
| Database session and its `SET LOCAL` identity | `Context.session` | One transaction | Commit or rollback. `SET LOCAL` unsets itself |
| Supabase JWKS public keys | Module cache in `core/auth.py` | Process, with a TTL | TTL expiry, or a verification failure forcing a refetch |
| A user's remaining allowance | Nowhere. Computed per call | One call | Not cached, by decision |

Allowance is not cached. At this volume an indexed count is free, and a cache
would be a second source of truth for a number that gates spending.

## 7. Error handling

Moved to the sub-plans. The shared pieces are the `DomainError` base and
`@map_errors` in section 4.

## 8. Test plan

Only cases that span slices. Each sub-plan carries its own.

| id | Level | Case | Covers |
|---|---|---|---|
| T-X.1 | integration | An unauthenticated request to a gateway-backed field never reaches the provider, and records no usage row | FR-7 |
| T-X.2 | integration | User A calls `extract()`, user B queries `ai_usage`, and sees none of A's rows | FR-6, T7 |
| T-X.3 | integration | Count of provider calls equals count of usage rows across a run of mixed successes and failures | NFR-3, FR-13 |
| T-X.4 | integration | Usage rows written before a forced process restart are present after it | NFR-6 |
| T-X.5 | integration | No log line emitted across a full successful call contains the credential | FR-3, NFR-1 |

T-X.3 and T-X.5 are the two that catch the failures nobody notices: attribution
silently skipped on one path, and the key reaching a log through an exception
string.

## 9. Rollout

| Item | Decision |
|---|---|
| Feature flag | None. There is no user-facing behaviour to flag, and nothing calls the gateway until epic 001 |
| Rollout stages | Slice 1 deploys to the managed host and proves the deploy path. Slices 2 and 3 follow to the same environment |
| Kill switch | `GATEWAY_ENABLED=false` in the environment. `ExtractionService` returns `ProviderUnavailable` without calling out. One variable, no deploy |
| Metrics to watch | Usage rows per day against the 1,000 project ceiling. Refusals by outcome. Provider call count against usage row count, for NFR-3 |
| Rollback plan | Both migrations are reversible. The application rolls back by redeploying the previous image. No data migration to undo |

The provider-side spend cap in the Google console is set **before slice 3 first
calls the provider**, not after. It is the only cost defence that works while
nobody is watching.

## 10. Task breakdown

Moved to the sub-plans. Slice order is section 2.

## 11. Definition of done

The feature is done when every sub-plan is done and:

- [ ] All tasks shipped or explicitly dropped in the dev log, by id.
- [ ] The five cross-slice cases in section 8 pass.
- [ ] Both migrations applied, and every table holding user data has RLS with a policy.
- [ ] Secret scanning runs in CI and passes, per NFR-1.
- [ ] A provider-side spend cap and billing alert exist in the Google console.
- [ ] `index.md` updated to `shipped`.

There is no design to match. This epic had no stage 2.

## Change log

| Date | Change | Why | Approved by | Sub-plans re-opened |
|---|---|---|---|---|
| 2026-09-12 | Created as an index, split into 3 slices | All five split thresholds crossed, 52 files against a threshold of 25 | user | — |
