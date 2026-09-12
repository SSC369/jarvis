---
doc: build-plan
feature: 000-ai-gateway
title: AI Gateway and Usage
stage: 3
status: approved
owner: user
created: 2026-09-09
updated: 2026-09-12
approved_on: 2026-09-12
supersedes: null
---

# Build Plan (HLD) — AI Gateway and Usage

> **Approved** by @user on 2026-09-12. Locked — changes require a change record (§7).

Context: [PRD](./01-prd.md) · [Epic](./00-epic.md) · [Tech stack](../tech-stack.md)

No design stage. This epic has no screen.

This document locks the high-level architecture. It also asks. Section 10 must
be answered before approval.

> **One vendor finding changed this plan before it was written.** Google no
> longer publishes per-tier rate limits in its documentation, so the PRD
> dependency assigned to Claude could not be closed as written. The limits were
> read from the account instead. Section 5.

## 1. Architecture summary

The gateway is one domain, `app/domains/gateway/`, and it is the only code in
Slashit that holds the provider credential or speaks to Gemini. Callers ask it
for a structured extraction and receive a typed result. They never name a
provider.

Every call runs the same four steps in order: authenticate the user, check that
user's allowance, call the provider under a timeout, record the usage. The
allowance check happens before the provider call, so a user over their limit
costs nothing.

Usage is written to PostgreSQL in the same transaction as the caller's work, so
a restart cannot lose it. Prompt and response content never reach that table.

Other domains reach the gateway the way every domain reaches another: through
`gateway/public.py`, a port the consumer owns, and an adapter. See
[the backend ruleset](../../backend/rules/repo-rules.md) section 6.

## 2. Component map

| Component | Responsibility | Talks to | New or existing |
|---|---|---|---|
| `core/auth.py` | Verify the Supabase JWT, produce `user_id` | Supabase JWKS | New |
| `core/db.py` | Session, and the per-transaction identity that makes RLS bind | PostgreSQL | New |
| `gateway/services/extraction_service.py` | The one entry point. Orchestrates the four steps | The three below | New |
| `gateway/services/allowance_service.py` | Read a user's limit, decide if this call is permitted | `usage_repository`, `settings` | New |
| `gateway/adapters/gemini_client.py` | The only holder of the credential. Speaks Gemini | Gemini API | New |
| `gateway/repositories/usage_repository.py` | Write and read `ai_usage` | PostgreSQL | New |
| `gateway/public.py` | What other domains may import | — | New |

```
caller domain (records, later epics)
    │  its own port, its own adapter
    ▼
gateway/public.py  →  ExtractionService
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
 AllowanceService   GeminiClient      UsageRepository
        │            (the key)              │
        ▼                 ▼                 ▼
   ai_usage          Gemini API         ai_usage
   (read)                               (write)
```

The credential enters at exactly one place, `GeminiClient`, constructed from
`settings` in the composition root. Nothing else can reach it.

## 3. Data model

| Entity | Key fields | Owns | Lifecycle | Tenancy scope |
|---|---|---|---|---|
| `ai_usage` | `id`, `user_id`, `provider`, `model`, `input_tokens`, `output_tokens`, `total_tokens`, `estimated_cost_usd`, `outcome`, `latency_ms`, `created_at` | gateway | Append only. Never updated | RLS on `user_id`. Operator reads via service role |
| `ai_user_limit` | `user_id`, `plan`, `requests_per_day`, `updated_at` | gateway | Mutable, rarely | RLS on `user_id`, writable only by service role |

`outcome` is an enum and carries FR-13 and FR-18: `success`, `provider_unavailable`,
`provider_timeout`, `shared_quota_exhausted`, `user_limit_reached`,
`malformed_result`. A failed call is a row, not an absence.

There is no `users` table. The epic's supplied model listed one, but
[the tech stack](../tech-stack.md) puts identity in Supabase's `auth.users`, and
a second copy is the synchronisation failure that decision rejected Clerk over.
`ai_usage.user_id` is a foreign key to `auth.users(id)`.

`plan` carries one value, `free`, exactly as the PRD said it would. The epic
listed it on a `users` table; it lives on `ai_user_limit` instead, because that
is a table Slashit owns and `auth.users` is not. The column exists so it does not
have to be added later, which is the PRD's stated reason for keeping it.

Migrations required: yes, two tables, both with RLS enabled and a policy in the
same migration, per rule T2.

## 4. API surface

The gateway exposes **no GraphQL fields**. It is called in-process by other
domains. This is the whole point of FR-16 and it is why this epic has no screen.

| Action | Caller | Auth | Input | Output | Serves |
|---|---|---|---|---|---|
| `ExtractionService.extract()` | Any domain, via its own port and adapter | `user_id` from request context | prompt parts, target schema, timeout | `ExtractionResult` union | FR-16, FR-18 |
| `UsageRepository.usage_for_period()` | Operator, out of band | Service role | date range, optional `user_id` | usage rows | FR-14 |

`ExtractionResult` is a union, matching
[the backend ruleset](../../backend/rules/repo-rules.md) section 8: `Extraction`,
`UserLimitReached`, `SharedQuotaExhausted`, `ProviderUnavailable`,
`ProviderTimeout`, `MalformedResult`. Six members, one per FR-18 outcome.

Operator access for FR-14 is a SQL query in V1, not a screen. See Q5.

## 5. Model and vendor choices

Every number in this section is sourced, per rule T8. Model positioning is from
Google's model documentation, read 2026-09-09. Rate limits are from the account
dashboard, read 2026-09-10.

| Use | Choice | Why | Fallback | Latency budget |
|---|---|---|---|---|
| Structured extraction from a capture command | `gemini-2.5-flash` | Google describes it as the best price-performance model for low-latency, high-volume tasks, which is this workload exactly | None in V1. A failure is a typed refusal, per FR-18 | 8 s, then abandon per FR-19 |

### Rate limits, read from the account on 2026-09-10

The PRD assigned Claude to read Gemini's paid-tier rate limits from
documentation. **That is not possible.** Google's rate limits page no longer
publishes per-tier RPM, TPM and RPD. It states limits depend on usage tier and
account status, and directs the reader to their own dashboard. The dependency
moved to the user and was discharged by reading the account.

For `gemini-2.5-flash`, after a billing account was linked on 2026-09-10:

| Limit | Free tier, read first | Paid, after billing | Binding? |
|---|---|---|---|
| RPM | 5 | 10,000 | No |
| TPM | 250,000 | 1,000,000 | No. 650 tokens per capture means TPM binds only above ~1,500 captures per minute |
| RPD | 20 | **1,000** | **Yes. This is the ceiling** |

> Assumption: RPM 10,000 alongside RPD 1,000 is an unusual pairing, since the
> day's whole budget could be spent in six seconds. Google's Tier 1 for this
> model is more commonly RPM 1,000 with RPD 10,000. **Worth re-reading the
> dashboard to confirm the two are not transposed.** Nothing below changes if
> they are: RPD is the ceiling either way, and 10,000 would mean more headroom,
> not less. The conservative figure is used throughout.

The free-tier reading is kept in the table because it is the evidence behind
goal G4. It also confirmed that the project had been running on free-tier terms,
which is the data-handling risk [the tech stack](../tech-stack.md) rejected when
it moved to the paid tier. Linking billing closed that, and Google applied the
new limits immediately as its documentation says it would.

### What 1,000 requests per day supports

Rate limits are per project, not per API key. This is the whole product's daily
budget.

| Users, each capturing | Project usage per day | Fits in 1,000? |
|---|---|---|
| 10 users at 10 captures | 100 | Yes, 10% of ceiling |
| 50 users at 10 captures | 500 | Yes, 50% |
| 20 users at 20 captures | 400 | Yes, 40% |
| 100 users at 10 captures | 1,000 | At the ceiling |

Goal G4 of the PRD asks whether the tier carries the load. Answered: **yes, to
roughly 50 to 100 users at realistic personal-capture volume**, and the operator
now has the number to watch.

## 6. Cross-cutting concerns

| Concern | Decision |
|---|---|
| Authentication | Supabase-issued JWT verified in `core/auth.py` against Supabase's JWKS endpoint, per request, with the public key cached. An unverified token never reaches a resolver, satisfying FR-7 |
| Authorisation | The gateway is not callable from outside the process. There is no field, so there is no field permission. The caller's own resolver carries the permission class |
| Tenant isolation | RLS on both tables keyed on `user_id`. The gateway never accepts a `user_id` argument from a caller; it reads it from the request context, so a caller cannot attribute a call to someone else. This is the mechanism behind FR-6 |
| Rate limits and quotas | **20 model calls per user per day.** Checked before the provider call in `AllowanceService`, reading `ai_user_limit.requests_per_day` with a default in `settings` for a user with no row. One row change, no deploy, satisfying FR-10 |
| Cost controls | Two layers. Per user, the allowance check. Globally, a provider-side spend cap set in the Google console, which is the only defence that works while nobody is watching. See the tech stack section 7 |
| Caching | None. Extraction of a user's own command is not cacheable across users, and caching within a user would return yesterday's interpretation of "tomorrow" |
| Observability | Langfuse for the model call, structlog for the request. `request_id` on every line. Rule T6 binds: prompt content never reaches usage or analytics tables. Langfuse holds prompts and is therefore not an analytics store for this purpose, see Q6 |
| Failure and retry | One retry, only on a connection error or an HTTP 5xx, never on a timeout or a malformed result. The usage row is written once per logical call with the final outcome, satisfying FR-20 |
| Data retention and privacy | `ai_usage` holds counts only, never text, enforced by the table having no text column that could hold it. Retention is Q4 |

**The timeout is 8 seconds** (NFR-4). `estimate`, chosen because a capture is a
foreground action and a user will not wait longer. It wants measuring against
real p95 latency once epic 001 runs, and revising then.

## 7. Alternatives considered

| Decision | Chosen | Alternatives | Why they lost | Reversibility |
|---|---|---|---|---|
| Gateway shape | An in-process domain | A separate service | A network hop, a second deploy and a second secret store, for one caller and no scaling need | cheap |
| Usage write timing | Same transaction as the caller's work | Fire-and-forget background job | NFR-6 requires survival of a restart. A queued write that dies in memory is exactly the loss it forbids | cheap |
| Usage write timing | Same transaction | Procrastinate job | Adds latency and a failure mode to satisfy NFR-5's 10 ms, which a single insert already satisfies | cheap |
| Identity source | Supabase `auth.users` only | A mirrored `users` table, as the epic supplied | A second copy needs synchronising, which is the failure the tech stack rejected Clerk over | costly |
| Limit storage | `ai_user_limit` table | Environment variable | FR-10 requires change without a deploy | cheap |
| Limit check | Count rows in `ai_usage` for the window | A counter in Redis | The tech stack removed Redis deliberately. At dozens of calls a day an indexed count is free | cheap |
| Model | `gemini-2.5-flash` | `gemini-3.8-flash` | Google positions 3.8 Flash for long-horizon software engineering. This workload parses one sentence, and 2.5 Flash is the stated price-performance choice for low-latency, high-volume work | cheap |
| ORM | SQLAlchemy 2.x async | SQLModel | Thinner, and by FastAPI's author, but it lags SQLAlchemy on async and complex queries, and this codebase has a repository layer that wants full query power | costly |
| ORM | SQLAlchemy 2.x async | Raw asyncpg | Fast, but every repository hand-rolls mapping, and Alembic has nothing to read | costly |
| Migrations | Alembic | Supabase CLI SQL migrations | Attractive because RLS policies are SQL, but two migration histories over one database is the problem it appears to solve. Alembic executes raw SQL for policies | costly |
| Driver | asyncpg | psycopg3 | Both work. asyncpg is faster and is what SQLAlchemy's async docs assume. See the pooling note below | cheap |

**Pooling and RLS, answering T-Q2.** Identity reaches the connection with
`SET LOCAL request.jwt.claims` inside the transaction that does the work.
`SET LOCAL` is scoped to the transaction and unsets on commit, so a pooled
connection cannot leak one user's identity to the next. This is why the usage
write shares the caller's transaction rather than opening its own.

> Assumption: connecting through Supabase's pooler in transaction mode requires
> `statement_cache_size=0` on asyncpg, because transaction pooling and prepared
> statements conflict. Stated from knowledge of the pooler's behaviour and **not
> verified against Supabase's current documentation**. It must be confirmed at
> stage 4, and it is Q8 below.

## 8. Architecture decisions to lock

> **AD-7 was amended on 2026-09-12, after approval.** The original decision named
> `SET LOCAL request.jwt.claims` alone. Measured against the live database, that
> leaks every row: the `postgres` role carries `rolbypassrls`, which outranks
> `FORCE ROW LEVEL SECURITY`, so the policy is never evaluated. The corrected
> decision adds `SET LOCAL ROLE authenticated`, which drops the bypass privilege
> for the transaction. Evidence and the corrected design are in
> [04.2](./04.2-identity-and-isolation.md) section 6.

| # | Decision | Status | Graduates to tech-stack.md |
|---|---|---|---|
| AD-1 | The gateway is an in-process domain with no GraphQL field | locked | no |
| AD-2 | `gemini-2.5-flash` is the V1 model | locked | yes, the stack names only "Gemini Flash" |
| AD-3 | ORM is SQLAlchemy 2.x async | locked | **yes, no row exists** |
| AD-4 | Migrations are Alembic, RLS policy in the creating migration | locked | **yes, no row exists** |
| AD-5 | Driver is asyncpg | locked | **yes, no row exists** |
| AD-6 | Python 3.12 | locked | **yes, no row exists** |
| AD-7 | Identity reaches the connection by `SET LOCAL` claims **and** `SET LOCAL ROLE authenticated`, both inside the work transaction | **amended 2026-09-12** | yes, closes T-Q2 |
| AD-8 | Usage is written in the caller's transaction, not a job | locked | no |
| AD-9 | No mirrored `users` table. `auth.users` is the only identity store | locked | yes |

AD-3 to AD-6 are the four rows that block `backend/requirements.txt`. They are
the reason this document was written before that file.

## 9. Risks

| Risk | Impact | Mitigation | Trigger to revisit |
|---|---|---|---|
| The 8 s timeout is wrong in both directions: too short for a slow model, too long for a foreground action | medium | Labelled `estimate`, measured in epic 001 | First real p95 latency reading |
| `SET LOCAL` is omitted on a path, silently disabling RLS with no error | severe | Rule T7's boundary test, plus a session-level default that grants nothing | Any new connection path |
| Counting `ai_usage` rows for the allowance check gets slow | low | Index on `(user_id, created_at)`. At V1 volume this is not a real risk | Sustained four-figure daily calls per user |
| Langfuse holds prompt content, and prompt content is passports and finances | severe | Rule T6 keeps it out of usage tables. Langfuse is a separate question, Q6 | Before the first real user |
| The project ceiling of 1,000 requests per day is shared, so growth past ~50 users exhausts it silently | high | The allowance check of FR-8 caps each user at 50. G4's metric is project usage against 1,000, watched by the operator. Tier 2 is the escalation | Sustained days above 60% of ceiling |
| The spend cap is set in the gateway but not at the provider | high | The provider-side cap is the one that works unattended. Named in section 6 and owed per the tech stack section 7 | Before the first real user |

## 10. Questions for the user

Answer before approval. The first seven are the PRD's open questions, carried
here as the PRD said they would be.

| # | Question | Options | Recommendation | Answer |
|---|---|---|---|---|
| Q1 | What is the per-user limit, and over what window? PRD Q1 | Requests per day / tokens per month / spend per day | **20 model calls per user per day.** Flat, no tiers | **Answered 2026-09-10.** 20 per day |
| Q2 | Is streaming needed in V1? PRD Q2 | Yes / no | **No.** Extraction returns a record, not prose. There is nothing to stream, and dropping it removes real complexity | **Answered 2026-09-10.** No streaming |
| Q3 | How is estimated cost computed? PRD Q3 | Rate card / zero | **Rate card, stored per row at the rate in force.** Storing the rate alongside the row keeps history correct when the rate card changes | **Answered 2026-09-10.** Rate card, stored per row |
| Q4 | How long are `ai_usage` rows kept? PRD Q4 | Forever / 13 months / 90 days | **13 months.** Enough for a year-over-year read, and small: one row per capture is well under a megabyte per user per year | **Answered 2026-09-10.** 13 months |
| Q5 | How does the operator read usage? PRD Q5 | SQL query / screen / periodic report | **SQL query in V1.** FR-14 says the operator can read it, not that there is a screen. A screen is its own epic | **Answered 2026-09-10.** SQL query |
| Q6 | When the shared quota is exhausted, should the gateway alert you? PRD Q6 | No / email / log only | **Email through Resend, once per hour at most.** Quota exhaustion breaks capture for everyone, and nobody is watching a log | **Answered 2026-09-10.** Email via Resend, hourly at most |
| Q7 | Read the account's real rate limits, since Google no longer publishes them | — | **Resolved 2026-09-10.** Billing linked, limits are RPM 10,000, TPM 1,000,000, RPD 1,000. One follow-up only: confirm RPM and RPD are not transposed, per the note in section 5 | **Answered** |
| Q8 | Does a spend ceiling replace the request ceiling? PRD Q8 | Requests only / spend only / both | **Both, as in Q1.** Google enforces its own spend limit per 10 minutes, so the concept already exists upstream | **Answered 2026-09-10.** Both ceilings |
| Q9 | Confirm the asyncpg and Supabase pooler assumption in section 7, or defer it to stage 4 | Confirm now / defer | **Defer to stage 4.** It changes two lines of connection configuration, not the architecture | **Answered 2026-09-10.** Deferred to stage 4 |
| Q10 | AD-3 to AD-6 add four rows that `tech-stack.md` does not have. Add them there on approval? | Yes / no | **Yes.** They bind every future epic, and rule 8 of the process says a decision beyond one feature graduates | **Answered 2026-09-10.** Yes, graduate them |
| Q11 | A request count does not bound request size. Where does the input-length cap live? | Epic 001 capture path / gateway / nowhere | **Epic 001.** A command input is short by nature and the cap belongs where the input arrives. Recorded in section 11.4 so it is not lost | |

## 11. The per-user limit, and what it supports

Added 2026-09-10. It sits outside the template because the capacity arithmetic
behind the limit is worth keeping, not because the plan needs another section.

### 11.1 The limit

**20 model calls per user per day.** One number, every user, no tiers.

A command input in chat is one model call, so this is 20 commands a day. That is
generous for personal capture, where 5 to 15 items a day is typical, and it is
the same figure the free Gemini tier allowed for the whole product, now applied
per user against a ceiling fifty times larger.

`plan` stays a single value. Tiers and pricing were explored on 2026-09-10 and
dropped the same day at the user's direction. **Nothing in this document reverses
the PRD**: "billing, plans and tiers" remains a non-goal, `plan` still carries one
value, and nothing is charged. The exploration is in git history, not here.

### 11.2 What it supports

The Gemini account allows 1,000 requests per day for the whole product, read from
the dashboard on 2026-09-10.

| Users | If every user hit the cap | Share of ceiling |
|---|---|---|
| 25 | 500 | 50% |
| 50 | 1,000 | **100%, the wall** |
| 60 | 1,200 | Over |

> Assumption: real usage runs at roughly 40% of cap, which is typical of metered
> products and is unmeasured here. On that assumption 50 users consume about 400
> calls a day and the practical ceiling is nearer 120 users. The 50-user figure
> is the safe one and is used below.

**Plan for 50 users on the current Gemini tier.** The per-user limit is not what
binds first; the shared project ceiling is.

### 11.3 Raising the ceiling

| Google tier | Qualification | Billing cap |
|---|---|---|
| Tier 1, current | Active billing account linked | 250 USD |
| Tier 2 | 100 USD paid, plus 3 days from first payment | 2,000 USD |
| Tier 3 | 1,000 USD paid, plus 30 days | 20,000 USD and above |

Read from Google's rate limits page on 2026-09-10. Qualification counts
cumulative spend across the whole Google Cloud billing account, not Gemini alone.

Tier 2 needs 100 USD of cumulative spend and 3 days from the first payment. That
spend accrues slowly at this volume, so the practical route is to reach the
threshold deliberately rather than wait for it. **Tier 2's RPD for this model is
not published** and must be read from the dashboard after upgrading.

The 50-user wall is therefore a three-day problem if it is seen coming. Trigger
the upgrade at 30 users, not at 50.

### 11.4 The gap this leaves

A daily request count bounds how often a user calls the model. It does not bound
how large each call is. Twenty requests carrying very large inputs cost far more
than twenty short commands.

**Recommendation: cap the length of a command input rather than adding a spend
ledger.** A chat command is inherently short, the cap belongs in the capture path
where the input arrives, and it bounds cost without a second thing to maintain.
The number belongs in epic 001, which owns capture. Raised here as Q11 so it is
not lost.

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-09 | Created | Epic 000 was at stage 3 waiting on it, and it blocks `backend/requirements.txt` | pending |
| 2026-09-10 | Real rate limits recorded: RPM 5, TPM 250K, RPD 20. These are free-tier numbers. Q1 suspended behind Q7, and a severe risk added | User read the AI Studio dashboard | pending |
| 2026-09-10 | All ten questions answered, user said go with the recommendations | User direction | user |
| 2026-09-10 | Section 11 added: three plan tiers and a pricing model | User asked for free, plus and pro tiers | pending |
| 2026-09-12 | **AD-7 amended after approval.** `SET LOCAL` claims alone leak every row, because `postgres` carries `rolbypassrls`. The role switch to `authenticated` is now mandatory. Stale downstream: none, no code had been written against AD-7. `tech-stack.md` section 3 updated in the same change | Measured against the live database while planning slice 2 | user |
| 2026-09-12 | **Build plan approved.** AD-1 to AD-9 locked. AD-2 to AD-7 and AD-9 graduated to `tech-stack.md` in the same commit, per rule 6 of the process. Q11 carried to epic 001, which owns capture | User said proceed | user |
| 2026-09-10 | Model cost figures removed throughout: the per-call cost, the rate-card comparison, the spend projections and the promotional-pricing risk. Rate limits and Google tier qualification thresholds kept | User direction | user |
| 2026-09-10 | Tiers and pricing dropped. One flat limit of 20 calls per user per day. Section 11 keeps the capacity and escalation arithmetic. No PRD non-goal is reversed any more. Q11 repurposed to the input-length cap | User direction: pricing not needed now, 20 commands per day for everyone | user |
| 2026-09-10 | Billing linked. Limits are now RPM 10,000, TPM 1,000,000, RPD 1,000. Q7 resolved, Q1 answered at 50 per user per day, free-tier risk closed and replaced with a shared-ceiling risk | User linked a billing account and re-read the dashboard | pending |
