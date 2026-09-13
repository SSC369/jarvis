"""Answer a pending capture, whenever the user gets to it. FR-37, FR-38."""

from datetime import datetime
from typing import Any, cast
from uuid import UUID

from app.domains.capture.constants import DUE_AT_ONLY_INSTRUCTION, DUE_AT_ONLY_SCHEMA
from app.domains.capture.interfaces.ports import ExtractionPort, TaskPort
from app.domains.capture.interfaces.repositories import PendingCaptureRepository
from app.domains.gateway.public import Extraction
from app.domains.records.public import TaskDTO


class PendingCaptureNotFoundError(Exception):
    """Raised when the pending capture does not exist, or belongs to another
    user. Not a DomainError: there is no screen for this, since the frontend
    never holds an id it did not receive from its own account. Mapped to a
    plain GraphQL error by the resolver, not a union member.
    """


class AnswerCouldNotBeUnderstoodError(Exception):
    """The answer did not resolve to what the question asked for."""


class AnswerPendingCaptureInteractor:
    def __init__(
        self,
        *,
        pending_capture_repository: PendingCaptureRepository,
        task_port: TaskPort,
        extraction: ExtractionPort,
    ) -> None:
        self.pending_capture_repository = pending_capture_repository
        self.task_port = task_port
        self.extraction = extraction

    async def answer_pending_capture(
        self, *, user_id: UUID, pending_capture_id: UUID, answer: str
    ) -> TaskDTO:
        """Resolve a pending capture with the user's answer, creating the task.

        Raises:
            PendingCaptureNotFoundError: no such pending capture for this user.
            ValueError: the answer is empty.
            AnswerCouldNotBeUnderstoodError: a due-date answer that the model
                could not resolve to a date, per FR-38's own reference moment.
        """
        pending_capture = await self.pending_capture_repository.get_pending_capture(
            user_id=user_id, pending_capture_id=pending_capture_id
        )
        if pending_capture is None:
            raise PendingCaptureNotFoundError()

        answer_text = answer.strip()
        if not answer_text:
            raise ValueError("answer is empty")

        if pending_capture.missing_field == "title":
            title = answer_text
            due_at = None
        else:
            title = pending_capture.known_title or answer_text
            due_at = await self._resolve_due_at(
                user_id=user_id, answer_text=answer_text
            )
            if due_at is None:
                raise AnswerCouldNotBeUnderstoodError()

        task = await self.task_port.create_task(
            user_id=user_id,
            title=title,
            due_at=due_at,
            # FR-38: the answer resolves against the moment the original
            # capture was made, not the moment it was answered.
            original_input=pending_capture.original_input,
        )
        await self.pending_capture_repository.delete_pending_capture(
            user_id=user_id, pending_capture_id=pending_capture_id
        )
        return task

    async def _resolve_due_at(
        self, *, user_id: UUID, answer_text: str
    ) -> datetime | None:
        """Resolve a free-text due-date answer ("Friday", "tomorrow") through
        the same gateway extraction path capture itself uses, rather than a
        second date-parsing dependency this domain would otherwise need.
        """
        result = await self.extraction.extract(
            user_id=user_id,
            prompt=answer_text,
            schema=DUE_AT_ONLY_SCHEMA,
            instruction=DUE_AT_ONLY_INSTRUCTION,
        )
        if not isinstance(result, Extraction):
            return None
        raw_due_at = cast(dict[str, Any], result.data).get("due_at")
        if not isinstance(raw_due_at, str) or not raw_due_at:
            return None
        try:
            return datetime.fromisoformat(raw_due_at)
        except ValueError:
            return None
