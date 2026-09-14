"""Discarding a pending capture. FR-37."""

import uuid

import pytest

from app.domains.capture.interactors.discard_pending_capture import (
    DiscardPendingCaptureInteractor,
    PendingCaptureNotFoundError,
)
from tests.fakes.fake_capture_turn_repository import FakeCaptureTurnRepository
from tests.fakes.fake_pending_capture_repository import FakePendingCaptureRepository


async def test_discarding_removes_it_without_creating_a_task() -> None:
    """T-1.8. T-4.6: writes one discarded turn before deleting."""
    pending_repo = FakePendingCaptureRepository()
    turn_repo = FakeCaptureTurnRepository()
    user_id = uuid.uuid4()
    pending = await pending_repo.create_pending_capture(
        user_id=user_id,
        command_name="/add-task",
        known_title=None,
        missing_field="title",
        question_text="What should the task be called?",
        original_input="/add-task",
    )
    interactor = DiscardPendingCaptureInteractor(
        pending_capture_repository=pending_repo,
        capture_turn_repository=turn_repo,
    )

    await interactor.discard_pending_capture(
        user_id=user_id, pending_capture_id=pending.id
    )

    assert pending.id not in pending_repo.rows

    assert len(turn_repo.rows) == 1
    turn = turn_repo.rows[0]
    assert turn.outcome == "discarded"
    assert turn.resulting_pending_capture_id == pending.id
    assert turn.question_text == "What should the task be called?"
    assert turn.input_text == "/add-task"
    assert turn.resulting_task_id is None


async def test_discarding_a_pending_capture_that_does_not_exist_raises() -> None:
    interactor = DiscardPendingCaptureInteractor(
        pending_capture_repository=FakePendingCaptureRepository(),
        capture_turn_repository=FakeCaptureTurnRepository(),
    )

    with pytest.raises(PendingCaptureNotFoundError):
        await interactor.discard_pending_capture(
            user_id=uuid.uuid4(), pending_capture_id=uuid.uuid4()
        )
