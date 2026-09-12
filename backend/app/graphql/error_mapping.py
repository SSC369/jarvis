"""Translate domain errors into union members.

Written once, here. A resolver never carries a ``try`` block for a business
failure. See backend/rules/repo-rules.md section 8.
"""

from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any

from app.core.errors import DomainError


def map_errors[R](
    resolver: Callable[..., Awaitable[R]],
) -> Callable[..., Awaitable[R | Any]]:
    """Return the union member for any ``DomainError`` the resolver raises."""

    @wraps(resolver)
    async def wrapper(*args: Any, **kwargs: Any) -> R | Any:
        try:
            return await resolver(*args, **kwargs)
        except DomainError as exc:
            return exc.to_gql()

    return wrapper
