from typing import Annotated, cast
from uuid import UUID

import strawberry
from strawberry.types import Info

from app.core.context import Context
from app.core.deps import build_update_timezone_interactor
from app.domains.identity.graphql.errors import InvalidTimezone
from app.domains.identity.graphql.inputs import UpdateTimezoneInput
from app.domains.identity.graphql.types import Settings, settings_dto_to_type
from app.domains.identity.interactors.dtos import UpdateTimezoneInputDTO
from app.graphql.error_mapping import map_errors
from app.graphql.permissions import IsAuthenticated

UpdateTimezoneResult = Annotated[
    Settings | InvalidTimezone, strawberry.union("UpdateTimezoneResult")
]


@strawberry.type
class IdentityMutations:
    @strawberry.mutation(permission_classes=[IsAuthenticated])  # type: ignore[untyped-decorator]
    @map_errors
    async def update_timezone(
        self,
        info: Info,
        input_: Annotated[UpdateTimezoneInput, strawberry.argument(name="input")],
    ) -> UpdateTimezoneResult:
        context = cast(Context, info.context)
        user_id = cast(UUID, context.user_id)
        interactor = build_update_timezone_interactor(context)
        settings = await interactor.update_timezone(
            dto=UpdateTimezoneInputDTO(user_id=user_id, timezone=input_.timezone)
        )
        return cast(UpdateTimezoneResult, settings_dto_to_type(settings=settings))
