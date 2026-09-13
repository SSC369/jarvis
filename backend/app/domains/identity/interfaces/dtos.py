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
