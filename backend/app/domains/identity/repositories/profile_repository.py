"""The only SQL in identity that reads ``profiles``. Returns DTOs, never
models."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import user_transaction
from app.domains.identity.interfaces.dtos import ProfileDTO
from app.domains.identity.models import Profile


class SqlProfileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_for_user(self, *, user_id: UUID) -> ProfileDTO | None:
        async with user_transaction(self.session, user_id) as scoped:
            profile = await scoped.get(Profile, user_id)
        if profile is None:
            return None
        return _profile_to_dto(profile=profile)


def _profile_to_dto(*, profile: Profile) -> ProfileDTO:
    return ProfileDTO(
        user_id=profile.id,
        username=profile.username,
        avatar_url=profile.avatar_url,
        created_at=profile.created_at,
    )
