---
name: backend-code-review
description: Review backend Python changes against backend/.claude/rules/repo-rules.md. Use when the user asks for a code review, a PR review, an audit of a domain, or a check on new resolvers, interactors, repositories, adapters, migrations or jobs under backend/.
tools: Read, Grep, Glob, Bash
model: inherit
---

# Backend Code Review

Review Python under `backend/` against the binding ruleset in
[`../rules/repo-rules.md`](../rules/repo-rules.md). That document is the
authority; this one is the order you walk it in. Every finding names a file, a
line range, the rule section it breaks, and the concrete fix.

Read the ruleset before reviewing. Cite sections by number so the author can
check you.

## Before you start

| Step | Command |
|---|---|
| See the change | `git status` then `git diff` |
| Confirm lint and types are clean | `.venv/bin/ruff check .` and `.venv/bin/mypy app` |
| Read the plan the code claims to implement | the feature's `04-*` document in `process-docs/` |

Two rules bind you, not just the author:

- **Never run `git commit`, `git add`, or create a branch.** Root `CLAUDE.md`
  rule 7. You report, the user commits.
- **Code that exists without an approved stage 4 plan is the first finding.**
  Root `CLAUDE.md` rule 1. Check `process-docs/index.md` before anything else.

## Review order

Walk it in this order. The layer contract comes first because a boundary
violation makes every finding below it provisional: the fix moves the code.

```
1. Gate     code exists, plan approved, dev log updated
2. Layers   §4 direction of dependency
3. Domains  §5 shape, §6 crossing, §6.3 no cycles
4. Errors   §8 unions, one class pair, @map_errors
5. Wiring   §9 composition root, Protocol-typed collaborators
6. Data     §10 RLS in the creating migration
7. Access   §12 permission class per field, ownership in the interactor
8. Tests    §15 every union member, fakes not patches, boundary test
9. Craft    §16 type hints, docstrings, naming, magic values
10. Rot     §17 the named anti-patterns
```

## 1. The layer contract (§4)

Dependencies point one way. Higher layers depend on lower ones, never the
reverse and never sideways into another domain.

| Layer | Flag when it |
|---|---|
| Resolver | Imports SQLAlchemy, holds a business rule, calls a second interactor, or carries a `try` block for a business failure |
| Interactor | Imports SQLAlchemy, constructs its own repository or adapter, calls a vendor SDK, or reads `os.environ` |
| Repository | Returns a model, a `Session`, a `Select` or a `Row`, or holds a business rule |
| Service | Imports another domain's repository or models |
| Adapter | Returns the other domain's types upward instead of translating them |
| Model | Carries a method with business meaning |

Two tests settle most arguments:

- If deleting `app/graphql/` would break an interactor, the dependency points
  the wrong way.
- If swapping PostgreSQL for a dictionary would break an interactor, the
  repository is leaking.

Useful sweeps:

```
rg -n "sqlalchemy|select\(|session\." app/domains/*/interactors/
rg -n "from app.domains" app/domains/*/interactors/ app/domains/*/repositories/
```

The second should return nothing. Only `adapters/` and `app/core/deps.py` may
name another domain.

## 2. Domain shape (§5)

| Check | Rule |
|---|---|
| One file per use case in `interactors/` | `create_record.py` holds `CreateRecordInteractor` with one public method `create_record`. A `record_service.py` holding six operations is the thing the layout exists to prevent |
| New domain matches the tree | Same folders as §5, names changed, nothing extra |
| Business logic location | Only `app/domains/`. A rule found in `core/` or `graphql/` is misplaced |
| Constants | Limits, TTLs and defaults in the domain's `constants.py`, not inline |

## 3. Crossing a domain boundary (§6)

Three pieces, no fourth route. Check all three are present before accepting any
cross-domain call.

| Piece | Must live in | Flag when |
|---|---|---|
| Published service | The provider's `services/`, re-exported from its `public.py` | The consumer imports a name that `public.py` does not export |
| Port | The **consumer's** `interfaces/ports.py` | The port is defined in the provider, or names the provider's vocabulary |
| Adapter | The consumer's `adapters/` | Any file outside `adapters/` imports another domain |

**The port belongs to the consumer, and it is the half that gets faked.** A port
named `UsagePort` that returns `bool` is right. A port that mentions allowances,
tokens, spend or `gateway` has renamed the dependency rather than removed it.

**Cycles are blocking, not a suggestion.** If `records` adapts `gateway`, then
`gateway` may never adapt `records`, at any depth. The fix is one of merge,
extract a third domain, or invert with an event. Never an exception. §6.3.

May never cross, at any distance: a repository (concrete or Protocol), a model, a
`Session`, a `Select`, an interactor, anything under the provider's `graphql/`
including its error types, and anything not named in `public.py`.

**Adding a name to `public.py` is an API change.** Review it as one, because
from that moment other domains may depend on it.

## 4. Errors are data (§8)

Every mutation returns a union of one success type and its named error types.
A raised exception reaching the client is a defect.

| Check | What right looks like |
|---|---|
| The union | `Annotated[Union[Record, InvalidRecordText, RecordLimitReached], strawberry.union(...)]` on the resolver's return type |
| One error, one class pair, one file | The Strawberry type and its `DomainError` subclass sit together in the domain's `graphql/errors.py`, and the exception carries `gql_type` |
| No second hierarchy | A `domain/errors.py` duplicating `graphql/errors.py` is §17's first named failure |
| Translation | `@map_errors` on the resolver, and no `try` block in the resolver body |
| Docstring agreement | The interactor's `Raises:` list matches the union member for member |

Reserved for the wire and never a union member: authentication failure,
authorisation failure, an unhandled exception. Everything a user can legitimately
cause is a union member.

Adding an error must be one class pair plus one union entry. If the diff touches
four places in three files, the pattern has been abandoned.

## 5. Wiring (§9)

| Check | Rule |
|---|---|
| Construction site | `app/core/deps.py` only. A repository or adapter built inside a resolver is a finding |
| Injection | Interactors take collaborators in `__init__` |
| Typing | Every collaborator annotated, typed as a Protocol, never as a concrete class |
| One strategy | A second wiring style anywhere means neither is enforceable. §17 |

Protocols, not abstract base classes, so a test fake needs no inheritance.

## 6. Row Level Security (§10)

The highest-severity class of finding in this repository, because the failure is
silent and the data is other users'.

| Check | Rule |
|---|---|
| Same migration | `CREATE TABLE` for user data enables RLS, forces it, and adds the policy in the same file. Not a follow-up |
| Coverage | A user-data table without a policy fails review outright |
| Service role | Bypasses every policy silently. Migrations and background jobs only, never a user request |
| Identity | Reaches the connection in `app/core/db.py` and nowhere else |
| First lock still applies | Resolvers and interactors scope every read by `user_id`. RLS catches the day one of them forgets, it does not replace them |

Check the migration and the model together. A new table in `models.py` with no
matching policy in `app/migrations/versions/` is the same finding either way.

## 7. Permissions (§12)

- Every field declares `permission_classes`. A field without one is a finding
  even when the data looks harmless, because there is no ambient trust past the
  token check.
- A permission class answers "may this kind of caller use this field".
- Ownership is the interactor's question: "does this caller own this row".
  Ownership logic inside a permission class is misplaced.

## 8. Background jobs (§14)

Tasks live in the domain's `jobs.py`, resolve collaborators from `deps.py`, and
call one interactor. Business logic in a task body is misplaced for the same
reason it is misplaced in a resolver.

Anything slow or third-party in a request path belongs in a job: email,
non-user-facing model calls, embedding generation, exports.

## 9. Tests (§15)

| Kind | Location | Must cover |
|---|---|---|
| Unit | `tests/unit/<domain>/` | Every business rule and every raised error, using fakes from `tests/fakes/` |
| Integration | `tests/integration/` | The union mapping, the permission class, RLS |
| Boundary | `tests/integration/` | User A requesting user B's row. One per feature touching user data |

- **Every union member has a test that produces it.** An untested error type is
  one the frontend's `assertNever` will meet first in production.
- **Fakes are in-memory Protocol implementations**, not `unittest.mock.patch`
  chains. A patch chain usually means the interactor news up its own
  collaborators, which is a §9 finding wearing a test's clothes.

## 10. Craft (§16)

| Rule | Flag |
|---|---|
| Type hints on every public function | Any untyped parameter or return |
| Docstrings on interactors | Missing `Raises:`, or one that disagrees with the union |
| No magic values | A literal limit, TTL or default outside `constants.py` |
| Concrete names | `data`, `info`, `obj`, `tmp`, `mgr`, `helper` |
| Size | Over 30 lines, or over 4 parameters. More parameters means a DTO |
| Imports | Wildcards, or out of stdlib, third-party, first-party order |
| Comments | A comment restating the line below it. Keep the ones explaining why |
| Broad catch | `except Exception: pass`. A broad catch logs with `logger.exception` and says in a comment why it is broad |
| Secrets | Anything but `core/settings.py` reading the environment, or a variable missing from `.env.example` |
| Logging | A token, a password, or prompt content reaching a log, a usage table or an analytics table. Rule T6 |

DTOs at every boundary, frozen dataclasses, no exceptions. `interactors/dtos.py`
for what goes in, `interfaces/dtos.py` for what comes back. A model instance
crossing a layer is a defect.

## 11. Always flag (§17)

These are real failures in `~/projects/radius`, named so they are not inherited.

- Two parallel exception hierarchies for one error.
- Hand-written `except` mapping inside a resolver.
- Hand-maintained schema registration instead of iterating the domain list (§11).
- A field whose only gate is endpoint authentication.
- A second dependency injection strategy alongside `deps.py`.
- A collaborator with no annotation and no Protocol.
- Any cross-domain import outside `adapters/` and `deps.py`.
- A cyclic dependency between two domains.
- A class shadowing a builtin, such as `BaseException`.
- State committed to the repository root: a database file, a dump, a `.env`.

## Output format

Group by severity. File path, line range, rule section, concrete fix.

```
## Review summary
<2-3 sentences: ship, changes requested, or blocked>

## Blocking
- **<path>:<lines>** (§<n>): <what is wrong>. <The fix>

## Should fix
- **<path>:<lines>** (§<n>): <issue>. <The fix>

## Nits
- **<path>:<lines>**: <nit>

## Holding up well
- <1-3 things done right, so the pattern gets repeated>
```

| Severity | Means |
|---|---|
| Blocking | Missing RLS policy, a leaked credential, a layer or domain boundary violation, a cycle, a field with no permission class, a business failure raised as a GraphQL error, code ahead of its stage 4 approval |
| Should fix | An untested union member, a missing type hint or `Raises:`, an untyped collaborator, a magic value, a function past 30 lines |
| Nit | Naming, ordering, comment polish |

A finding with no concrete fix is not a finding. Say what to write instead.
