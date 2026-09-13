from app.domains.identity.constants import DEFAULT_TIMEZONE
from app.domains.identity.interactors.dtos import GetSettingsInputDTO
from app.domains.identity.interfaces.dtos import SettingsDTO
from app.domains.identity.interfaces.repositories import SettingsRepository


class GetSettingsInteractor:
    def __init__(self, *, settings_repository: SettingsRepository) -> None:
        self.settings_repository = settings_repository

    async def get_settings(self, *, dto: GetSettingsInputDTO) -> SettingsDTO:
        """Return the caller's settings, creating them on first read.

        FR-28: a user with no row yet gets one created with the timezone their
        browser detected, so ``settings`` never returns nothing to render.
        """
        existing = await self.settings_repository.get_for_user(user_id=dto.user_id)
        if existing is not None:
            return existing
        return await self.settings_repository.upsert(
            user_id=dto.user_id, timezone=dto.detected_timezone or DEFAULT_TIMEZONE
        )
