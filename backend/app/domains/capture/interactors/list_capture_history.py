"""List a user's capture history, newest first. FR-44, FR-45."""

from uuid import UUID

from app.domains.capture.constants import CAPTURE_HISTORY_PAGE_SIZE
from app.domains.capture.interfaces.dtos import CaptureHistoryPageDTO
from app.domains.capture.interfaces.repositories import CaptureTurnRepository


class ListCaptureHistoryInteractor:
    def __init__(self, *, capture_turn_repository: CaptureTurnRepository) -> None:
        self.capture_turn_repository = capture_turn_repository

    async def list_capture_history(
        self, *, user_id: UUID, cursor: str | None, limit: int | None
    ) -> CaptureHistoryPageDTO:
        page_size = self._clamp_limit(limit=limit)
        return await self.capture_turn_repository.list_turns_for_user(
            user_id=user_id, cursor=cursor, limit=page_size
        )

    def _clamp_limit(self, *, limit: int | None) -> int:
        if limit is None or limit <= 0 or limit > CAPTURE_HISTORY_PAGE_SIZE:
            return CAPTURE_HISTORY_PAGE_SIZE
        return limit
