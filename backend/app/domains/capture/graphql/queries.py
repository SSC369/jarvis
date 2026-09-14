"""Capture's one query: past capture turns, newest first. FR-44, FR-45."""

from typing import cast
from uuid import UUID

import strawberry
from strawberry.types import Info

from app.core.context import Context
from app.core.deps import build_list_capture_history_interactor
from app.domains.capture.graphql.types import (
    CaptureHistoryPage,
    capture_turn_dto_to_type,
)
from app.graphql.permissions import IsAuthenticated


@strawberry.type
class CaptureQueries:
    @strawberry.field(permission_classes=[IsAuthenticated])  # type: ignore[untyped-decorator]
    async def capture_history(
        self, info: Info, cursor: str | None = None, limit: int | None = None
    ) -> CaptureHistoryPage:
        context = cast(Context, info.context)
        user_id = cast(UUID, context.user_id)
        interactor = build_list_capture_history_interactor(context)
        page = await interactor.list_capture_history(
            user_id=user_id, cursor=cursor, limit=limit
        )
        return CaptureHistoryPage(
            items=[capture_turn_dto_to_type(turn=turn) for turn in page.items],
            next_cursor=page.next_cursor,
        )
