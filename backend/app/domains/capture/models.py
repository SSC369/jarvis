"""SQLAlchemy tables for capture. Nothing else lives here."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base

MISSING_FIELDS = ("title", "due_at")


class PendingCapture(Base):
    """One unanswered question. FR-37: answerable at any later point, so this
    is a table, not a session or a cache entry, per build plan AD-2."""

    __tablename__ = "pending_captures"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    command_name: Mapped[str] = mapped_column(Text)
    known_title: Mapped[str | None] = mapped_column(Text)
    missing_field: Mapped[str] = mapped_column(
        Enum(*MISSING_FIELDS, name="pending_capture_missing_field", create_type=False)
    )
    question_text: Mapped[str] = mapped_column(Text)
    original_input: Mapped[str] = mapped_column(Text)
    asked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
