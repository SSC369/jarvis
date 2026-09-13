"""Discarding a pending capture. FR-37."""

import uuid

from app.domains.capture.interactors.discard_pending_capture import (
    DiscardPendingCaptureInteractor,
)
from tests.fakes.fake_pending_capture_repository import FakePendingCaptureRepository


async def test_discarding_removes_it_without_creating_a_task() -> None:
    """T-1.8."""
    pending_repo = FakePendingCaptureRepository()
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
        pending_capture_repository=pending_repo
    )

    await interactor.discard_pending_capture(
        user_id=user_id, pending_capture_id=pending.id
    )

    assert pending.id not in pending_repo.rows
