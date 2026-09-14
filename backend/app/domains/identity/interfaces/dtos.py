"""Data crossing identity's boundaries. Frozen, never a model instance."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class SettingsDTO:
    user_id: UUID
    timezone: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class ProfileDTO:
    user_id: UUID
    username: str | None
    # FR-21: set only for a Google-created account whose provider gave one.
    avatar_url: str | None
    # None when no `profiles` row exists yet (GetProfileInteractor.get_profile
    # synthesizes this DTO rather than raising, per 04.1's T-1.5 acceptance
    # check: "`me` returns `username: null` for a user with no profile row").
    # Not exposed through GraphQL's `Me` type, so a missing value never reaches
    # the client; kept honest here rather than backfilled with `now()`.
    created_at: datetime | None
