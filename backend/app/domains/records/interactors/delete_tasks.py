from app.domains.records.interactors.dtos import DeleteTasksInputDTO
from app.domains.records.interfaces.repositories import TaskRepository


class DeleteTasksInteractor:
    def __init__(self, *, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    async def delete_tasks(self, *, dto: DeleteTasksInputDTO) -> int:
        """Delete one or many tasks the caller owns. Ids not owned are ignored.

        Returns the number of rows actually deleted, which may be fewer than
        the number of ids supplied.
        """
        return await self.task_repository.delete_many(
            user_id=dto.user_id, task_ids=dto.task_ids
        )
