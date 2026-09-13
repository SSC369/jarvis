"""Discard a pending capture. FR-37: ignoring it forever creates nothing, and
discarding it explicitly is the same outcome, sooner."""

from uuid import UUID

from app.domains.capture.interfaces.repositories import PendingCaptureRepository


class DiscardPendingCaptureInteractor:
    def __init__(self, *, pending_capture_repository: PendingCaptureRepository) -> None:
        self.pending_capture_repository = pending_capture_repository

    async def discard_pending_capture(
        self, *, user_id: UUID, pending_capture_id: UUID
    ) -> None:
        await self.pending_capture_repository.delete_pending_capture(
            user_id=user_id, pending_capture_id=pending_capture_id
        )
