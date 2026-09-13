"""Editing a task's title and status. FR-19, FR-22, and the error table."""

import uuid

import pytest

from app.domains.records.graphql.errors import (
    NoFieldsToUpdateError,
    RecordNotFoundError,
)
from app.domains.records.interactors.dtos import UpdateTaskInputDTO
from app.domains.records.interactors.update_task import UpdateTaskInteractor
from tests.fakes.fake_task_repository import FakeTaskRepository


async def test_updates_title_leaves_due_at_untouched_and_bumps_updated_at() -> None:
    """T-2.6."""
    user_id = uuid.uuid4()
    repository = FakeTaskRepository()
    created = await repository.create_task(
        user_id=user_id,
        title="Finish API docs",
        due_at=None,
        origin="command",
        original_input=None,
    )
    interactor = UpdateTaskInteractor(task_repository=repository)

    updated = await interactor.update_task(
        dto=UpdateTaskInputDTO(
            user_id=user_id,
            task_id=created.id,
            title="Finish the API docs",
            status=None,
        )
    )

    assert updated.title == "Finish the API docs"
    assert updated.due_at == created.due_at
    assert updated.status == "pending"
    assert updated.updated_at > created.updated_at


async def test_neither_field_raises_no_fields_to_update() -> None:
    """T-2.7."""
    user_id = uuid.uuid4()
    repository = FakeTaskRepository()
    created = await repository.create_task(
        user_id=user_id,
        title="Finish API docs",
        due_at=None,
        origin="command",
        original_input=None,
    )
    interactor = UpdateTaskInteractor(task_repository=repository)

    with pytest.raises(NoFieldsToUpdateError):
        await interactor.update_task(
            dto=UpdateTaskInputDTO(
                user_id=user_id, task_id=created.id, title=None, status=None
            )
        )


async def test_missing_task_raises_not_found() -> None:
    user_id = uuid.uuid4()
    repository = FakeTaskRepository()
    interactor = UpdateTaskInteractor(task_repository=repository)

    with pytest.raises(RecordNotFoundError):
        await interactor.update_task(
            dto=UpdateTaskInputDTO(
                user_id=user_id, task_id=uuid.uuid4(), title="New title", status=None
            )
        )


async def test_cannot_update_another_users_task() -> None:
    owner_id = uuid.uuid4()
    other_user_id = uuid.uuid4()
    repository = FakeTaskRepository()
    created = await repository.create_task(
        user_id=owner_id,
        title="Finish API docs",
        due_at=None,
        origin="command",
        original_input=None,
    )
    interactor = UpdateTaskInteractor(task_repository=repository)

    with pytest.raises(RecordNotFoundError):
        await interactor.update_task(
            dto=UpdateTaskInputDTO(
                user_id=other_user_id, task_id=created.id, title="Hijacked", status=None
            )
        )
