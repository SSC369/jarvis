"""Backs both the `records` and `tasks` queries. See 04.2-records-and-settings.md."""

from app.domains.records.interactors.dtos import ListTasksInputDTO
from app.domains.records.interfaces.dtos import TaskDTO
from app.domains.records.interfaces.repositories import TaskRepository


class ListTasksInteractor:
    def __init__(self, *, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    async def list_tasks(self, *, dto: ListTasksInputDTO) -> list[TaskDTO]:
        """List the caller's tasks, filtered, searched and sorted."""
        return await self.task_repository.list_for_user(
            user_id=dto.user_id,
            kind_filter=dto.kind_filter,
            search=dto.search,
            sort_by=dto.sort_by,
            sort_desc=dto.sort_desc,
        )
