"""Listing capture history, newest first. FR-44, FR-45. 04.4 sub-plan."""

import uuid

from app.domains.capture.constants import CAPTURE_HISTORY_PAGE_SIZE
from app.domains.capture.interactors.list_capture_history import (
    ListCaptureHistoryInteractor,
)
from tests.fakes.fake_capture_turn_repository import FakeCaptureTurnRepository


async def test_returns_pages_newest_first() -> None:
    """T-4.7."""
    turn_repo = FakeCaptureTurnRepository()
    user_id = uuid.uuid4()
    for index in range(3):
        await turn_repo.record_turn(
            user_id=user_id,
            input_text=f"/add-task {index}",
            outcome="task_created",
            resulting_task_id=uuid.uuid4(),
            resulting_pending_capture_id=None,
            question_text=None,
            answer_text=None,
        )
    interactor = ListCaptureHistoryInteractor(capture_turn_repository=turn_repo)

    page = await interactor.list_capture_history(user_id=user_id, cursor=None, limit=2)

    assert [turn.input_text for turn in page.items] == ["/add-task 2", "/add-task 1"]
    assert page.next_cursor is not None

    next_page = await interactor.list_capture_history(
        user_id=user_id, cursor=page.next_cursor, limit=2
    )
    assert [turn.input_text for turn in next_page.items] == ["/add-task 0"]
    assert next_page.next_cursor is None


async def test_limit_clamped_when_unset_or_over_page_size() -> None:
    """T-4.7."""
    turn_repo = FakeCaptureTurnRepository()
    user_id = uuid.uuid4()
    for index in range(CAPTURE_HISTORY_PAGE_SIZE + 5):
        await turn_repo.record_turn(
            user_id=user_id,
            input_text=f"/add-task {index}",
            outcome="task_created",
            resulting_task_id=uuid.uuid4(),
            resulting_pending_capture_id=None,
            question_text=None,
            answer_text=None,
        )
    interactor = ListCaptureHistoryInteractor(capture_turn_repository=turn_repo)

    unset = await interactor.list_capture_history(
        user_id=user_id, cursor=None, limit=None
    )
    over_page_size = await interactor.list_capture_history(
        user_id=user_id, cursor=None, limit=CAPTURE_HISTORY_PAGE_SIZE + 100
    )

    assert len(unset.items) == CAPTURE_HISTORY_PAGE_SIZE
    assert len(over_page_size.items) == CAPTURE_HISTORY_PAGE_SIZE


async def test_only_returns_the_requesting_users_turns() -> None:
    """FR-6 pattern, T7."""
    turn_repo = FakeCaptureTurnRepository()
    owner_id = uuid.uuid4()
    other_id = uuid.uuid4()
    await turn_repo.record_turn(
        user_id=owner_id,
        input_text="/add-task mine",
        outcome="task_created",
        resulting_task_id=uuid.uuid4(),
        resulting_pending_capture_id=None,
        question_text=None,
        answer_text=None,
    )
    await turn_repo.record_turn(
        user_id=other_id,
        input_text="/add-task theirs",
        outcome="task_created",
        resulting_task_id=uuid.uuid4(),
        resulting_pending_capture_id=None,
        question_text=None,
        answer_text=None,
    )
    interactor = ListCaptureHistoryInteractor(capture_turn_repository=turn_repo)

    page = await interactor.list_capture_history(
        user_id=owner_id, cursor=None, limit=10
    )

    assert [turn.input_text for turn in page.items] == ["/add-task mine"]
