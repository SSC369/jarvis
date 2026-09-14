"""Capture's own success-shaped outcomes.

The five failure-shaped outcomes (UserLimitReached, ProviderUnavailable,
ProviderTimeout, SharedQuotaExhausted, MalformedResult) are not redefined
here: they cross from ``gateway.public`` directly, per build plan section 7
corrected 2026-09-13.
"""

from datetime import datetime
from enum import Enum

import strawberry

from app.domains.capture.interfaces.dtos import CaptureTurnDTO
from app.domains.records.public import Task


@strawberry.type
class TaskCreated:
    task: Task


@strawberry.type
class TasksListed:
    """`/tasks`. Its own outcome, not reused from a slice 2 query: this domain
    exists before slice 2's `tasks` GraphQL query does."""

    tasks: list[Task]


@strawberry.type
class PendingQuestionCreated:
    pending_capture_id: strawberry.ID
    question: str


@strawberry.type
class NonCommandGuidance:
    original_input: str


@strawberry.type
class UnrecognisedCommand:
    attempted_name: str
    closest_matches: list[str]


@strawberry.enum
class CaptureTurnOutcome(Enum):
    TASK_CREATED = "task_created"
    QUESTION_ASKED = "question_asked"
    DISCARDED = "discarded"
    REFUSED = "refused"


@strawberry.type
class CaptureTurn:
    id: strawberry.ID
    input_text: str
    outcome: CaptureTurnOutcome
    resulting_task_id: strawberry.ID | None
    resulting_pending_capture_id: strawberry.ID | None
    question_text: str | None
    answer_text: str | None
    created_at: datetime


@strawberry.type
class CaptureHistoryPage:
    items: list[CaptureTurn]
    next_cursor: str | None


def capture_turn_dto_to_type(*, turn: CaptureTurnDTO) -> CaptureTurn:
    return CaptureTurn(
        id=strawberry.ID(str(turn.id)),
        input_text=turn.input_text,
        outcome=CaptureTurnOutcome(turn.outcome),
        resulting_task_id=(
            strawberry.ID(str(turn.resulting_task_id))
            if turn.resulting_task_id
            else None
        ),
        resulting_pending_capture_id=(
            strawberry.ID(str(turn.resulting_pending_capture_id))
            if turn.resulting_pending_capture_id
            else None
        ),
        question_text=turn.question_text,
        answer_text=turn.answer_text,
        created_at=turn.created_at,
    )
