from app.domains.records.graphql.errors import RecordNotFoundError
from app.domains.records.interactors.dtos import GetRecordDetailInputDTO
from app.domains.records.interfaces.dtos import TaskDTO
from app.domains.records.interfaces.repositories import TaskRepository


class GetRecordDetailInteractor:
    def __init__(self, *, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    async def get_record_detail(self, *, dto: GetRecordDetailInputDTO) -> TaskDTO:
        """Return one task the caller owns, with every field.

        Raises:
            RecordNotFoundError: no task with this id belongs to this user.
        """
        task = await self.task_repository.get_by_id(
            user_id=dto.user_id, task_id=dto.task_id
        )
        if task is None:
            raise RecordNotFoundError()
        return task
