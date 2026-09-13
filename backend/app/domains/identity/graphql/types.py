from datetime import datetime

import strawberry

from app.domains.identity.interfaces.dtos import SettingsDTO


@strawberry.type
class Settings:
    timezone: str
    updated_at: datetime


def settings_dto_to_type(*, settings: SettingsDTO) -> Settings:
    return Settings(timezone=settings.timezone, updated_at=settings.updated_at)
