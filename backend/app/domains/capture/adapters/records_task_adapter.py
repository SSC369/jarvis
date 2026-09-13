"""Implements capture's TaskCreationPort against the records domain."""

from datetime import datetime
from uuid import UUID

from app.domains.records.public import RecordsService, TaskDTO


class RecordsTaskAdapter:
    def __init__(self, *, records_service: RecordsService) -> None:
        self.records_service = records_service

    async def create_task(
        self,
        *,
        user_id: UUID,
        title: str,
        due_at: datetime | None,
        original_input: str,
    ) -> TaskDTO:
        return await self.records_service.create_task(
            user_id=user_id,
            title=title,
            due_at=due_at,
            origin="command",
            original_input=original_input,
        )

    async def list_open_tasks(self, *, user_id: UUID) -> list[TaskDTO]:
        return await self.records_service.list_open_tasks(user_id=user_id)
