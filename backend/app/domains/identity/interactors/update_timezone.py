from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from app.domains.identity.graphql.errors import InvalidTimezoneError
from app.domains.identity.interactors.dtos import UpdateTimezoneInputDTO
from app.domains.identity.interfaces.dtos import SettingsDTO
from app.domains.identity.interfaces.repositories import SettingsRepository


class UpdateTimezoneInteractor:
    def __init__(self, *, settings_repository: SettingsRepository) -> None:
        self.settings_repository = settings_repository

    async def update_timezone(self, *, dto: UpdateTimezoneInputDTO) -> SettingsDTO:
        """Change the caller's stored timezone.

        Raises:
            InvalidTimezoneError: the string is not a real IANA zone.
        """
        self._validate_timezone(timezone=dto.timezone)
        return await self.settings_repository.upsert(
            user_id=dto.user_id, timezone=dto.timezone
        )

    def _validate_timezone(self, *, timezone: str) -> None:
        try:
            ZoneInfo(timezone)
        except (ZoneInfoNotFoundError, ValueError) as error:
            raise InvalidTimezoneError(timezone=timezone) from error
