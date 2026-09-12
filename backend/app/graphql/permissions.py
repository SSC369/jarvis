"""Field-level permissions.

Authentication at the endpoint is not authorisation. Every field declares what
it requires, so there is no ambient trust once a token has been checked. See
backend/rules/repo-rules.md section 12.

A permission class answers "may this kind of caller use this field". Whether a
caller owns a particular row is an interactor's question, not this one's.
"""

from typing import Any

from strawberry import BasePermission
from strawberry.types import Info

from app.core.context import Context


class IsAuthenticated(BasePermission):
    """Require a verified identity on the request."""

    message = "Not authenticated"

    def has_permission(self, source: Any, info: Info, **kwargs: Any) -> bool:
        context: Context = info.context
        return context.is_authenticated
