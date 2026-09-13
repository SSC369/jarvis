"""Data crossing capture's own boundaries. Frozen, never a model instance."""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID

MissingField = Literal["title", "due_at"]


@dataclass(frozen=True)
class PendingCaptureDTO:
    """One unanswered question, waiting on a missing field."""

    id: UUID
    user_id: UUID
    command_name: str
    known_title: str | None
    missing_field: MissingField
    question_text: str
    original_input: str
    asked_at: datetime


@dataclass(frozen=True)
class NonCommandGuidanceDTO:
    original_input: str


@dataclass(frozen=True)
class UnrecognisedCommandDTO:
    attempted_name: str
    closest_matches: list[str]
