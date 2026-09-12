"""The base for every business failure.

Business failures travel as typed data, never as exceptions on the wire. A
``DomainError`` raised inside an interactor is translated into a union member by
``app.graphql.error_mapping.map_errors``. See backend/rules/repo-rules.md
section 8.
"""

import dataclasses
from typing import Any, ClassVar


class DomainError(Exception):
    """A failure a user can legitimately cause.

    Subclasses declare ``gql_type``, the Strawberry type they translate into,
    and set any field that type declares as an attribute of the same name.

    Never raised past ``map_errors``. An exception reaching a client is a defect.
    """

    gql_type: ClassVar[type]

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

    def to_gql(self) -> Any:
        """Build the union member this error translates into."""
        names = {field.name for field in dataclasses.fields(self.gql_type)}
        return self.gql_type(**{name: getattr(self, name) for name in names})


class AuthenticationError(Exception):
    """A token was absent, malformed, expired, or not signed by the issuer.

    Deliberately not a ``DomainError``. Authentication failure is a transport
    concern that produces a GraphQL error, not a union member, because no
    resolver runs and there is no union to return.

    The message is always generic. Distinguishing expiry from a bad signature
    tells an attacker which half of a forged token to fix.
    """
