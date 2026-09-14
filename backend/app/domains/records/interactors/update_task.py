from app.domains.records.graphql.errors import (
    NoFieldsToUpdateError,
    RecordNotFoundError,
)
from app.domains.records.interactors.dtos import UpdateTaskInputDTO
from app.domains.records.interfaces.dtos import TaskDTO
from app.domains.records.interfaces.repositories import TaskRepository


class UpdateTaskInteractor:
    def __init__(self, *, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    async def update_task(self, *, dto: UpdateTaskInputDTO) -> TaskDTO:
        """Change the title, the status, the due date, or any combination, of
        one task the caller owns.

        Raises:
            NoFieldsToUpdateError: no field was supplied.
            RecordNotFoundError: no task with this id belongs to this user.
        """
        self._validate_has_a_field(
            title=dto.title, status=dto.status, due_at_provided=dto.due_at_provided
        )

        task = await self.task_repository.update(
            user_id=dto.user_id,
            task_id=dto.task_id,
            title=dto.title,
            status=dto.status,
            due_at=dto.due_at,
            due_at_provided=dto.due_at_provided,
        )
        if task is None:
            raise RecordNotFoundError()
        return task

    def _validate_has_a_field(
        self, *, title: str | None, status: str | None, due_at_provided: bool
    ) -> None:
        if title is None and status is None and not due_at_provided:
            raise NoFieldsToUpdateError()
