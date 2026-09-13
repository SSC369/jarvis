import strawberry

from app.domains.records.graphql.types import SortField, TaskStatus


@strawberry.input
class RecordsFilterInput:
    kind: str | None = None
    search: str | None = None
    sort_by: SortField = SortField.CREATED_AT
    sort_desc: bool = False


@strawberry.input
class UpdateTaskInput:
    title: str | None = None
    status: TaskStatus | None = None
