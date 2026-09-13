"""The contract for pending-capture storage."""

from typing import Protocol
from uuid import UUID

from app.domains.capture.interfaces.dtos import MissingField, PendingCaptureDTO


class PendingCaptureRepository(Protocol):
    async def create_pending_capture(
        self,
        *,
        user_id: UUID,
        command_name: str,
        known_title: str | None,
        missing_field: MissingField,
        question_text: str,
        original_input: str,
    ) -> PendingCaptureDTO: ...

    async def get_pending_capture(
        self, *, user_id: UUID, pending_capture_id: UUID
    ) -> PendingCaptureDTO | None: ...

    async def delete_pending_capture(
        self, *, user_id: UUID, pending_capture_id: UUID
    ) -> None: ...
