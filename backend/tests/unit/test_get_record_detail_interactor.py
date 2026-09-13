"""One task's full detail. FR-18, FR-22."""

import uuid

import pytest

from app.domains.records.graphql.errors import RecordNotFoundError
from app.domains.records.interactors.dtos import GetRecordDetailInputDTO
from app.domains.records.interactors.get_record_detail import GetRecordDetailInteractor
from tests.fakes.fake_task_repository import FakeTaskRepository


async def test_returns_origin_and_original_input_unchanged_from_creation() -> None:
    """T-2.5."""
    user_id = uuid.uuid4()
    repository = FakeTaskRepository()
    created = await repository.create_task(
        user_id=user_id,
        title="Finish API docs",
        due_at=None,
        origin="command",
        original_input="/add-task Finish API docs",
    )
    interactor = GetRecordDetailInteractor(task_repository=repository)

    detail = await interactor.get_record_detail(
        dto=GetRecordDetailInputDTO(user_id=user_id, task_id=created.id)
    )

    assert detail.origin == "command"
    assert detail.original_input == "/add-task Finish API docs"


async def test_raises_not_found_for_a_missing_task() -> None:
    user_id = uuid.uuid4()
    repository = FakeTaskRepository()
    interactor = GetRecordDetailInteractor(task_repository=repository)

    with pytest.raises(RecordNotFoundError):
        await interactor.get_record_detail(
            dto=GetRecordDetailInputDTO(user_id=user_id, task_id=uuid.uuid4())
        )
