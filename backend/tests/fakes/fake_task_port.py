"""An in-memory TaskPort. Not a mock: it behaves, so tests read as behaviour."""

import uuid
from datetime import UTC, datetime

from app.domains.records.public import TaskDTO


class FakeTaskPort:
    """Satisfies capture's TaskPort Protocol without inheriting from it."""

    def __init__(self) -> None:
        self.created_tasks: list[TaskDTO] = []

    async def create_task(
        self,
        *,
        user_id: uuid.UUID,
        title: str,
        due_at: datetime | None,
        original_input: str,
    ) -> TaskDTO:
        now = datetime.now(UTC)
        task = TaskDTO(
            id=uuid.uuid4(),
            user_id=user_id,
            title=title,
            due_at=due_at,
            status="pending",
            is_overdue=due_at is not None and due_at < now,
            origin="command",
            original_input=original_input,
            created_at=now,
            updated_at=now,
        )
        self.created_tasks.append(task)
        return task

    async def list_open_tasks(self, *, user_id: uuid.UUID) -> list[TaskDTO]:
        return [task for task in self.created_tasks if task.user_id == user_id]
