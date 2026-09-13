"""The one failure this domain has, as a union member and an exception."""

import strawberry

from app.core.errors import DomainError


@strawberry.type
class InvalidTimezone:
    message: str


class InvalidTimezoneError(DomainError):
    gql_type = InvalidTimezone

    def __init__(self, *, timezone: str) -> None:
        super().__init__(f'"{timezone}" is not a known timezone')
