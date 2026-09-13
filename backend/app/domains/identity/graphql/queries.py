from typing import cast
from uuid import UUID

import strawberry
from strawberry.types import Info

from app.core.context import Context
from app.core.deps import build_get_settings_interactor
from app.domains.identity.graphql.types import Settings, settings_dto_to_type
from app.domains.identity.interactors.dtos import GetSettingsInputDTO
from app.graphql.permissions import IsAuthenticated


@strawberry.type
class IdentityQueries:
    @strawberry.field(permission_classes=[IsAuthenticated])  # type: ignore[untyped-decorator]
    async def settings(
        self, info: Info, detected_timezone: str | None = None
    ) -> Settings:
        context = cast(Context, info.context)
        user_id = cast(UUID, context.user_id)
        interactor = build_get_settings_interactor(context)
        settings = await interactor.get_settings(
            dto=GetSettingsInputDTO(
                user_id=user_id, detected_timezone=detected_timezone
            )
        )
        return settings_dto_to_type(settings=settings)
