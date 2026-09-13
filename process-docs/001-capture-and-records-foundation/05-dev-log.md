---
doc: dev-log
feature: 001-capture-and-records-foundation
title: Capture and Records Foundation
stage: 5
status: draft
owner: user
created: 2026-09-13
updated: 2026-09-13
approved_on: null
supersedes: null
---

# Dev Log — Capture and Records Foundation

Context: [Index](./04-implementation-plan.md) · [04.1](./04.1-capture-core.md)

What actually happened. Deviations from the approved plan are recorded the day
they happen, per rule 5 of the root ruleset.

## Slice 1 — Capture Core

Backend and frontend both built and verified 2026-09-13, against the real
database, the real gateway, and a real signed-in Supabase user, in a browser.

### Tasks

| # | Task | Status | Note |
|---|---|---|---|
| T-1.a | `records`: `Task` model, `TaskDTO`/`Task` type, migration `0003_tasks` | **done** | Applied and reversed against the live database |
| T-1.b | `records`: `TaskRepository.create_task`, `RecordsService`, `public.py` | **done** | Extended beyond plan: `list_open_tasks_for_user`, see deviations |
| T-1.c | `capture`: `PendingCapture` model, migration `0004_pending_captures` | **done** | Applied and reversed against the live database |
| T-1.d | `capture`: `constants.py`, `interfaces/{dtos,repositories,ports}.py` | **done** | |
| T-1.e | `capture`: `SqlPendingCaptureRepository` | **done** | Against the request's own session, not a session factory — see deviations |
| T-1.f | `capture`: both adapters | **done** | Port renamed `TaskCreationPort` → `TaskPort`, extraction port generalised — see deviations |
| T-1.g | `capture`: `SubmitCaptureInteractor`, all nine outcomes | **done** | Returns DTOs, not GraphQL types — see deviations |
| T-1.h | `capture`: `AnswerPendingCaptureInteractor`, `DiscardPendingCaptureInteractor` | **done** | Answering a due-date question resolves the answer through the gateway too — see deviations |
| T-1.i | `capture`: `graphql/types.py`, `graphql/mutations.py`, `deps.py`, `schema.py` wiring | **done** | First mutation this project has; added the root `Mutation` type |
| T-1.j | `capture`: the live test | **done** | Passed after a schema fix, see incidents |
| T-1.k | Frontend: `tokens.css`, both modes | **done** | Values sourced from the canvas's `DarkTokens.dc.html`; an unplanned skeleton step came first, see deviations |
| T-1.l | Frontend: three operation folders | **done** | Apollo Client 4 needed a type-override file the plan did not anticipate, see deviations |
| T-1.m | Frontend: `CaptureStore` | **done** | |
| T-1.n | Frontend: `CommandCenterController` and components | **done** | Manual pass in a real browser reproduces every flow the canvas prototype proved: add-task with a date, add-task without one (pending question, answered), `/tasks`, non-command guidance, unrecognised command |

### Verification

| Check | Result |
|---|---|
| `pytest tests/unit` | **53 passed** |
| `pytest tests/integration -m "not live"` | **30 passed**, including the standing RLS guard (`test_every_user_table_is_locked_down`) covering the two new tables |
| `pytest tests/integration -m live` | **1 passed**, real `/add-task` call through the full stack: schema → auth → resolver → interactor → adapter → gateway → database |
| `ruff check .` / `ruff format --check .` | Clean |
| `mypy app` (strict) | No issues in 67 source files |
| `alembic upgrade head` then `downgrade 0002_ai_user_limit` then `upgrade head` | Both new migrations apply and reverse cleanly against the live database |
| `tsc -b --noEmit` | Clean |
| `oxlint` | Clean (generated files excluded, see D-21) |
| `npm run build` | Clean production build |
| Manual browser pass, real backend + real Gemini + a real Supabase session | `/add-task` with a date, `/add-task` without one → pending question → answered → task created, `/tasks` listing two real rows, a non-command with "Use with /add-task", an unrecognised command |

### Deviations

| # | Deviation | Why | Consequence |
|---|---|---|---|
| D-13 | The `CaptureResult` union is **nine** members, not the ten the build plan's heading said, and capture imports the gateway's five outcome types directly instead of mirroring them into its own `graphql/errors.py` | Reading the actual epic 000 code while building this slice: the gateway has no `graphql/` folder, so its types already cross legitimately via `public.py`. The build plan's reasoning was wrong, corrected there with a change record the same day | `03-build-plan.md` §7 corrected. No behaviour change |
| D-14 | `SubmitCaptureInteractor` and `AnswerPendingCaptureInteractor` return plain DTOs (`TaskDTO`, `list[TaskDTO]`, `PendingCaptureDTO`, `NonCommandGuidanceDTO`, `UnrecognisedCommandDTO`, or a gateway type), never a GraphQL type. The resolver in `graphql/mutations.py` converts | The sub-plan's own contract had the interactor importing from `capture/graphql/types.py`, which repo-rules.md section 7.3 forbids: an interactor imports nothing from `graphql/`. Caught before it shipped, not after | Matches the documented layer contract exactly. No sub-plan update needed since this is what "the resolver converts DTO to GraphQL type" already meant |
| D-15 | `SqlTaskRepository` and `SqlPendingCaptureRepository` take the request's own `AsyncSession` directly, not a `session_factory` | The sub-plan's contract copied the gateway's `SqlUsageRepository` shape, which exists specifically for AD-8 (a usage row must survive the caller's later work rolling back). Neither table here has that requirement, so the plain per-request session repo-rules.md section 7.4 documents is the correct, simpler choice | `Context` gained a `session_factory` field (see D-16), used only by the one collaborator that still needs an independent transaction: the gateway |
| D-16 | `Context` (`app/core/context.py`) gained a `session_factory: async_sessionmaker[AsyncSession]` field | Building the gateway from inside `capture`'s composition needs its own transaction (D-15's reasoning, in reverse); `Context` only carried a single shared `session` | Additive, no existing field changed. Every other domain keeps using `context.session` |
| D-17 | `TaskCreationPort` renamed `TaskPort` and gained `list_open_tasks`; `RecordsService`/`TaskRepository` gained `list_open_tasks(_for_user)` a slice early | The sub-plan scoped `TaskRepository` to `create_task` only, but its own test plan (T-1.9, `/tasks` lists open tasks) needs a read path that did not exist yet, and its own interactor contract listed a `task_repository: TaskRepository` parameter directly on `SubmitCaptureInteractor` — crossing into `records` without a port, which section 6 forbids. Resolved by extending the existing port/service rather than crossing directly | Slice 2 extends the same `TaskRepository` Protocol with detail, edit, complete and delete; it does not need to add listing, that already exists |
| D-18 | `AnswerPendingCaptureInteractor` takes an `ExtractionPort`, not just a `TaskPort`, and resolves a due-date answer ("Friday", "tomorrow") through the gateway with a second, minimal schema (`DUE_AT_ONLY_SCHEMA`) | Not designed in the sub-plan. A free-text date answer needs real resolution somewhere; the alternatives were a second date-parsing dependency (against T4's provider-boundary rule) or accepting ISO-only answers (breaking the demonstrated canvas prototype UX). Reusing the gateway, already the one place date resolution happens, was the smallest correct option | `ExtractionPort.extract` is generic (`schema`, `instruction` as parameters) rather than hardwired to the task schema, so both callers pass their own. One more gateway call, and one more possible `AnswerCouldNotBeUnderstoodError`, not in the original error table |
| D-19 | Backend gained a local-only CORS middleware in `app/main.py` (`allow_origins` limited to the Vite dev server, gated on `settings.environment == "local"`) | The frontend did not exist before this slice, so nothing in the backend previously needed to answer a browser request from a different origin. No production origin is configured; that is a deploy-time decision, not made here | Composition-root change only, no domain code touched. Needs revisiting once the frontend has a real deployed origin |
| D-20 | Frontend `package.json` sets `noUnusedLocals`/`noUnusedParameters` to `false` in `tsconfig.app.json`; `.oxlintrc.json` excludes `**/*.generated.ts` | `@graphql-codegen`'s `near-operation-file` preset always emits an `import * as Types` in every operation file, used or not, which `noUnusedLocals` flagged as an error in a file repo-rules.md forbids hand-editing. Generated output cannot satisfy a rule it doesn't control | Applies repo-wide, not just to generated files, since a single tsconfig covers `src/`. Hand-written dead code is now only caught by `oxlint`'s own unused-vars rule, which still runs on hand-written files |
| D-21 | `src/api/lib/apolloTypeOverrides.d.ts` pins Apollo Client 4.2's hook signature style to `"classic"`, alongside declaring `errorPolicy: "all"` in `DeclareDefaultOptions` | Apollo Client 4.2 requires a `DeclareDefaultOptions` module augmentation before a non-default `errorPolicy` in `defaultOptions` type-checks at all (repo-rules.md §4's mandated default), but declaring one also switches every hook to "modern" signatures, which reject the manually-specified `<Data, Variables>` generics `@graphql-codegen/typescript-react-apollo` v5 emits (it predates modern signatures and does not emit `TypedDocumentNode`). The Apollo changelog names this exact classic-pin combination for this migration state | A future `typescript-react-apollo` release that emits `TypedDocumentNode` should drop this file and the manual generics in every `useOperation.ts` |
| D-22 | `useSubmitCapture`/`useAnswerPendingCapture` gained an `onRequestFailed` callback, invoked both from the mutation's `onError` and when `onCompleted` fires with a null result field | Not in the sub-plan's hook contract. Found in manual testing: a top-level GraphQL error (hit once locally on an auth misconfiguration, see incidents) left its turn stuck showing "Reading your command" forever, since `errorPolicy: "all"` calls `onCompleted` with a null field rather than rejecting. `CommandCenterController` resolves the turn to the same `refused` status a `UserLimitReached`-style outcome uses | One more optional callback per submit-shaped hook; `responseHandler.ts`'s union switch is unchanged |
| D-23 | `CommandCenterController` scrolls its turn stream to the latest turn on every new turn (a `useRef` + `useEffect` keyed on `turns.length`) | The canvas prototype did this in `componentDidUpdate`; the first port of it to React was missed and only surfaced when a manual multi-turn browser pass left new turns below the fold | Matches the approved prototype's behaviour; no contract change |

### Incidents and defects

| # | What broke | Cause | Fix |
|---|---|---|---|
| I-1 | The live test (`T-1.13`) failed twice with `ProviderTimeout`, consistently around 10.3–10.7s against the 8s budget (NFR-2), even though gateway's own live test reliably completes in ~5.4s with a similar schema | A verbose `description` on the `due_at` JSON Schema property (two sentences) measurably slowed generation. Isolated by direct timing: gateway's exact schema/instruction ran in 5.3–5.5s twice; swapping in capture's schema alone (same field name, long description) reproduced the ~10.7s timeout; shortening the description to gateway's terse style brought it to 6.2s | `TASK_EXTRACTION_SCHEMA` and `DUE_AT_ONLY_SCHEMA` rewritten with terse, one-line descriptions matching gateway's own style; the adapter's appended reference-moment sentence shortened from two sentences to `"Today is {now_iso}."`. The live test then passed at 7.96–8.48s |
| I-2 | Even after the fix, one full-suite run (this test running back-to-back with gateway's own live test) still timed out; three isolated reruns passed at 7.96–8.48s | Real latency sits close enough to the 8s budget that ordinary variance can cross it. Not a code defect: the same request sometimes takes 6s, sometimes just over 8s | Not fixed further here — diminishing returns on shaving more schema text, and NFR-2's own docstring in `gateway/constants.py` already calls 8s an `estimate` to be revised against real p95 "once epic 001 calls this." That is now happening. **Flagged, not resolved**: revisit `PROVIDER_TIMEOUT_SECONDS` against a real measurement sample once more calls have been made, likely in slice 2 or 3. This is epic 000's constant; changing it needs a change record there, not here |
| I-3 | The first manual browser submission failed: the backend rejected the request as `Not authenticated`, logging `PyJWKClientConnectionError` while fetching Supabase's JWKS endpoint | The backend's Python venv (a python.org install under `/Library/Frameworks/Python.framework`) has no working default CA bundle; `ssl.get_default_verify_paths()` points at a `cert.pem` that install never wrote. `httpx` (used for the Gemini calls) ships its own certifi-backed default context and was unaffected; `PyJWKClient` uses stdlib `urllib`, which was not | Local machine fix, not a code change: the backend process needs `SSL_CERT_FILE` set to `certifi.where()`. This is a workstation setup gap, not tracked as a deviation because nothing in the repository changed; worth a line in a local setup doc if one gets written |
| I-4 | The stuck-loading turn from I-3's failed request never resolved, even after the fix, because it belonged to a promise whose callbacks were already bound before the code changed | Expected once traced: an in-flight mutation keeps the closures it started with. Not a bug in the final code, confirmed by every later submission resolving correctly | No fix needed; the page was reloaded, which cleared the (intentionally unpersisted) turn history |

### Not done, and why

No feature this epic has designed is skipped, but manual verification needed a
sign-in path that does not exist as product UI yet: no epic has designed a
sign-up or sign-in screen. `src/api/lib/supabaseClient.ts` exposes the
Supabase client on `window.__supabaseClient` in dev builds only
(`import.meta.env.DEV`), so a session can be established from the browser
console for manual testing. A real test account
(`sai9821c+slashitdev@gmail.com`) exists in the project's Supabase instance for
this purpose. This is a dev-only affordance, not a feature; a real sign-in
screen is an open gap this epic inherits rather than introduces, and belongs to
whichever epic is judged to own identity UI.

## Slice 2 — Records and Settings

Backend and frontend both built and verified 2026-09-13, against the real
database and a real browser session.

### Tasks

| # | Task | Status | Note |
|---|---|---|---|
| T-2.1 | `TaskRepository` Protocol extended; `task_repository.py` implements list/get/update/set_status/delete | **done** | |
| T-2.2 | `list_tasks.py`, `get_record_detail.py` interactors | **done** | |
| T-2.3 | `update_task.py`, `delete_tasks.py` interactors | **done** | `completeTask` reuses `UpdateTaskInteractor` rather than a fifth interactor — not itemised as its own row, matches the sub-plan's own interactor list |
| T-2.4 | `records/graphql/` — types, inputs, errors, queries, mutations | **done** | `Task` itself not redeclared here, see deviations |
| T-2.5 | `identity` domain, backend, in full | **done** | |
| T-2.6 | `deps.py` wiring, `schema.py` registration for both domains | **done** | |
| T-2.7 | Boundary tests, `tests/integration/` | **done** | Built as GraphQL-level tests (real JWTs), not raw-SQL boundary tests, since the union outcome (`RecordNotFound`) is what rule T7 needs proven here, not just row invisibility |
| T-2.8 | Frontend operation folders, all eight, plus `TaskFragment` | **done** | Query folders use `useLazyQuery` + a `useEffect` in the controller, not `onCompleted` — see deviations |
| T-2.9 | `RecordsStore`, `SettingsStore`, `RootStore` wiring | **done** | |
| T-2.10 | `RecordsController`, `RecordTable`, `EmptyRecords` | **done** | |
| T-2.11 | `RecordDetailController`, `RecordEditForm`, `DeleteConfirmModal` | **done** | Status is changed through the same "Save changes" as the title, per `RecordEdit.dc.html` — see deviations |
| T-2.12 | `SettingsController`, `detectTimezone.ts` | **done** | |
| T-2.13 | Response-handler tests for all four mutations | **done** | Vitest and React Testing Library newly installed for this slice; no frontend test infrastructure existed before it |

### Verification

| Check | Result |
|---|---|
| `pytest tests/unit` | **70 passed** (53 from slice 1 + 17 new) |
| `pytest tests/integration -m "not live"` | **46 passed** (30 from slice 1 + 16 new), including the standing RLS guard now covering `user_settings` automatically |
| `ruff check .` / `ruff format --check .` | Clean |
| `mypy app` (strict) | No issues in 99 source files |
| `alembic upgrade head` then `downgrade 0004_pending_captures` then `upgrade head` | `0005_user_settings` applies and reverses cleanly against the live database |
| `npx tsc -b --noEmit` / `npx oxlint` | Clean |
| `npm run test` (Vitest, newly installed this slice) | **17 passed**, response-handler exhaustiveness for `UpdateTask`, `CompleteTask`, `DeleteTask`, `UpdateTimezone`, plus `RecordsController`'s empty-state case |
| `npm run build` | Clean production build |
| Manual browser pass, real backend + real Supabase session | Records table listed all 3 real tasks; opened a detail page; edited a title and flipped status to Done via the segmented control, table updated live; deleted a task via the confirm modal; search filtered server-side; Settings showed the real detected browser timezone, changed it, confirmed it persisted after reload |

### Deviations

| # | Deviation | Why | Consequence |
|---|---|---|---|
| D-24 | `records/graphql/types.py` does not redeclare `Task` | The sub-plan's file table (section 4) listed `Task` as one of the types created there, drafted before slice 1 settled where `Task` actually lives: `interfaces/dtos.py`, placed there specifically so it can cross into `capture` (deviation D-13). Redeclaring it in `graphql/types.py` would give the schema two incompatible `Task` types | `graphql/types.py` holds only what slice 1 didn't already build: the `TaskStatus`, `RecordOrigin` and `SortField` enums. No contract change, since every consumer (capture, and now records' own resolvers) already imports `Task` from `interfaces/dtos.py` |
| D-25 | `records`' and `identity`'s `graphql/__init__.py` files are empty; `app/graphql/schema.py` composes `Query`/`Mutation` by multiple inheritance from each domain's `RecordQueries`/`RecordMutations`/`IdentityQueries`/`IdentityMutations` classes directly, the same way `CaptureMutations` already does | Matches the pattern slice 1 actually shipped (`capture/graphql/__init__.py` is empty; `schema.py` imports `CaptureMutations` directly), not repo-rules.md §11's aspirational "domains register `queries =`/`mutations =`, schema.py iterates a domain list" description, which was never implemented | None functionally; `schema.py`'s class-base list grows by one entry per domain, same cost as slice 1 |
| D-26 | Every resolver argument that would otherwise shadow a Python builtin (`id`, `filter`, `input`) is renamed to `id_`/`filter_`/`input_` in the function signature, with `Annotated[T, strawberry.argument(name="id")]` (etc.) preserving the external GraphQL field name | repo-rules.md §7.1's own worked example uses `input: CreateRecordInput` as a literal parameter name, which `ruff`'s enabled `A002` rule (flake8-builtins) refuses. Untested until this slice, since slice 1's resolvers happened to avoid these three names. `ruff`'s config excludes `*.md` and `rules/` from linting, so the doc's own example was never actually checked against the lint config it's meant to satisfy | None to the schema — the GraphQL field names are unchanged, only the Python-side parameter names differ from the doc's illustrative naming |
| D-27 | The `records` query returns `[Task!]!` directly, not a separate `RecordSummary` type the sub-plan's file table named | Drafted, then reverted during review: with one record type this epic, a `RecordSummary` projection would carry the same fields `Task` already has, plus a `recordType` field whose value never varies ("task"), for no behavioural gain and one more DTO-to-type mapping to maintain. The canvas's "Type" column is a static "Task" label the frontend can render directly, the same way the mockup itself hardcodes it | The `records` list and `record(id)` detail share one type end to end. A second record type in a later epic is what actually justifies `RecordSummary`, added then with a change record |
| D-28 | `identity/models.py`'s `UserSettings` gained `created_at` in addition to the `user_id`/`timezone` the sub-plan's file table named | Every other table in this schema carries `created_at`/`updated_at`; T-2.10's own test case ("a second call returns the same row, not a new one") needs `created_at` to prove identity, not just value equality | Additive column, no contract change |
| D-29 | Query operation hooks (`useGetRecords`, `useGetRecordDetail`, `useGetTasks`, `useGetSettings`) use `useLazyQuery` plus a `useEffect` in the controller that calls the operation's `responseHandler` itself, instead of an `onCompleted` callback | Apollo Client 4 removed `onCompleted`/`onError` from `useLazyQuery` entirely (verified against its type definitions) — this was already how repo-rules.md §6.2's own query example was shaped, since only its mutation example used `onCompleted`; not a deviation from the documented pattern, only from an assumption made mid-slice | None; mutations (`updateTask`, `completeTask`, `deleteTask`, `updateTimezone`) still use `onCompleted` via `useMutation`, which Apollo Client 4 keeps |
| D-30 | `completeTask` has no UI trigger in this slice; `RecordEditForm` sends a status change through `updateTask` alongside the title, one "Save changes" button, one call | `RecordEdit.dc.html` draws a single save action for both fields, no separate complete affordance. The `CompleteTask` operation folder and its response-handler test were still built, per the task list, and sit ready for a future quick-complete control (a checkbox in `RecordTable`, say) that the canvas does not currently draw | `completeTask` is reachable over GraphQL and tested, just not wired to a click anywhere yet |
| D-31 | `DeleteConfirmModal`'s only real caller is `RecordDetailController`, deleting one id | The canvas draws no multi-select UI in `RecordTable`, so bulk delete (FR-21) has no UI to call it from yet. The component's props already accept a count for that future case | `deleteTask`'s multi-id path is proven at the interactor level (`test_delete_tasks_interactor.py`) and reachable over GraphQL; no frontend UI calls it with more than one id yet |
| D-32 | A sidebar app shell (`src/app/AppShell.tsx`) was built this slice, wrapping all three routes (`/`, `/records`, `/settings`) with the rail nav every canvas artboard draws | Neither slice's file table itemised it. Slice 1 shipped `CommandCenterController` as the sole full-page component with no way to navigate anywhere else, which was fine with one destination; slice 2 adds two more real destinations that would otherwise be reachable only by typing a URL | `router.tsx` now nests all three page components under one layout route. Slice 3 (installed app and theme) inherits a real shell to attach to, rather than needing to build one itself |

### Incidents and defects

None.

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-13 | Slice 1 backend built and verified: 2 domains, 2 migrations, 9 backend files beyond the original file-by-file plan (D-17's `list_open_tasks` addition), 83 tests passing including one real Gemini call. Frontend not started | User asked to build slice 1 | user |
| 2026-09-13 | Slice 1 frontend built and verified: project bootstrapped from scratch (Vite, Tailwind v4, Apollo Client 4, MobX, codegen), `tokens.css`, three operation folders, `CaptureStore`, `CommandCenterController` and its components, ported from the canvas's `Main.dc.html`. Verified against the real backend, real database and real Gemini in a browser, all five capture flows (add-task with a date, add-task without one, `/tasks`, non-command, unrecognised command) | User asked to bootstrap the frontend and finish slice 1's UI | user |
| 2026-09-13 | Slice 2 backend built and verified: `records` extended (5 new repository methods, 4 interactors, a full `graphql/` folder), `identity` domain built from scratch, 1 migration, 116 tests passing (70 unit, 46 integration) | User asked to build slice 2 | user |
| 2026-09-13 | Slice 2 frontend built and verified: 8 operation folders, `RecordsStore`/`SettingsStore`, `RecordsController`/`RecordDetailController`/`SettingsController` and their components, a new sidebar app shell (D-32), Vitest and React Testing Library installed for the first time. Verified against the real backend and a real Supabase session in a browser: list, detail, edit, complete-via-edit, delete, search, and timezone change all confirmed working | User asked to build slice 2 | user |
