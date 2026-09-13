"""Records' own GraphQL types.

`Task` is not redefined here: it already lives in `interfaces/dtos.py`, placed
there in slice 1 so it may cross into `capture` per repo-rules.md section 6.2.
Redeclaring it here would give the schema two incompatible `Task` types.
"""

from enum import Enum

import strawberry


@strawberry.enum
class TaskStatus(Enum):
    PENDING = "pending"
    DONE = "done"


@strawberry.enum
class RecordOrigin(Enum):
    COMMAND = "command"
    EDIT = "edit"


@strawberry.enum
class SortField(Enum):
    CREATED_AT = "CREATED_AT"
    DUE_AT = "DUE_AT"
