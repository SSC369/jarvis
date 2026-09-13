"""The only SQL in the capture domain. Returns DTOs, never models."""

import uuid
from datetime import UTC, datetime
from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import user_transaction
from app.domains.capture.interfaces.dtos import MissingField, PendingCaptureDTO
from app.domains.capture.models import PendingCapture


class SqlPendingCaptureRepository:
    """Against the request's own session. See task_repository.py's docstring
    for why this differs from the gateway's own session-factory pattern."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_pending_capture(
        self,
        *,
        user_id: uuid.UUID,
        command_name: str,
        known_title: str | None,
        missing_field: MissingField,
        question_text: str,
        original_input: str,
    ) -> PendingCaptureDTO:
        now = datetime.now(UTC)
        pending_capture_id = uuid.uuid4()
        async with user_transaction(self.session, user_id) as scoped:
            scoped.add(
                PendingCapture(
                    id=pending_capture_id,
                    user_id=user_id,
                    command_name=command_name,
                    known_title=known_title,
                    missing_field=missing_field,
                    question_text=question_text,
                    original_input=original_input,
                    asked_at=now,
                )
            )
        return PendingCaptureDTO(
            id=pending_capture_id,
            user_id=user_id,
            command_name=command_name,
            known_title=known_title,
            missing_field=missing_field,
            question_text=question_text,
            original_input=original_input,
            asked_at=now,
        )

    async def get_pending_capture(
        self, *, user_id: uuid.UUID, pending_capture_id: uuid.UUID
    ) -> PendingCaptureDTO | None:
        async with user_transaction(self.session, user_id) as scoped:
            pending_capture = await scoped.get(PendingCapture, pending_capture_id)
            if pending_capture is None:
                return None
            return PendingCaptureDTO(
                id=pending_capture.id,
                user_id=pending_capture.user_id,
                command_name=pending_capture.command_name,
                known_title=pending_capture.known_title,
                missing_field=cast(MissingField, pending_capture.missing_field),
                question_text=pending_capture.question_text,
                original_input=pending_capture.original_input,
                asked_at=pending_capture.asked_at,
            )

    async def delete_pending_capture(
        self, *, user_id: uuid.UUID, pending_capture_id: uuid.UUID
    ) -> None:
        async with user_transaction(self.session, user_id) as scoped:
            pending_capture = await scoped.get(PendingCapture, pending_capture_id)
            if pending_capture is not None:
                await scoped.delete(pending_capture)
