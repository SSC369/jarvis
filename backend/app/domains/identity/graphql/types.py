from datetime import datetime

import strawberry

from app.domains.identity.interfaces.dtos import ProfileDTO, SettingsDTO


@strawberry.type
class Settings:
    timezone: str
    updated_at: datetime


def settings_dto_to_type(*, settings: SettingsDTO) -> Settings:
    return Settings(timezone=settings.timezone, updated_at=settings.updated_at)


@strawberry.type
class Me:
    id: strawberry.ID
    email: str
    username: str | None
    avatar_url: str | None


def profile_dto_to_type(*, profile: ProfileDTO, email: str) -> Me:
    return Me(
        id=strawberry.ID(str(profile.user_id)),
        email=email,
        username=profile.username,
        avatar_url=profile.avatar_url,
    )
