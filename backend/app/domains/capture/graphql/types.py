"""Capture's own success-shaped outcomes.

The five failure-shaped outcomes (UserLimitReached, ProviderUnavailable,
ProviderTimeout, SharedQuotaExhausted, MalformedResult) are not redefined
here: they cross from ``gateway.public`` directly, per build plan section 7
corrected 2026-09-13.
"""

import strawberry

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
