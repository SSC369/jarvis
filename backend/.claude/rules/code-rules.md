---
doc: code-rules
scope: backend
title: Backend Coding Style
status: current
owner: user
created: 2026-09-12
updated: 2026-09-12
---

# Backend — Coding Style

How a method is written under `backend/`. Where code goes is owned by
[`repo-rules.md`](./repo-rules.md). This file owns types, call style, the
shape of an interactor method, storage purity, and names.

Read both before writing Python here.

## 1. Type every argument and return

Every parameter and every return value is annotated. That includes private
methods and `__init__`. Domain code does not use untyped `*args` or `**kwargs`.

This is repo-rules §16 tightened from public functions to every method.

Do:

```python
async def extract(
    self, *, user_id: UUID, request: ExtractionRequest
) -> ExtractionResult:
    ...

def __init__(
    self,
    *,
    provider: ModelProvider,
    usage_repository: UsageRepository,
) -> None:
    ...
```

Not:

```python
async def extract(self, user_id, request):
    ...
```

## 2. Call with keyword arguments

Project functions are keyword-only after `self`. The signature uses `*`. Call
sites pass names.

```python
def extract(
    self, *, user_id: UUID, request: ExtractionRequest
) -> ExtractionResult: ...

result = await interactor.extract(user_id=user_id, request=request)
await self._record_request(
    user_id=user_id,
    model=model,
    input_tokens=input_tokens,
    output_tokens=output_tokens,
    error=error,
    latency_ms=latency_ms,
)
```

Not:

```python
await self._record(user_id, model, 0, 0, error, elapsed_ms)
```

Exceptions: Python builtins (`len`, `str`, `cast`) and operators stay
positional. Collaborators passed into `__init__` are still keyword-only.

## 3. Interactor: validate first, then orchestrate

The public method is an orchestrator. It does not contain validation branches
inline.

Order inside the public method:

1. Run every validation. Each check is its own private method.
2. Perform the work: ports, services, repositories.
3. Persist or record outcomes if the use case requires it.
4. Return the result.

Each check is `_ensure_<thing>` or `_validate_<thing>`. It raises the matching
domain error, or returns the union member when that is the domain's existing
error style. One concern per method.

Do:

```python
async def create_record(self, *, dto: CreateRecordInputDTO) -> RecordDTO:
    self._validate_title(title=dto.title)
    self._validate_body(body=dto.body)
    await self._ensure_under_record_limit(user_id=dto.user_id)
    return await self.record_repository.create(dto=storage_dto)

def _validate_title(self, *, title: str) -> None:
    if not title.strip():
        raise InvalidRecordTextError(reason="empty_title")
```

Not:

```python
async def create_record(self, dto: CreateRecordInputDTO) -> RecordDTO:
    if not dto.title.strip():
        raise InvalidRecordTextError(reason="empty_title")
    if not dto.body.strip():
        raise InvalidRecordTextError(reason="empty_body")
    count = await self.record_repository.count_for_user(dto.user_id)
    if count >= MAX_RECORDS_PER_USER:
        raise RecordLimitReachedError(limit=MAX_RECORDS_PER_USER)
    return await self.record_repository.create(...)
```

## 4. Storage is SQL only

Repositories are this codebase's storage. They execute queries and map model to
DTO and back. They do not decide limits, outcomes, retries, or whether a call
counts. That stays in the interactor or a domain service.

The layer contract is repo-rules §4, Repository row, and §7.4. Restated here
so a storage method is not a place to hide a business rule.

Do:

```python
async def create(self, *, dto: CreateRecordStorageDTO) -> RecordDTO:
    record = Record(**asdict(dto))
    self.session.add(record)
    await self.session.flush()
    return record_model_to_dto(record)
```

Not:

```python
async def create(self, *, dto: CreateRecordStorageDTO) -> RecordDTO:
    count = await self.count_for_user(user_id=dto.user_id)
    if count >= MAX_RECORDS_PER_USER:
        raise RecordLimitReachedError(limit=MAX_RECORDS_PER_USER)
    ...
```

## 5. Names describe the action

A method name is a short verb phrase a new reader understands without opening
the body.

| Prefer | Over |
| ------ | ---- |
| `_record_usage` / `_record_request` | `_record` |
| `_ensure_user_has_capacity` | `_check` |
| `_validate_title` | `_ok` |

## 6. Variables are contextual, never placeholders

Ban `a`, `e`, `x`, `this`, `that`, `data`, `obj`, `tmp`, `val`, and `info`
except Strawberry's `info: Info`. Use names from the domain: `user_id`,
`allowance`, `usage_record`, `domain_error`. A loop variable names the item:
`for usage_row in usage_rows`.
