"""The two failure outcomes this slice adds, as union members and exceptions.

Both faces of an error live in this one file, per
backend/.claude/rules/repo-rules.md section 7.1 and 8.
"""

import strawberry

from app.core.errors import DomainError


@strawberry.type
class RecordNotFound:
    message: str


class RecordNotFoundError(DomainError):
    gql_type = RecordNotFound

    def __init__(self) -> None:
        super().__init__("No record with that id belongs to you")


@strawberry.type
class NoFieldsToUpdate:
    message: str


class NoFieldsToUpdateError(DomainError):
    gql_type = NoFieldsToUpdate

    def __init__(self) -> None:
        super().__init__("Nothing was supplied to change")
