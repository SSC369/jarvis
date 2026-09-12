"""The composition root.

The only place a repository, an adapter or a service is constructed, and the
only module allowed to import from more than one domain, because wiring is its
whole job. See backend/rules/repo-rules.md section 9.

Slice 2 wires nothing beyond the request context. Slice 3 adds the gateway.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.auth import extract_bearer_token, verify_token
from app.core.context import Context
from app.core.errors import AuthenticationError
from app.core.settings import Settings


async def build_context(
    authorization_header: str | None,
    request_id: str,
    session_factory: async_sessionmaker[AsyncSession],
    settings: Settings,
) -> Context:
    """Build the per-request context.

    An absent or unusable token produces a context with no identity rather than
    an error. Refusal is a field's decision, made by its permission class, so
    that a public field remains reachable without a token while every other
    field is closed by ``IsAuthenticated``.
    """
    user_id: uuid.UUID | None = None
    token = extract_bearer_token(authorization_header)
    if token is not None:
        try:
            user_id = verify_token(token, settings)
        except AuthenticationError:
            user_id = None

    return Context(
        user_id=user_id,
        session=session_factory(),
        request_id=request_id,
    )
