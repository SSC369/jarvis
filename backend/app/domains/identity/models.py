"""SQLAlchemy tables for identity. Nothing else lives here.

The foreign key to ``auth.users`` is declared in the migration, not here, for
the same reason ``records.models`` does it that way (AD-9, no local mirror of
Supabase's ``auth`` schema).
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class UserSettings(Base):
    """One row per user. Created on first read, per FR-28."""

    __tablename__ = "user_settings"

    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    timezone: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
