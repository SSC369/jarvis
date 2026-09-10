---
doc: build-plan
feature: 000-ai-gateway
title: AI Gateway and Usage
stage: 3
status: draft
owner: user
created: 2026-09-10
updated: 2026-09-10
approved_on: null
supersedes: null
---

# Build Plan (HLD) — AI Gateway and Usage

Context: [PRD](./01-prd.md) · [Epic](./00-epic.md) · [Tech stack](../tech-stack.md) · [Backend ruleset](../../backend/rules/repo-rules.md)

Design stage: none. This epic has no user-facing surface, with one exception
that section 10 asks about.

This document locks the high-level architecture. It also asks. Section 10 must
be answered before approval.

## 1. Architecture summary

The gateway is one backend domain, `app/domains/gateway/`, and it is the only
code in Slashit that holds the Gemini credential or speaks to a provider. Other
domains import a single port from its `public.py`, hand it a `user_id` and a
schema, and receive either a parsed result or one of six named failures. Every
call, successful or not, writes one row to `ai_usage` carrying counts and no
content. The call is a single synchronous request and response, bounded by a
timeout, retried at most once, and never streamed. Nothing in V1 limits how
much any user consumes, which is a deliberate choice recorded in
[the PRD](./01-prd.md#11-open-questions) and carried into section 9 as the
largest open risk.

## 2. Component map

| Component | Responsibility | Talks to | New or existing |
|---|---|---|---|
| `core/settings.py` | The only reader of `os.environ`. Holds `GEMINI_API_KEY` | Nothing | New |
| `core/auth.py` | Verifies the Supabase JWT, produces `user_id` | Supabase JWKS | New |
| `core/context.py` | Per-request `Context`: `user_id`, session, loaders | — | New |
| `core/deps.py` | Composition root. The only place a repository or adapter is built | Every domain | New |
| `gateway/public.py` | The gateway's entire contract to other domains | — | New |
| `gateway/interactors/run_extraction.py` | The use case. Orchestrates, times, classifies failures, records usage. No I/O of its own | Ports only | New |
| `gateway/services/gemini_client.py` | **The only holder of the credential.** Builds the request, calls Gemini, maps provider errors to typed failures | Gemini API | New |
| `gateway/repositories/usage_repository.py` | The only SQL over `ai_usage` | PostgreSQL | New |
| `gateway/services/operator_alert.py` | Sends the quota-exhaustion alert, throttled | Resend | New |
| `gateway/graphql/queries.py` | The operator usage query, FR-14 | Interactor | New |
| `gateway/models.py` | The `ai_usage` table | — | New |
| `gateway/constants.py` | Timeouts, retry budget, model id, alert throttle | — | New |

```
                    caller domain (records, in epic 001)
                              |
                    ports.py  |  ExtractionPort, owned by the caller
                              v
                 adapters/gateway_extraction_adapter.py
                              |
                              |  imports gateway/public.py only
                              v
  +---------------------- gateway domain ----------------------+
  |                                                            |
  |   public.py                                                |
  |      |                                                     |
  |      v                                                     |
  |   interactors/run_extraction.py                             |
  |      |                  |                     |            |
  |      v                  v                     v            |
  |   GeminiClient    UsageRepository      OperatorAlert        |
  |      |                  |                     |            |
  +------|------------------|---------------------|------------+
         v                  v                     v
    Gemini API         ai_usage table          Resend
   (credential           (counts only,       (throttled, on
    stops here)          never content)    quota exhaustion)
```

**The credential boundary is one file.** `gemini_client.py` reads the key from
`settings` and nothing above it in the diagram can name a provider. That is
FR-5 and rule T4, enforced by structure rather than by review.

## 3. Data model

One table. Migrations required: yes, one.

| Entity | Key fields | Owns | Lifecycle | Tenancy scope |
|---|---|---|---|---|
| `ai_usage` | `id`, `user_id`, `provider`, `model`, `operation`, `input_tokens`, `output_tokens`, `total_tokens`, `outcome`, `latency_ms`, `request_id`, `occurred_at` | The gateway | Written once per model call, never updated, never deleted in V1 | `user_id`, filtered in the repository |

```sql
create table ai_usage (
    id            uuid primary key default gen_random_uuid(),
    user_id       uuid not null references auth.users(id) on delete cascade,
    provider      text not null,
    model         text not null,
    operation     text not null,
    input_tokens  integer not null default 0,
    output_tokens integer not null default 0,
    total_tokens  integer not null default 0,
    outcome       text not null,
    latency_ms    integer not null,
    request_id    text not null unique,
    occurred_at   timestamptz not null default now()
);

create index ai_usage_user_occurred_idx on ai_usage (user_id, occurred_at desc);
create index ai_usage_occurred_idx      on ai_usage (occurred_at desc);
create index ai_usage_outcome_idx       on ai_usage (outcome) where outcome <> 'success';
```

Four things about this table are decisions, not defaults.

**No cost column.** Q3 was answered "not needed now". Cost is a pure function of
`model`, `input_tokens` and `output_tokens`, so storing it would duplicate
derivable data. A rate card applied at read time produces the same figure on the
day someone wants it, with no backfill and no wrong historical rate baked in.

**No content column, and no room for one.** FR-12 and rule T6. The table has no
text field a prompt could be put in without a migration, which is the point.

**`request_id` is unique, and it is what makes FR-20 true.** The interactor
generates it before the first attempt and reuses it across the retry, so a
retried call cannot write two rows.

**`user_id` is not nullable.** Rule T2 as rewritten on 2026-09-10 needs a column
to filter on, and rule 1 of the backend ruleset §10 needs one to enable RLS
against later without a rewrite.

> Assumption: `on delete cascade` against `auth.users`. Deleting a user erases
> their usage history, which is right for a privacy posture and wrong for an
> operator reconciling a bill. Flagged rather than assumed silently.

## 4. API surface

The gateway serves two different callers, and they are not the same shape.

**In-process, to other domains.** This is the FR-16 contract and it is Python,
not HTTP. No network hop, no serialisation, no second auth check.

```python
# app/domains/gateway/public.py
@dataclass(frozen=True)
class ExtractionRequest:
    user_id: UUID
    operation: str          # "record_extraction". Names the call site for FR-11
    instruction: str        # the system instruction
    user_text: str          # never stored, never logged
    response_schema: type[BaseModel]

@dataclass(frozen=True)
class ExtractionSuccess:
    data: BaseModel
    usage_id: UUID

class ExtractionFailure(Enum):
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    TIMED_OUT            = "timed_out"
    QUOTA_EXHAUSTED      = "quota_exhausted"
    MALFORMED_RESULT     = "malformed_result"
    INVALID_REQUEST      = "invalid_request"

ExtractionOutcome = ExtractionSuccess | ExtractionFailure
```

Five failures, not six. `user_limit_reached` is listed in FR-18 and is not
emitted in V1, because FR-8 is deferred. The member is left out of the enum
rather than defined and never returned, so an exhaustiveness check in a caller
cannot pass against a case that will never arrive.

**Over GraphQL, to the operator.** One query, FR-14.

| Endpoint or action | Method | Auth | Input | Output | Serves |
|---|---|---|---|---|---|
| `operatorUsage` | GraphQL query | `IsOperator` | `from`, `to`, optional `userId` | Per-user rows and a total: requests, tokens, outcome counts | FR-14 |

No mutation. The gateway is never called from the client.

## 5. Model and vendor choices

| Use | Choice | Why | Fallback | Est. cost per call | Latency budget |
|---|---|---|---|---|---|
| Structured extraction from a command | Gemini Flash, paid tier | Settled in [the tech stack](../tech-stack.md). Native JSON-schema-constrained output removes the parse-and-repair loop | None in V1. A failure is a typed failure, not a second vendor | 0.0001 USD `estimate` | 8 s per attempt, 18 s ceiling `estimate` |

Every number in that row is `estimate` and none has been read from a vendor
page. Rule T8 requires that said rather than implied, and
[the tech stack](../tech-stack.md#7-verification-owed) already carries the
verification debt for the whole stack.

**Structured output, not prompt-and-parse.** The request pins
`response_mime_type: "application/json"` and a `response_schema` generated from
the caller's Pydantic model. The provider constrains generation to the schema,
so `MALFORMED_RESULT` becomes rare rather than routine.

**The exact model id is configuration, pinned at stage 4** against the current
model list, per FR-17. Naming a specific version string here would be inventing
a fact this document cannot check.

**Token budget.** Roughly 500 in and 150 out per capture, from
[the tech stack](../tech-stack.md#5-cost-envelope), `estimate`. `max_output_tokens`
is set from the caller's schema size at stage 4, not left unbounded, because an
unbounded output is an unbounded bill under a paid tier with no cap.

## 6. Cross-cutting concerns

| Concern | Decision |
|---|---|
| Authentication | Supabase JWT verified in `core/auth.py` against the project JWKS, on every request. An unverified request never reaches a resolver, which is FR-7. The gateway never authenticates on its own, it reads `user_id` off `Context` |
| Authorisation | Every GraphQL field declares a permission class. `operatorUsage` declares `IsOperator`. `IsAuthenticated` is not sufficient for it, and the difference is the whole of section 10 Q2 |
| Tenant isolation | `usage_repository` filters every read by `user_id`, except the operator query, which is the one deliberate cross-user read in the codebase and is gated by `IsOperator`. There is no RLS, per T2 as rewritten on 2026-09-10. The boundary test of rule T7 is mandatory: user A queries `operatorUsage`, receives a permission error, not a filtered list |
| Rate limits and quotas | **None in V1.** No per-user cap, no spend ceiling, no HTTP rate limit on `/graphql`. This is the answer to Q1 and Q8 and it is the largest known hole in this plan. See R-1 |
| Cost controls | One control exists and it is not in this codebase: the provider-side spend cap, T-Q9 of the tech stack. It is not set yet. `max_output_tokens` bounds a single call, the retry budget bounds a single failure, and nothing bounds a user |
| Caching | None. Two identical captures are two model calls. Caching an extraction keyed on user text would put user text in a cache, which rule T6 forbids in spirit even where it is silent |
| Observability | `structlog` with a request id on every line. Langfuse for the model call itself, see Q5. A log line carries `user_id`, `operation`, `outcome`, `latency_ms` and token counts, and never the prompt, the response or the key |
| Failure and retry | One retry, and only for `PROVIDER_UNAVAILABLE` and transport errors. Never for `MALFORMED_RESULT`, which is deterministic, and never for `QUOTA_EXHAUSTED`, which retrying makes worse. Backoff of 1 s. The `request_id` is generated once and reused, so the retry cannot double-record. This is FR-20 |
| Data retention and privacy | `ai_usage` rows are kept indefinitely, per Q4. No deletion job exists in V1. Rows carry counts only. A user deletion cascades their rows away |
| Secret handling | `GEMINI_API_KEY` is read once, in `settings.py`. Provider exceptions are caught in `gemini_client.py` and re-raised as domain failures carrying a message the client wrote, never the provider's raw error body, because a provider error body can echo a request header. This is FR-2 and FR-3 |

**Quota exhaustion, which is what Q6 asked about.** With no per-user limit, the
only exhaustion left is the provider's own. The chain is:

1. Gemini returns `RESOURCE_EXHAUSTED` or HTTP 429.
2. `gemini_client` maps it to `QUOTA_EXHAUSTED`. No retry.
3. The interactor writes the `ai_usage` row with that outcome, so FR-13 holds.
4. The caller receives a typed failure and refuses the capture honestly, which
   is epic 001's FR-35.
5. `operator_alert` sends one email, and **at most one per hour**, held in
   `constants.py` as `ALERT_THROTTLE_SECONDS = 3600`. Without a throttle, the
   condition that broke capture also sends one email per failed capture.

The alert is fired from a Procrastinate job, not inline. A user waiting on a
capture does not also wait on an SMTP round trip, which is NFR-5.

**Usage recording and NFR-5.** The row is written inside the same transaction as
the request, after the provider returns. It is a single insert against an
indexed table and it is well inside the 10 ms budget. It is not deferred to a
job: a job queue that loses a row loses attribution, and FR-15 forbids silent
loss. If the insert raises, the failure is logged at `error` and the extraction
result is still returned, because failing a user's capture to protect a usage
row is the wrong trade.

## 7. Alternatives considered

| Decision | Chosen | Alternatives | Why they lost | Reversibility |
|---|---|---|---|---|
| Gateway shape | An in-process domain behind `public.py` | A separate HTTP service | A network hop, a second deploy target and a second auth boundary, to isolate one file that already isolates itself | cheap |
| Caller contract | Typed result union | Raise an exception on failure | FR-18 needs the caller to act on the difference between five failures. Exceptions push that into `except` chains, which is anti-pattern 2 of the backend ruleset §17 | cheap |
| Output parsing | Provider-side schema constraint | Prompt for JSON, parse, repair on failure | The repair loop doubles cost and latency on exactly the calls already going badly | cheap |
| Usage write | Synchronous insert in the request | A Procrastinate job | A queue hop between the call and its record is a window where attribution is lost. NFR-3 measures that window | cheap |
| Cost figure | Not stored, derived later | Store `estimated_cost_usd` per row | Duplicates derivable data and freezes a rate that changes | cheap |
| Alert transport | Email through Resend | A log line the operator reads | A log line nobody is watching is not an alert | cheap |
| Retry policy | One retry, two failure classes | Retry everything three times | Under a paid tier with no spend cap, an aggressive retry on a systemic failure is a bill multiplier | cheap |
| Per-user limits | None, by user direction | A request cap, a token cap, a spend cap | Not argued down. Deferred by the answer to Q1 and Q8 so the product can be reached first | **costly** — see R-1 |

Every row is cheap to reverse except the last, and the last is the one that was
chosen against the recommendation.

## 8. Architecture decisions to lock

| # | Decision | Status | Graduates to tech-stack.md or product.md |
|---|---|---|---|
| AD-1 | One domain holds the credential. No other component reads `GEMINI_API_KEY` or imports a provider SDK | proposed | yes, tech stack. It generalises past this epic |
| AD-2 | Callers receive a typed union of one success and five failures. The gateway raises nothing across `public.py` | proposed | no, epic-local |
| AD-3 | Structured output is constrained provider-side by a JSON schema, not prompted and parsed | proposed | no, epic-local |
| AD-4 | Usage is written synchronously in the request transaction, never queued | proposed | no, epic-local |
| AD-5 | The backend is async throughout: `async def` resolvers, SQLAlchemy 2.0 async, `psycopg` 3 async. A sync driver behind an async resolver blocks the event loop, and subscriptions in epic 002 need the loop free | proposed | yes, tech stack. It binds every later epic |
| AD-6 | Cost is derived at read time from a rate card, never stored per row | proposed | no, epic-local |
| AD-7 | No rate limit, quota or spend ceiling ships in V1 | proposed | yes, product doc. It is a product posture, not a technical one |

## 9. Risks

| Risk | Impact | Mitigation | Trigger to revisit |
|---|---|---|---|
| **R-1. One user, or one retry loop, runs up an unbounded bill.** FR-8 is deferred, no spend ceiling exists, and the provider-side cap is not set | severe. This is money, and it is silent until the invoice | **There is no mitigation in this codebase.** The provider-side spend cap, T-Q9, is the entire defence and it is unset. The `ai_usage` table makes the damage visible afterwards, not preventable | Before the first real user. Or the first invoice above the 5 USD envelope |
| **R-2. A forgotten `user_id` predicate returns another user's rows.** RLS was the database-level catch and it is deferred | severe | Rule T2 as rewritten, plus the mandatory T7 boundary test. Both are code-review and test discipline, not a guarantee | The first time a repository method is written without a `user_id` argument |
| The credential leaks through a provider error body echoed into a client response | severe, and not patchable. A leak is fixed by rotation | FR-2 and FR-3. `gemini_client` never passes a provider message upward. Secret scanning in CI, NFR-1 | Any change to error handling in `gemini_client.py` |
| The operator screen becomes a second cross-user read that later grows without a permission check | high | `IsOperator` on the field, and exactly one cross-user repository method, named so it is greppable | A second operator field |
| Gemini deprecates the pinned model id | medium | FR-17 makes model a config value. A change is an environment variable | A provider deprecation notice |
| The gateway accretes per-caller special cases | medium | `public.py` takes a schema and returns data. A caller-specific branch inside the gateway is the smell | The second `operation` value that needs different handling |
| The alert throttle hides a second, different failure | low | The throttle is per outcome class, not global | A second alerting outcome |

## 10. Questions for the user

Answer before approval. Grouped, with the recommendation stated.

| # | Question | Options | Recommendation | Answer |
|---|---|---|---|---|
| Q1 | You chose a **screen** for FR-14, but epic 000 has no design stage and no frontend exists yet. Where is it drawn? | **(a)** Ship the `operatorUsage` query in 000 and draw the screen inside epic 001, where the shell and design system already exist. **(b)** Open a design stage on 000 and draw it now. **(c)** Ship the query now and read it through a GraphQL client until 001 lands | **(a).** It keeps 000 backend-only as the PRD intends, and a screen drawn without a design system is a screen redrawn later | |
| Q2 | How is an operator recognised, since no role concept exists? | **(a)** `OPERATOR_USER_IDS` in the environment, checked by `IsOperator`. **(b)** A custom claim in Supabase `app_metadata`. **(c)** A `role` column on a users table | **(a).** There is one operator, it is you, and an environment variable needs no schema, no migration and no admin surface to manage it | |
| Q3 | R-1 is severe and unmitigated. The provider-side spend cap is the only defence and it is not set. Is it set before the first API call, and at what figure? | A monthly figure, in USD | Set it before the key is first used, at 10 USD a month. That is well above the envelope's 1 USD and well below a number that hurts | |
| Q4 | T-Q1 is still open: Render or Railway. It does not block this architecture, but it blocks the deploy step of stage 4 | Render, Railway | Either. Decide when stage 4 reaches the deploy task, not now | |
| Q5 | Langfuse is in the stack. Does it ship in this epic, or later? | **(a)** Now, wrapping the Gemini call. **(b)** Later, when there is prompt quality to debug | **(b).** `ai_usage` answers every FR-14 question already. Langfuse answers "why was this extraction wrong", which is an epic 001 question and needs 001's prompts to exist | |
| Q6 | `ai_usage` cascades on user deletion, erasing that user's history. Right? | Cascade, or retain the rows with a nulled `user_id` | Cascade. Retaining usage for a deleted user is a privacy question nobody asked for | |

## 11. Backend dependencies

Named here so stage 4 installs a list that was reviewed rather than assembled at
the keyboard. Versions are pinned at stage 4 against the current index, not
guessed here.

**Runtime**

| Package | Why |
|---|---|
| `fastapi` | The API framework |
| `strawberry-graphql[fastapi]` | The GraphQL server, mounted on it |
| `uvicorn[standard]` | ASGI server |
| `pydantic`, `pydantic-settings` | Settings and the extraction schemas of section 4 |
| `sqlalchemy[asyncio]` | ORM and Core, async per AD-5 |
| `alembic` | Migrations |
| `psycopg[binary,pool]` | PostgreSQL driver, async |
| `google-genai` | The Gemini SDK. **The only package that may import a provider** |
| `pyjwt[crypto]` | Supabase JWT verification in `core/auth.py` |
| `httpx` | JWKS fetch, and the SDK's transport |
| `structlog` | Structured logging |
| `procrastinate` | The job queue, used here only for the alert |
| `resend` | The operator alert |

**Development**

| Package | Why |
|---|---|
| `pytest`, `pytest-asyncio` | The suites of §15 of the backend ruleset |
| `pytest-cov` | Coverage |
| `ruff` | Lint and format |
| `mypy` | The type discipline §16 requires is not optional without it |
| `detect-secrets` | NFR-1 wants secret scanning in CI, and NFR-1 has the only acceptable number in the PRD |

`langfuse` is deliberately absent, pending Q5.

## Change log

| Date | Change | Why | Approved by |
|---|---|---|---|
| 2026-09-10 | Created against the eight answered PRD questions and the 2026-09-10 tech-stack revision | PRD approved 2026-09-09, no design stage, and every open question closed | pending |
