from datetime import datetime
from typing import Protocol
from uuid import UUID

from app.domains.identity.interfaces.dtos import ProfileDTO, SettingsDTO


class SettingsRepository(Protocol):
    async def get_for_user(self, *, user_id: UUID) -> SettingsDTO | None: ...

    async def upsert(self, *, user_id: UUID, timezone: str) -> SettingsDTO: ...


class ProfileRepository(Protocol):
    async def get_for_user(self, *, user_id: UUID) -> ProfileDTO | None: ...


class AuthAccountRepository(Protocol):
    """Reaches ``auth.users`` directly, on the service-role connection only.

    Never scoped to one user: this is what the background sweep in
    ``jobs.py`` runs against, per rule T3. No other repository in this
    codebase talks to ``auth.users`` for writes.
    """

    async def delete_unverified_created_before(self, *, cutoff: datetime) -> int: ...
