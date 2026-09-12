"""The GraphQL schema.

Slice 2 adds a field that proves identity reaches a resolver. Domains register
their own queries and mutations here as they land; this file never grows a
hand-maintained import list. See backend/rules/repo-rules.md section 10.
"""

from typing import cast

import strawberry
from strawberry.types import Info

from app.core.context import Context
from app.graphql.permissions import IsAuthenticated


@strawberry.type
class Query:
    """Root query. Domains extend this as they land."""

    @strawberry.field
    def api_version(self) -> str:
        """Public. A field exists so the schema is valid before any domain ships."""
        return "0.1.0"

    @strawberry.field(  # type: ignore[untyped-decorator]
        permission_classes=[IsAuthenticated]
    )
    def me(self, info: Info) -> str:
        """The caller's own id, proving a verified token reached a resolver.

        The ignore is on strawberry.field(permission_classes=...), which is
        untyped upstream. Removing it fails mypy strict, not the runtime.
        """
        context = cast(Context, info.context)
        # IsAuthenticated guarantees this; the check keeps mypy honest.
        if context.user_id is None:  # pragma: no cover
            raise RuntimeError("IsAuthenticated did not run")
        return str(context.user_id)


schema = strawberry.Schema(query=Query)
