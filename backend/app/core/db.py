"""Database engine, sessions, and the identity-bearing transaction.

The transaction helper in this module is the mechanism that makes Row Level
Security bind. Rule T2 of the tech stack makes isolation a database guarantee
rather than a code-review guarantee, and this is where that guarantee is
established. Read ``user_transaction`` before changing anything here.
"""

import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from uuid import UUID

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.sql import text

from app.core.settings import Settings

# The role the application acts as inside a request transaction. It does not
# carry rolbypassrls, which is the entire point. See the module docstring of
# user_transaction.
APPLICATION_ROLE = "authenticated"

_CLAIMS_SETTING = "request.jwt.claims"


def create_engine(settings: Settings) -> AsyncEngine:
    """Build the async engine.

    ``pool_pre_ping`` matters against a hosted database: a pooled connection can
    be closed by the far end between requests, and without it the next request
    inherits the corpse.
    """
    return create_async_engine(
        settings.async_database_url,
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_pool_max_overflow,
        pool_pre_ping=True,
        echo=False,
    )


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Build the session factory. One per process."""
    return async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


@asynccontextmanager
async def user_transaction(
    session: AsyncSession, user_id: UUID | None
) -> AsyncIterator[AsyncSession]:
    """Open a transaction that Row Level Security will actually police.

    Two statements are required, and both are mandatory. Running only the first
    leaks every row in every table, with no error.

    1. ``set_config('request.jwt.claims', ...)`` supplies the identity the
       policies read.
    2. ``SET LOCAL ROLE authenticated`` drops ``rolbypassrls``.

    The second is the one that is easy to miss and impossible to notice. The
    application connects as ``postgres``, which on Supabase is not a superuser
    but does carry ``rolbypassrls``. That privilege outranks
    ``FORCE ROW LEVEL SECURITY``, so without the role switch the policy is never
    evaluated and every query returns every user's rows. Measured against the
    live database on 2026-09-12; see sub-plan 04.2 section 6.

    Both statements are ``LOCAL``, so neither survives the transaction. A pooled
    connection cannot carry one user's identity, or the elevated role, into the
    next request.

    Passing ``user_id=None`` is legitimate and deliberate: the role switch still
    happens, the claim is empty, and every policy therefore matches nothing. The
    transaction fails closed rather than open.
    """
    claims = json.dumps({"sub": str(user_id)}) if user_id is not None else "{}"

    async with session.begin():
        await session.execute(
            text("SELECT set_config(:key, :claims, true)"),
            {"key": _CLAIMS_SETTING, "claims": claims},
        )
        # Not parameterisable: SET LOCAL ROLE takes an identifier, not a value.
        # APPLICATION_ROLE is a module constant and never caller input.
        await session.execute(text(f"SET LOCAL ROLE {APPLICATION_ROLE}"))
        yield session


async def check_connection(engine: AsyncEngine) -> bool:
    """Return whether the database answers. Used by the readiness check."""
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
    except Exception:
        return False
    return True
