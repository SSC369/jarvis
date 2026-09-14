"""Discard a pending capture. FR-37: ignoring it forever creates nothing, and
discarding it explicitly is the same outcome, sooner."""

from uuid import UUID

import structlog

from app.domains.capture.interfaces.dtos import PendingCaptureDTO
from app.domains.capture.interfaces.repositories import (
    CaptureTurnRepository,
    PendingCaptureRepository,
)

logger = structlog.get_logger(__name__)


class PendingCaptureNotFoundError(Exception):
    """Raised when the pending capture does not exist, or belongs to another
    user. Not a DomainError: there is no screen for this, since the frontend
    never holds an id it did not receive from its own account. Mapped to a
    plain GraphQL error by the resolver, not a union member.
    """


class DiscardPendingCaptureInteractor:
    def __init__(
        self,
        *,
        pending_capture_repository: PendingCaptureRepository,
        capture_turn_repository: CaptureTurnRepository,
    ) -> None:
        self.pending_capture_repository = pending_capture_repository
        self.capture_turn_repository = capture_turn_repository

    async def discard_pending_capture(
        self, *, user_id: UUID, pending_capture_id: UUID
    ) -> None:
        """Discard one pending capture.

        Raises:
            PendingCaptureNotFoundError: no such pending capture for this
                user. Fetched first, per FR-44, so its input and question
                text can be logged before the row is deleted.
        """
        pending_capture = await self.pending_capture_repository.get_pending_capture(
            user_id=user_id, pending_capture_id=pending_capture_id
        )
        if pending_capture is None:
            raise PendingCaptureNotFoundError()

        await self._record_turn(user_id=user_id, pending_capture=pending_capture)
        await self.pending_capture_repository.delete_pending_capture(
            user_id=user_id, pending_capture_id=pending_capture_id
        )

    async def _record_turn(
        self, *, user_id: UUID, pending_capture: PendingCaptureDTO
    ) -> None:
        """FR-44. A capture-turn write failure never blocks the discard:
        NFR-9's "no capture is lost" binds the task or question, not the log
        of it, per the 04.4 sub-plan section 9."""
        try:
            await self.capture_turn_repository.record_turn(
                user_id=user_id,
                input_text=pending_capture.original_input,
                outcome="discarded",
                resulting_task_id=None,
                resulting_pending_capture_id=pending_capture.id,
                question_text=pending_capture.question_text,
                answer_text=None,
            )
        except Exception:
            logger.exception("capture_turn.record_failed", user_id=str(user_id))
