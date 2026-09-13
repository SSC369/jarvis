"""The records domain's published surface. Extended, not replaced, by slice 2.

Per repo-rules.md section 6: a domain's whole public surface may be one class
here, re-exported from ``public.py``, for a consumer to reach through its own
port and adapter.
"""

from datetime import datetime
from uuid import UUID

from app.domains.records.interfaces.dtos import RecordOrigin, TaskDTO
from app.domains.records.interfaces.repositories import TaskRepository


class RecordsService:
    def __init__(self, *, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    async def create_task(
        self,
        *,
        user_id: UUID,
        title: str,
        due_at: datetime | None,
        origin: RecordOrigin,
        original_input: str | None,
    ) -> TaskDTO:
        return await self.task_repository.create_task(
            user_id=user_id,
            title=title,
            due_at=due_at,
            origin=origin,
            original_input=original_input,
        )

    async def list_open_tasks(self, *, user_id: UUID) -> list[TaskDTO]:
        return await self.task_repository.list_open_tasks_for_user(user_id=user_id)
