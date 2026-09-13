---
doc: build-plan
feature: 001-capture-and-records-foundation
title: Capture and Records Foundation
stage: 3
status: draft
owner: user
created: 2026-09-13
updated: 2026-09-13
approved_on: null
supersedes: null
---

# Build Plan (HLD) — Capture and Records Foundation

Context: [PRD](./01-prd.md) · [Design](./02-design.md) · [Tech stack](../tech-stack.md)

This document locks the high-level architecture. It also asks. Section 10 must
be answered by the user before approval.

> 310 lines against a 250 budget. Two new backend domains, a persisted pending
> question, and the PWA and dark-theme surfaces the user asked to include now
> account for the excess. Cutting to budget would mean dropping a table, not
> prose.

## 1. Architecture summary

Two new backend domains: `capture`, which turns one line of text into a
command and orchestrates the AI gateway, and `records`, which owns tasks and
every future record type. Capture depends on `records` and on epic 000's
`gateway` through ports it declares itself, per rule §6 of the backend
ruleset. Three tables: `tasks`, `pending_captures`, `user_settings`, each with
Row Level Security. The frontend is React on Vite, deployed to Vercel, talking
to one GraphQL endpoint through Apollo as transport with MobX as the source of
truth, styled from the tokens `02-design.md` §6 fixed. A service worker adds
install, offline reads and an update banner; dark theme is CSS tokens only,
switched by the device's setting.

## 2. Component map

| Component | Responsibility | Talks to | New or existing |
|---|---|---|---|
| `app/domains/capture/` | Parse a command, call the gateway, create or update a record, hold a pending question until answered | `records` (via a port), `gateway` (via a port), GraphQL | New |
| `app/domains/records/` | Own tasks and future record types: create, edit, complete, delete, list, detail | Database only | New |
| `app/domains/identity/` (extended) | Timezone, detected and changeable | Database only | Existing shell, first real use |
| `app/domains/gateway/` | Structured extraction | Consumed by `capture`, unchanged | Existing (epic 000) |
| `frontend/src/features/capture/` | Command Center: input, palette, transcript, pending questions | GraphQL mutations, `CaptureStore` | New |
| `frontend/src/features/records/` | Records list, filter, search, detail, edit, delete | GraphQL queries and mutations, `RecordsStore` | New |
| `frontend/src/features/settings/` | Timezone, theme (read-only, follows device) | GraphQL, `SettingsStore` | New |
| Service worker | Install prompt, cached read-only shell, offline banner, update banner | Browser cache API only, no network | New |

```
Command Center (React) --mutation--> capture domain --port--> gateway domain (epic 000)
                                          |--port--> records domain --SQL--> tasks
                                          |--SQL--> pending_captures
Records view (React)   --query/mutation-> records domain --SQL--> tasks
Settings (React)        --query/mutation-> identity domain --SQL--> user_settings
```

## 3. Data model

| Entity | Key fields | Owns | Lifecycle | Tenancy scope |
|---|---|---|---|---|
| `tasks` | `id`, `user_id`, `title`, `due_at` (nullable), `status` (pending, done), `origin` (command, edit), `original_input`, `created_at`, `updated_at` | `records` | Created on capture or manual add, edited or deleted by the user. Never hard-deleted by the system | RLS on `user_id` |
| `pending_captures` | `id`, `user_id`, `command_name`, `known_fields` (jsonb), `missing_field`, `question_text`, `original_input`, `asked_at` | `capture` | Created when a required field is missing, FR-8. Removed when answered (becomes a task) or discarded, FR-37. No expiry: the PRD does not set one, see §10 Q6 | RLS on `user_id` |
| `user_settings` | `user_id` (PK), `timezone` | `identity` | One row per user, created on first use with a browser-detected value, updated by the user | RLS on `user_id` |

`overdue` is not a column. FR-43 is `due_at < now() AND status = 'pending'`,
computed in the repository's query, per the storage-purity rule that a
repository filters and converts but does not decide: the decision here is a
plain time comparison, not a business rule with alternatives, so it is
computed in SQL rather than carried as a stored flag that could drift from the
truth.

Migrations required: three, each creating its table with RLS enabled and a
policy in the same migration, per rule T2. No column additions to an existing
table.

## 4. API surface

| Endpoint or action | Method | Auth | Input | Output | Serves |
|---|---|---|---|---|---|
| `submitCapture` | mutation | `IsAuthenticated` | raw text | `CaptureResult` union, ten members (§7) | FR-1 to FR-9, FR-12, FR-35 |
| `answerPendingCapture` | mutation | `IsAuthenticated` | pending capture id, answer text | `CaptureResult` union | FR-37, FR-38 |
| `discardPendingCapture` | mutation | `IsAuthenticated` | pending capture id | `Boolean` | FR-37 |
| `records` | query | `IsAuthenticated` | type filter, text search | `[RecordSummary]` | FR-13 to FR-17 |
| `record` | query | `IsAuthenticated` | record id | `RecordDetail` or not found | FR-18, FR-22 |
| `updateTask` | mutation | `IsAuthenticated` | task id, field edits | `Task` or typed error | FR-19 |
| `completeTask` | mutation | `IsAuthenticated` | task id | `Task` | FR-24 |
| `deleteTask` | mutation | `IsAuthenticated` | task id(s) | `Boolean` | FR-20, FR-21 |
| `tasks` | query | `IsAuthenticated` | none | `[Task]`, soonest due first | FR-25 |
| `settings` | query | `IsAuthenticated` | none | `Settings` | FR-27 |
| `updateTimezone` | mutation | `IsAuthenticated` | IANA timezone string | `Settings` | FR-28 |

**The command list is a frontend constant, not a query.** Four commands, fixed
for this epic. A query earns its place when discovery has to reflect something
the server knows that the client does not, which is not true yet.

**No subscription.** `tasks` and `records` re-query after a mutation the same
tab made; MobX writes the result into the store the moment the mutation
resolves, which is what FR-13's "without reloading or waiting" asks for
inside one tab. Multi-tab and multi-device live sync would need a
subscription, which needs a backplane the stack has not chosen yet, T-Q3. See
§10 Q3.

## 5. Model and vendor choices

| Use | Choice | Why | Fallback | Est. cost per call | Latency budget |
|---|---|---|---|---|---|
| Structured extraction from a capture | Epic 000's `ExtractInteractor`, unchanged | Already built, tested and boundary-tested. Building a second path would duplicate FR-8, FR-11 to FR-15 and FR-19 to FR-20 of the gateway PRD | Typed refusal, per the gateway's own six-outcome union | `estimate` 0.0001 USD, `tech-stack.md` §5 | 8 s, inherited from `04.3-the-gateway.md` §1 |
| Service worker tooling | `vite-plugin-pwa` | Generates the manifest and worker from one Vite config entry, and is the standard choice for a Vite app; hand-writing a worker for install, cache and update banner is a well-known amount of boilerplate this avoids | None; a hand-written worker if the plugin cannot express a need | 0 USD, dev dependency | n/a |

No new model or vendor decision. This epic is the gateway's first caller.

## 6. Cross-cutting concerns

| Concern | Decision |
|---|---|
| Authentication | Supabase JWT, verified by the existing `IsAuthenticated` permission class from epic 000 slice 2. No new auth code |
| Authorisation | `user_id` comes from the request context, never from input (mirrors the gateway's own FR-6). Every interactor scopes its query by it before RLS is ever reached |
| Tenant isolation | RLS with a policy on all three new tables, in the migration that creates each, per T2. A boundary test per table, per T7: user A requests user B's task or pending capture and gets nothing |
| Rate limits and quotas | Inherited entirely from the gateway. `capture` adds no allowance logic of its own; a refused capture is the gateway's `UserLimitReached` or `SharedQuotaExhausted`, mapped through |
| Input length | Epic 000's build plan Q11 assigned this epic the input-length cap. **Decided here: 500 characters**, refused client-side before the mutation fires, with a server-side check at the same limit so a client bypass still fails cleanly. `estimate`: 500 characters covers every drawn example in `02-design.md` with headroom, and stays well under the ~650-token figure the gateway build plan uses for TPM math |
| Cost controls | None new. The gateway owns spend; this epic cannot cause a call outside it |
| Caching | Apollo as transport only, `network-only`, per `tech-stack.md` §3. MobX stores are the one source of truth for tasks, pending captures and settings |
| Observability | Structlog, existing pattern. `original_input` is application data on the record itself, shown in `RecordDetail` per FR-18 and design §4 — it is not a usage or analytics table, so rule T6 does not forbid storing it there, only in `ai_usage`-shaped stores |
| Failure and retry | The gateway's five failure outcomes map to FR-35's refusal card, one union member each. No retry at this layer; the gateway already retries a connection failure once |
| Data retention and privacy | Tasks and pending captures persist until the user deletes or answers them. No auto-expiry designed for a stale pending capture, see §10 Q6 |
| PWA offline | Read-only. The service worker caches the last-fetched records list and detail views; capture is refused in the input itself when `navigator.onLine` is false, per FR-40 and design §5a. Nothing is queued |

## 7. The ten-member `CaptureResult` union

| Member | Meaning | Source |
|---|---|---|
| `TaskCreated` | A record now exists, every field shown | FR-6, FR-7 |
| `PendingQuestionCreated` | One field missing, one question asked | FR-8 |
| `NonCommandGuidance` | Input had no command, text preserved | FR-9 |
| `UnrecognisedCommand` | `/` name matches nothing, closest matches offered | FR-12, should-priority |
| `UserLimitReached` | The gateway's per-user cap, mapped straight through | Gateway FR-9 |
| `ProviderUnavailable` | Kill switch or a 5xx after retry | Gateway union |
| `ProviderTimeout` | Over the 8 s budget | Gateway union |
| `SharedQuotaExhausted` | The project's daily ceiling | Gateway union |
| `MalformedResult` | The model's answer failed the schema | Gateway union |

**Capture defines its own GraphQL types for the five gateway-sourced members.**
Rule §6.2 of the backend ruleset forbids a domain's `graphql/` types crossing a
boundary; `capture`'s `graphql/errors.py` mirrors the shape of the gateway's
domain errors (which do cross, as exceptions) and is one small file, not a
second hierarchy, since the mapping is a one-line constructor call per member.

## 8. Alternatives considered

| Decision | Chosen | Alternatives | Why they lost | Reversibility |
|---|---|---|---|---|
| Domain split | `capture` and `records` as two domains | One combined domain | `records` grows a new record type almost every future epic; `capture` orchestrates across domains and belongs to the pattern in repo-rules.md §6, not inside the thing it calls | costly once record types multiply |
| Pending question storage | A `pending_captures` table | In-memory, keyed by session | FR-37 requires answerable "at any later point," which an in-memory store loses on a restart or a second instance | cheap now, costly later |
| Live records update | Optimistic MobX write on mutation resolve | A GraphQL subscription per change | T-Q3's subscription backplane is unresolved for more than one instance; a subscription today would be single-instance-only and need rework the moment a second instance exists | cheap to add later, since the transport is already chosen |
| Command list | A frontend constant | A `commands` GraphQL query | Four fixed commands; a query is one more round trip for data that never changes this epic | cheap to add later |
| `overdue` | Computed in the query | A stored, denormalised column | A stored flag needs a background job to keep true past midnight; a computed comparison cannot drift | cheap either way |

## 9. Architecture decisions to lock

| # | Decision | Status | Graduates to tech-stack.md or product.md |
|---|---|---|---|
| AD-1 | `capture` and `records` are separate domains; `capture` depends on `records` and on `gateway`, never the reverse | proposed | no |
| AD-2 | Pending questions are a table, not a session or cache entry | proposed | no |
| AD-3 | No subscription in V1; live updates are an optimistic client-side write after each mutation | proposed | no, revisit at T-Q3 |
| AD-4 | Capture input is capped at 500 characters, checked client and server | proposed | no |
| AD-5 | `overdue` is computed, never stored | proposed | no |
| AD-6 | Frontend hosting is Vercel | proposed | **yes**, answers `tech-stack.md` T-Q5 |
| AD-7 | Service worker built with `vite-plugin-pwa` | proposed | no |

## 10. Questions for the user

| # | Question | Options | Recommendation | Answer |
|---|---|---|---|---|
| Q1 | Does a stale pending capture ever expire? | Never / after N days, auto-discarded | **Never, in V1.** FR-37 says answerable "whenever you like"; adding a silent expiry contradicts that unless the PRD is changed first | |
| Q2 | 500-character input cap: is that generous enough, or should it be higher for a task with a long description? | 500 / 1,000 / no cap | **500.** Every drawn example is well under it, and a cap protects TPM headroom cheaply | |
| Q3 | Confirm: no GraphQL subscription this epic, live update is same-tab-only via the mutation response | Confirm / want cross-tab sync now | **Confirm.** Cross-tab sync needs T-Q3 answered first, which is a platform question, not this epic's | |
| Q4 | `UnrecognisedCommand` (FR-12) is a `should`, not a `must`. Build it in this pass, or defer? | Build now / defer | **Build now.** It is one union member and a Levenshtein-distance match against four names, cheap next to the other nine members already being built | |
| Q5 | The service worker caches records for offline reading. How much: the last N records, or everything the user has? | Last 50 / everything | **Everything.** A personal task list stays small for a long time; capping it adds complexity FR-40 does not ask for | |

## 11. Risks

| Risk | Impact | Mitigation | Trigger to revisit |
|---|---|---|---|
| The optimistic same-tab update (AD-3) reads stale in a second tab until that tab's own mutation or a manual reload | medium | Named plainly in the design as a V1 limit; not drawn as a bug | A user reports a second tab or device disagreeing |
| A pending capture with no expiry accumulates forever for a user who never answers or discards | low | Cheap to store, one row each; revisit only if it becomes a real volume | Hundreds of unanswered rows per user |
| `vite-plugin-pwa`'s cache-everything offline strategy (Q5) grows the cached payload as records grow | low | Personal-capture volume stays small for a long time, per the gateway build plan's own capacity reasoning | A user with thousands of records reports slow offline load |
| The 500-character cap (AD-4) is enforced in two places, client and server, and could drift out of sync | low | One shared constant, imported by both; a build-time check is a stage 4 task | The two disagree in a bug report |

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-13 | Created | Design approved, stage 3 opened | pending |
