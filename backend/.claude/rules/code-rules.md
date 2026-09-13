# Backend — Code Rules

How code is written line by line. [`repo-rules.md`](./repo-rules.md) owns where
code goes; this file owns what it looks like.

## 1. Types on every argument and return

Every parameter and every return value carries a type hint, including `self`-less
helpers and test fixtures. `mypy --strict` enforces it.

```python
# Bad
def count_since(self, user_id, since): ...

# Good
async def count_since(self, *, user_id: UUID, since: datetime) -> int: ...
```

## 2. Keyword arguments, always

Any function or method taking more than one argument besides `self` declares them
keyword-only with `*`, and every call site names them. A positional call breaks
silently when two arguments of the same type swap order.

```python
# Bad
await self._record(user_id, model, 0, 0, error, None)

# Good
await self._record_usage(
    user_id=user_id, model=model, input_tokens=0, output_tokens=0,
    error=error, latency_ms=None,
)
```

Exempt: single-argument calls, and third-party APIs that do not accept keywords.

## 3. Interactors validate first, then orchestrate

The public method reads as a list of steps. It holds no conditions of its own.

1. **Every validation is a private method** named `_validate_<what>`. It raises
   a `DomainError` or returns nothing.
2. **All validations run before any side effect.** No write, no provider call,
   no job enqueued until every check has passed.
3. **The public method only calls steps.** Validate, act, record, return.

```python
async def create_record(self, *, request: CreateRecordRequest) -> RecordDTO:
    self._validate_title(title=request.title)
    self._validate_body(body=request.body)
    await self._validate_record_limit(user_id=request.user_id)

    record = await self.record_repository.create_record(record=...)
    await self._publish_record_created(record=record)
    return record

def _validate_title(self, *, title: str) -> None:
    if not title.strip():
        raise InvalidRecordTextError(reason="title is empty")
```

## 4. Storage does database operations only

A repository method reads or writes rows and converts them to DTOs. It never
decides.

| Storage may | Storage may not |
|---|---|
| Filter by what the caller passed | Choose a default a business rule implies |
| Convert a model to a DTO | Compare a count against a limit |
| Raise when the database fails | Raise a `DomainError` |

```python
# Bad: the limit check is a business rule
async def can_create(self, *, user_id: UUID) -> bool:
    return await self._count(user_id=user_id) < MAX_RECORDS_PER_USER

# Good: storage counts, the interactor decides
async def count_records_for_user(self, *, user_id: UUID) -> int: ...
```

## 5. Names say what the thing does

A method name is a verb phrase that describes its effect without reading the
body. A private helper is named as specifically as a public one.

| Bad | Good |
|---|---|
| `_record` | `_record_usage` |
| `_usage` | `_read_token_count` |
| `limit_for` | `get_request_limit_for_user` |
| `handle` | `refuse_over_limit_request` |
| `process` | `extract_structured_task` |

A boolean reads as a question: `has_capacity`, `is_authenticated`.

## 6. Variable names from the domain

No single letters and no placeholders. Name a value for what it holds here.

| Bad | Good |
|---|---|
| `a`, `e`, `x`, `s`, `k`, `v` | `allowance`, `error`, `secret`, `field_name`, `field_value` |
| `this`, `that`, `obj`, `tmp` | `usage_record`, `previous_limit` |
| `data`, `value`, `res`, `ret` | `extracted_task`, `requests_per_day`, `usage_rows` |

Exempt: names a framework mandates, such as Strawberry's `info` and a public
field a caller already depends on. `_` for a deliberately unused value.

## Enforcement

| Rule | Checked by |
|---|---|
| 1 | `mypy --strict`, plus ruff `ANN` |
| 2 | `*` in signatures makes positional calls a `TypeError` and a mypy error |
| 3, 4 | `backend-code-review` agent, and review |
| 5 | Review |
| 6 | `tests/unit/test_code_rules.py`, which rejects banned names by AST |
