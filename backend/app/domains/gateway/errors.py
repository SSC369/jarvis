"""The six outcomes, as union members and as exceptions.

Both faces of an error live in this one file. There is no second hierarchy to
keep in step. See backend/.claude/rules/repo-rules.md section 8.

Requirement FR-18: a caller acts on the difference between these, so they are
six distinct types rather than one error with a string.
"""

from datetime import datetime
from typing import Annotated, Any

import strawberry

from app.core.errors import DomainError


@strawberry.type
class Extraction:
    """Success. The structured result the caller asked for."""

    data: strawberry.scalars.JSON
    model: str
    input_tokens: int
    output_tokens: int


@strawberry.type
class UserLimitReached:
    message: str
    limit: int
    resets_at: datetime


class UserLimitReachedError(DomainError):
    gql_type = UserLimitReached

    def __init__(self, limit: int, resets_at: datetime) -> None:
        self.limit = limit
        self.resets_at = resets_at
        super().__init__(f"Daily limit of {limit} reached")


@strawberry.type
class SharedQuotaExhausted:
    """The Slashit-wide provider quota, not this user's limit.

    Distinct from UserLimitReached because the user did nothing wrong and there
    is nothing they can do. Requirement FR-9.
    """

    message: str


class SharedQuotaExhaustedError(DomainError):
    gql_type = SharedQuotaExhausted

    def __init__(self) -> None:
        super().__init__("The service is temporarily at capacity")


@strawberry.type
class ProviderUnavailable:
    message: str


class ProviderUnavailableError(DomainError):
    gql_type = ProviderUnavailable

    def __init__(self, message: str = "The model provider is unavailable") -> None:
        super().__init__(message)


@strawberry.type
class ProviderTimeout:
    message: str
    budget_seconds: float


class ProviderTimeoutError(DomainError):
    gql_type = ProviderTimeout

    def __init__(self, budget_seconds: float) -> None:
        self.budget_seconds = budget_seconds
        super().__init__(f"The model did not answer within {budget_seconds} seconds")


@strawberry.type
class MalformedResult:
    message: str
    reason: str


class MalformedResultError(DomainError):
    gql_type = MalformedResult

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(f"The model returned an unusable result: {reason}")


ExtractionResult = Annotated[
    Extraction
    | UserLimitReached
    | SharedQuotaExhausted
    | ProviderUnavailable
    | ProviderTimeout
    | MalformedResult,
    strawberry.union("ExtractionResult"),
]

# Every outcome, for the tests that assert all six are covered.
ALL_ERROR_TYPES: tuple[type[Any], ...] = (
    UserLimitReachedError,
    SharedQuotaExhaustedError,
    ProviderUnavailableError,
    ProviderTimeoutError,
    MalformedResultError,
)
