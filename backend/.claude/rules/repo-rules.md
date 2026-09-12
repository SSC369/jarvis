---
doc: repo-rules
scope: backend
title: Backend Repository Structure and Patterns
status: current
owner: user
created: 2026-09-09
updated: 2026-09-12
---

# Backend — Repository Structure and Patterns

The binding ruleset for every file under `backend/`. It answers one question:
where does this code go, and what shape is it in. How a method is written
(types, keyword calls, interactor orchestration, names) lives in
[`code-rules.md`](./code-rules.md).

Read both before writing code here. A change that contradicts them says so in
the feature's dev log, per root `CLAUDE.md` rule 5.

## 1. Where these rules came from

Most of what follows is taken from a working system, not invented. The `radius`
project runs a 32,000 line Django backend on this architecture across seven
domains and roughly 140 unit tests. It proves the layer contract holds at scale.
It also shows what rots, and §17 lists those failures by name so they are not
repeated.

The translation is Django to FastAPI, Graphene to Strawberry, and Celery to
Procrastinate. The layering is unchanged, because the layering is not a Django
idea.

## 2. Stack, and what this folder supersedes

The stack is owned by [`process-docs/tech-stack.md`](../../process-docs/tech-stack.md).
The rows that shape this folder:

| Layer                  | Choice                                |
| ---------------------- | ------------------------------------- |
| Language               | Python                                |
| API framework          | FastAPI                               |
| GraphQL server         | Strawberry                            |
| Database               | PostgreSQL, hosted by Supabase        |
| Data isolation         | Row Level Security                    |
| Auth                   | Supabase Auth                         |
| Background jobs        | Procrastinate, backed by PostgreSQL   |
| Vector search          | pgvector                              |
| Notification transport | GraphQL subscriptions over WebSockets |

Standing rules T1 to T8 of the tech stack are binding here and are not restated.
T2, T3, T5 and T7 have direct structural consequences, in §10, §10, §5 and §15.

**One supersession.** The tech stack's Repository row reads
`apps/web`, `apps/api`, `packages/`. The user replaced it on 2026-09-09 with
`backend/` and `frontend/` at the repository root. That decision holds and this
document follows it. `process-docs/tech-stack.md` has not been updated to match
and should be.

## 3. Directory tree

```
backend/
├── CLAUDE.md
├── rules/
│   ├── repo-rules.md            ← this file
│   └── code-rules.md            ← types, keyword calls, names. See code-rules.md
├── pyproject.toml
├── .env.example                 ← every variable, no values
├── Dockerfile
├── app/
│   ├── main.py                  ← FastAPI app, mounts /graphql, health
│   ├── core/                    ← infrastructure, owned by no domain
│   │   ├── settings.py          ← pydantic-settings. The only reader of os.environ
│   │   ├── db.py                ← engine, session, per-transaction RLS identity
│   │   ├── auth.py              ← Supabase JWT verification
│   │   ├── context.py           ← request context: user_id, session, loaders
│   │   ├── errors.py            ← DomainError base
│   │   ├── deps.py              ← the composition root. See §9
│   │   ├── logging.py           ← structlog, request id
│   │   └── jobs.py              ← Procrastinate app
│   ├── domains/                 ← one folder per domain. See §5
│   │   ├── records/
│   │   ├── gateway/
│   │   └── identity/
│   ├── graphql/                 ← assembly only, no business logic
│   │   ├── schema.py            ← composed from domain exports. See §11
│   │   ├── permissions.py       ← Strawberry permission classes. See §12
│   │   ├── error_mapping.py     ← the @map_errors decorator. See §8
│   │   ├── loaders.py           ← DataLoader registry. Rule T5
│   │   └── scalars.py
│   └── migrations/              ← Alembic. RLS policy in the creating migration
└── tests/
    ├── unit/                    ← per domain, fake repositories
    ├── integration/             ← resolver through to database
    └── fakes/                   ← in-memory repository implementations
```

Two folders and nothing else may hold business logic: `app/domains/`. `core/`
and `graphql/` are plumbing. A business rule found in either is misplaced.

## 4. The layer contract

Code flows in one direction. Higher layers depend on lower ones. Never the
reverse, and never sideways into another domain.

```
graphql/  (resolvers, types, permissions)
    │
    ▼
interactors/            use cases. Business rules. No I/O
    │
    ▼
interfaces/             Protocols and DTOs. The contract
    │
    ▼
repositories/  services/   SQL, vendors, jobs, email
    │
    ▼
models/   PostgreSQL   Gemini   Procrastinate
```

| Layer      | May                                                      | May not                                                                    |
| ---------- | -------------------------------------------------------- | -------------------------------------------------------------------------- |
| Resolver   | Read context, call one interactor, return a union member | Touch the ORM. Hold a business rule. Call a second interactor              |
| Interactor | Validate, decide, orchestrate, raise domain errors       | Import SQLAlchemy. Construct its own collaborators. Call a vendor directly |
| Repository | Execute SQL, convert model to DTO                        | Return a model, a `Session` or a `Select`. Hold a business rule            |
| Service    | Talk to Gemini, Resend, the job queue                    | Import another domain's repository                                         |
| Adapter    | Import one other domain's `public.py` and translate it   | Return that domain's types upward. See §6                                  |
| Model      | Describe a table                                         | Contain methods with business meaning                                      |

**The test for a violation.** If deleting `graphql/` would break an interactor,
the dependency points the wrong way. If swapping PostgreSQL for a dictionary
would break an interactor, the repository is leaking.

## 5. Anatomy of a domain

Every domain has the same shape. A new domain is this tree with the names
changed, and nothing else.

```
app/domains/records/
├── models.py              SQLAlchemy tables. Nothing else
├── public.py              the ONLY names other domains may import. See §6
├── interfaces/
│   ├── dtos.py            frozen dataclasses crossing every boundary
│   ├── repositories.py    Protocol per repository. The contract
│   └── ports.py           Protocol per external need, in this domain's words. §6
├── repositories/
│   └── record_repository.py     implements the Protocol. The only SQL
├── adapters/              the only files that know another domain exists. §6
│   └── gateway_usage_adapter.py     implements a port against gateway
├── interactors/
│   ├── dtos.py            input DTOs, one per use case
│   ├── create_record.py   CreateRecordInteractor
│   ├── update_record.py
│   └── list_records.py
├── services/              stateless collaborators. What §6 publishes lives here
├── graphql/
│   ├── types.py           Strawberry output types
│   ├── inputs.py          Strawberry input types
│   ├── errors.py          error types and their exceptions together. See §8
│   ├── queries.py         RecordQueries
│   ├── mutations.py       RecordMutations
│   └── subscriptions.py   optional. See §13
├── errors.py              domain exceptions, if not colocated in graphql/errors.py
├── constants.py           enums, limits, defaults. No magic values elsewhere
├── jobs.py                Procrastinate tasks
└── tests/
```

**One file per use case in `interactors/`.** Not one file per entity. A file
named `record_service.py` holding six operations is the thing this layout
exists to prevent. `radius` has 34 interactor files in one domain and each is
readable in a minute.

**Naming.** File `create_record.py` holds class `CreateRecordInteractor` with
one public method `create_record`. The repetition is deliberate and makes the
codebase greppable.

## 6. Crossing a domain boundary

A domain never imports another domain's internals. Crossing happens through
exactly three pieces, and no other route is permitted.

| Piece             | Lives in                                                                   | Job                                                                               |
| ----------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Published service | The **providing** domain, in `services/`, re-exported from its `public.py` | The only entry point other domains may call                                       |
| Port              | The **consuming** domain, in `interfaces/ports.py`                         | A Protocol describing what this domain needs, in its own vocabulary               |
| Adapter           | The **consuming** domain, in `adapters/`                                   | Implements the port by calling the published service, and translates types across |

**The port belongs to the consumer.** This is the half that is easy to get wrong
and the half that does the work. If the consuming domain imports the providing
domain's interface, nothing has been decoupled; the dependency has been renamed.
The consumer declares what it needs, and the adapter is the only file in the
consuming domain that knows another domain exists at all.

### 6.1 Worked example

`records` needs to know whether a user is within their usage allowance. Usage is
owned by `gateway`.

**The provider publishes a narrow surface.**

```python
# app/domains/gateway/services/usage_service.py
class GatewayUsageService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def allowance_for(self, user_id: UUID) -> AllowanceDTO:
        ...


# app/domains/gateway/public.py
"""The only names other domains may import from gateway."""

from app.domains.gateway.services.usage_service import GatewayUsageService
from app.domains.gateway.interfaces.dtos import AllowanceDTO

__all__ = ["GatewayUsageService", "AllowanceDTO"]
```

**The consumer declares what it needs, in its own words.**

```python
# app/domains/records/interfaces/ports.py
class UsagePort(Protocol):
    async def has_capacity(self, user_id: UUID) -> bool: ...
```

Note what the port does not say. It does not mention allowances, tokens, spend
or `gateway`. `records` needs one boolean, so the port is one boolean.

**The adapter translates.**

```python
# app/domains/records/adapters/gateway_usage_adapter.py
from app.domains.gateway.public import GatewayUsageService


class GatewayUsageAdapter:
    """Implements records' UsagePort against the gateway domain."""

    def __init__(self, usage_service: GatewayUsageService) -> None:
        self.usage_service = usage_service

    async def has_capacity(self, user_id: UUID) -> bool:
        allowance = await self.usage_service.allowance_for(user_id)
        return allowance.remaining > 0
```

**The interactor sees only its own port.**

```python
class CreateRecordInteractor:
    def __init__(
        self,
        record_repository: RecordRepository,
        usage: UsagePort,
    ) -> None:
```

It can be tested with a two-line fake. It does not import `gateway`, and it does
not change when `gateway` changes shape.

### 6.2 What may cross

| May cross                                            | May not cross                                                       |
| ---------------------------------------------------- | ------------------------------------------------------------------- |
| A published service class, imported from `public.py` | A repository, concrete or Protocol                                  |
| A DTO listed in `public.py`                          | A model, a `Session`, a `Select`                                    |
| A constant or enum listed in `public.py`             | An interactor                                                       |
|                                                      | Anything under the provider's `graphql/`, including its error types |
|                                                      | Anything not named in `public.py`                                   |

**A domain's `public.py` is its contract.** Adding a name to it is a deliberate
act, reviewed like an API change, because from that moment other domains may
depend on it. A domain with no `public.py` exposes nothing and may not be
imported.

### 6.3 Direction, and no cycles

Dependencies between domains form a directed acyclic graph. If `records` adapts
`gateway`, then `gateway` may never adapt `records`, in either direction, at any
depth.

A cycle means the two domains are one domain wearing two names. When you find
yourself needing one, the fix is one of three things, never an exception:

1. Merge them, because the boundary was drawn in the wrong place.
2. Extract the shared concept into a third domain both may depend on.
3. Invert the direction with an event, so the provider announces and the
   consumer subscribes, rather than the provider calling back.

Enforce it with a test. An import-linter contract, or a test that walks
`app/domains/*/adapters/` and asserts the graph is acyclic, costs one afternoon
and holds forever.

## 7. The API lifecycle

One mutation, traced through every layer. This is the section the rest of the
document hangs off. Read it once and the layout explains itself.

### 7.1 Input and result types

`app/domains/records/graphql/inputs.py`

```python
import strawberry

@strawberry.input
class CreateRecordInput:
    title: str
    body: str
    kind: RecordKind
    occurred_at: datetime | None = None
```

`app/domains/records/graphql/errors.py`. Both faces of an error live in one
file, next to each other. See §8 for why.

```python
import strawberry
from app.core.errors import DomainError


@strawberry.type
class InvalidRecordText:
    message: str
    reason: str


class InvalidRecordTextError(DomainError):
    gql_type = InvalidRecordText

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(f"Invalid record text: {reason}")


@strawberry.type
class RecordLimitReached:
    message: str
    limit: int


class RecordLimitReachedError(DomainError):
    gql_type = RecordLimitReached

    def __init__(self, limit: int) -> None:
        self.limit = limit
        super().__init__(f"Record limit of {limit} reached")
```

`app/domains/records/graphql/mutations.py`

```python
from typing import Annotated, Union

CreateRecordResult = Annotated[
    Union[Record, InvalidRecordText, RecordLimitReached],
    strawberry.union("CreateRecordResult"),
]
```

### 7.2 Resolver

Four responsibilities and no fifth: read context, build the interactor from the
composition root, convert input to a DTO, call one interactor method.

```python
@strawberry.type
class RecordMutations:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @map_errors
    async def create_record(
        self, info: Info, input: CreateRecordInput
    ) -> CreateRecordResult:
        interactor = build_create_record_interactor(info.context)
        record = await interactor.create_record(
            CreateRecordInputDTO(
                user_id=info.context.user_id,
                title=input.title,
                body=input.body,
                kind=input.kind.value,
                occurred_at=input.occurred_at,
            )
        )
        return record_dto_to_type(record)
```

There is no `try` block. `@map_errors` owns the translation, and it is written
once. §8.

### 7.3 Interactor

Holds every business rule. Imports nothing from `graphql/` and nothing from
SQLAlchemy.

```python
class CreateRecordInteractor:
    def __init__(
        self,
        record_repository: RecordRepository,
        usage: UsagePort,
    ) -> None:
        self.record_repository = record_repository
        self.usage = usage

    async def create_record(self, dto: CreateRecordInputDTO) -> RecordDTO:
        """Create one record for a user.

        Raises:
            InvalidRecordTextError: title or body fails validation.
            RecordLimitReachedError: the user is at the plan ceiling.
        """
        title = normalise_title(dto.title)
        body = normalise_body(dto.body)

        count = await self.record_repository.count_for_user(dto.user_id)
        if count >= MAX_RECORDS_PER_USER:
            raise RecordLimitReachedError(limit=MAX_RECORDS_PER_USER)

        return await self.record_repository.create(
            CreateRecordStorageDTO(
                id=uuid7(),
                user_id=dto.user_id,
                title=title,
                body=body,
                kind=dto.kind,
                occurred_at=dto.occurred_at,
            )
        )
```

### 7.4 Repository

The only SQL in the codebase. Returns a DTO, always.

```python
class SqlRecordRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, dto: CreateRecordStorageDTO) -> RecordDTO:
        record = Record(**asdict(dto))
        self.session.add(record)
        await self.session.flush()
        return record_model_to_dto(record)
```

Its Protocol, in `interfaces/repositories.py`, is what the interactor depends
on:

```python
class RecordRepository(Protocol):
    async def create(self, dto: CreateRecordStorageDTO) -> RecordDTO: ...
    async def count_for_user(self, user_id: UUID) -> int: ...
```

Protocols, not abstract base classes. Structural typing means a test fake needs
no inheritance, and the Protocol stays a contract rather than a base class
someone is tempted to put behaviour in.

### 7.5 The shape

```
CreateRecordInput  →  CreateRecordInputDTO  →  [Interactor]
                                                  │
                                    ┌─────────────┴─────────────┐
                                    ▼                           ▼
                          CreateRecordStorageDTO          DomainError
                                    │                           │
                                    ▼                           ▼
                              [Repository]                 @map_errors
                                    │                           │
                                    ▼                           ▼
                                RecordDTO                  error type
                                    │                           │
                                    └──────────►  union  ◄──────┘
```

**DTOs at every boundary, frozen dataclasses, no exceptions.** Two families:
`interactors/dtos.py` for what goes in, `interfaces/dtos.py` for what comes back.
A model instance crossing a layer is a defect.

## 8. Errors are data

Every mutation returns a union of one success type and its named error types.
Business failures never travel as GraphQL errors. The client switches on
`__typename` and the compiler enforces exhaustiveness. `frontend/rules/repo-rules.md`
§7 is the other half of this contract.

**One error, one class pair, one file.** The Strawberry type and its exception
sit together in the domain's `graphql/errors.py`, and the exception carries
`gql_type`. There is no second hierarchy to keep in step.

`app/core/errors.py`

```python
class DomainError(Exception):
    """Base for every business failure. Never raised past @map_errors."""

    gql_type: ClassVar[type]

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

    def to_gql(self):
        names = {f.name for f in dataclasses.fields(self.gql_type)}
        return self.gql_type(**{n: getattr(self, n) for n in names})
```

`app/graphql/error_mapping.py`

```python
def map_errors(resolver):
    """Translate any DomainError into its union member."""

    @wraps(resolver)
    async def wrapper(*args, **kwargs):
        try:
            return await resolver(*args, **kwargs)
        except DomainError as exc:
            return exc.to_gql()

    return wrapper
```

Adding an error is therefore: one class pair in `graphql/errors.py`, one entry
in the union. Not four edits in three files.

**Reserved for the wire, not for business.** Authentication failure,
authorisation failure and an unhandled exception are GraphQL errors with an HTTP
status. Everything a user can legitimately cause is a union member.

## 9. Dependency injection

One composition root: `app/core/deps.py`. It holds a `build_*_interactor`
function per use case, and it is the only place a repository or an adapter is
constructed. It is also the one file allowed to import from more than one
domain, because wiring is its whole job.

```python
def build_create_record_interactor(ctx: Context) -> CreateRecordInteractor:
    return CreateRecordInteractor(
        record_repository=SqlRecordRepository(ctx.session),
        usage=GatewayUsageAdapter(GatewayUsageService(ctx.session)),
    )
```

Interactors take collaborators in `__init__`, typed as Protocols. Every
collaborator is typed. `radius` has an interactor whose `user_storage` parameter
carries no annotation and no interface, and it is the one collaborator nobody
can fake cleanly in a test.

**Resolvers never construct a repository inline.** `radius` uses a composition
root for its REST views and inline construction in its GraphQL resolvers. Two
wiring strategies in one repository means neither is enforced.

## 10. Row Level Security

Rule T2 of the tech stack, as a build rule.

1. **The `CREATE TABLE` migration enables RLS and adds the policy.** Same
   migration, same file. Not a follow-up.
2. **A table holding user data without a policy fails review.** Add a migration
   test that asserts `relrowsecurity` on every table in the user schema.
3. **The service-role connection bypasses every policy silently.** Rule T3. It
   is for migrations and background jobs. It never serves a user request.
4. **Identity must reach the connection or RLS does nothing.** The mechanism is
   open question T-Q2 of the tech stack and is not settled here. Whichever wins,
   it lives in `app/core/db.py` and nowhere else, and it is covered by the
   boundary test of rule T7.

RLS is the second lock, not the first. Resolvers and interactors still scope
every read by `user_id`. RLS is what catches the day one of them forgets.

## 11. Schema assembly

Each domain exports its own pieces:

```python
# app/domains/records/graphql/__init__.py
queries = RecordQueries
mutations = RecordMutations
subscriptions = None
```

`app/graphql/schema.py` composes the schema by iterating the domain list. It is
short, and it does not grow when a mutation is added.

**Never a hand-maintained import file.** `radius/schema.py` is 120 lines of
imports followed by 45 lines of field assignment, and every mutation is
registered in three places. A forgotten registration fails at runtime, not at
import.

## 12. Permissions

Every field declares a permission class. Authentication at the endpoint is not
authorisation.

```python
@strawberry.mutation(permission_classes=[IsAuthenticated])
@strawberry.mutation(permission_classes=[IsAdmin])
```

`radius` authenticates once in the view's `dispatch` and every resolver past it
trusts the caller. Its admin mutations, including user deletion, sit in the same
schema as user queries with no field-level check. Do not repeat this.

Ownership is checked in the interactor, not the permission class. A permission
class answers "may this kind of user call this field". An interactor answers
"does this user own this row".

## 13. Subscriptions

A subscription resolver lives in its domain's `graphql/subscriptions.py` and
follows the same layering: it calls an interactor, it holds no business rule.

The backplane for more than one API instance is open question T-Q3 of the tech
stack. Until it is answered, a subscription is correct on one instance and is
documented as such in the feature's build plan.

## 14. Background jobs

Procrastinate tasks live in the domain's `jobs.py` and are thin. A task
resolves its collaborators from `deps.py` and calls one interactor. Business
logic in a task body is misplaced, for the same reason it is misplaced in a
resolver.

Anything slow or third-party in a request path becomes a job: email, model
calls that are not user-facing, embedding generation, exports.

## 15. Testing

| Kind        | Location               | Against                                     | Covers                                      |
| ----------- | ---------------------- | ------------------------------------------- | ------------------------------------------- |
| Unit        | `tests/unit/<domain>/` | Interactors, with fakes from `tests/fakes/` | Every business rule and every raised error  |
| Integration | `tests/integration/`   | Resolver through to a real database         | The union mapping, permissions, RLS         |
| Boundary    | `tests/integration/`   | Resolver as user A requesting user B's row  | Rule T7. One per feature touching user data |

Fakes are in-memory Protocol implementations, not `unittest.mock.patch` chains.
This is only cheap because interactors take collaborators in `__init__`, which
is the practical payoff of §9.

**Every union member is tested.** An error type that no test produces is an
error type the frontend's exhaustiveness check will meet first in production.

## 16. Conventions

Types, keyword-only calls, interactor orchestration, storage purity, and
naming are owned by [`code-rules.md`](./code-rules.md). Do not restate them
here.

- **Docstrings on interactors** with `Raises:` listing every domain error. The
  union in the resolver must match it.
- **No magic values.** Limits, TTLs and defaults live in the domain's
  `constants.py`.
- **Functions under 30 lines, under 4 parameters.** More parameters means a DTO.
- **Imports** in order: stdlib, third party, first party. No wildcards.
- **Comments explain why.** A comment restating the line below it is deleted.
- **Never `except Exception: pass`.** A broad catch logs with
  `logger.exception` and says in a comment why it is broad.
- **Secrets come from `core/settings.py`.** Nothing else reads the environment.
  `.env.example` lists every variable with no values.
- **Never log** a token, a password, or prompt content. Rule T6 extends this:
  prompt content never reaches usage or analytics tables.

## 17. What we deliberately do not do

Each of these is a real failure in `~/projects/radius`, named so it is not
repeated by inheritance.

| Anti-pattern                                | What it cost                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Two parallel exception hierarchies          | `points/exceptions/custom_exceptions.py` and `points_graphql/exceptions/graphql_exceptions.py` declare near-identical classes. Every new error is two classes, one `except` clause, one union entry, in three files                                                                                                                                                                                     |
| Hand-written exception mapping per resolver | One `mutate()` carries ten `except` clauses. Adding an error means editing every resolver that can raise it                                                                                                                                                                                                                                                                                             |
| Manual schema registration                  | 165 lines of imports and assignments. A missed registration fails at runtime                                                                                                                                                                                                                                                                                                                            |
| Authentication as the only gate             | Admin deletion sits in the user schema with no field-level check                                                                                                                                                                                                                                                                                                                                        |
| Two dependency injection strategies         | A composition root for REST, inline construction for GraphQL. Neither is enforceable                                                                                                                                                                                                                                                                                                                    |
| An untyped collaborator                     | `user_storage` with no annotation and no Protocol. The one dependency that is awkward to fake                                                                                                                                                                                                                                                                                                           |
| Cross-domain imports                        | `radius` scaffolded `radius_core/adapters/notification_service/` and left it empty. It has 233 direct cross-domain imports instead, reaching concrete repositories (`reports` imports `points.storages.map_point_storage`), models (`radius_core` imports `iam.models`) and even another domain's presentation layer (`radius_core` imports `iam.iam_graphql` twenty times). §6 is the sanctioned route |
| Cyclic domain dependencies                  | `radius_core` imports `iam` 96 times and `iam` imports `radius_core` 6 times. `radius_core` and `notifications` do the same. Neither pair can be tested, deployed or reasoned about separately. §6.3                                                                                                                                                                                                    |
| `class BaseException`                       | Shadows the builtin in `points/exceptions/`                                                                                                                                                                                                                                                                                                                                                             |
| State in the repository root                | `db.sqlite3`, `dump.rdb`, `celerybeat-schedule`, `.env` and `.env.alpha` all committed or present                                                                                                                                                                                                                                                                                                       |

## 18. Open

Inherited from `process-docs/tech-stack.md` §7 and not answered here.

| #    | Question                                                    | Blocks                                         |
| ---- | ----------------------------------------------------------- | ---------------------------------------------- |
| T-Q2 | How identity reaches the database connection so RLS applies | The shape of `app/core/db.py`                  |
| T-Q3 | Subscription backplane for more than one instance           | `graphql/subscriptions.py` beyond one instance |
| T-Q4 | Query depth and complexity limits, as numbers               | A guard in `main.py` before public launch      |
| T-Q7 | One graph or a split schema as epics land                   | `graphql/schema.py` composition                |

One question this document raises on its own:

| #    | Question                                                                                                                                | Owner |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| B-Q1 | `process-docs/tech-stack.md` still names `apps/api` as the backend root. It needs updating to `backend/`, or this folder needs renaming | user  |
