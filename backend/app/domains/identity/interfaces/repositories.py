from typing import Protocol
from uuid import UUID

from app.domains.identity.interfaces.dtos import SettingsDTO


class SettingsRepository(Protocol):
    async def get_for_user(self, *, user_id: UUID) -> SettingsDTO | None: ...

    async def upsert(self, *, user_id: UUID, timezone: str) -> SettingsDTO: ...
