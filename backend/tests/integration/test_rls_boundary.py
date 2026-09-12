"""Row Level Security boundary tests.

These are the tests rule T7 requires: a case where user A requests user B's
record and receives nothing.

T-2.7 is the one that matters. It is negative, and it is the only case here that
distinguishes "the policy ran and excluded rows" from "the policy never ran". A
positive test passes under the leaking configuration, because a user querying
their own row gets that row whether or not the policy is evaluated.
"""

import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.sql import text

from app.core.db import user_transaction

INSERT_USAGE = text(
    "INSERT INTO ai_usage (id, user_id, provider, model, outcome) "
    "VALUES (:id, :user_id, 'gemini', 'gemini-2.5-flash', 'success')"
)
COUNT_USAGE = text("SELECT count(*) FROM ai_usage")


async def _insert_for(
    factory: async_sessionmaker[AsyncSession], user_id: uuid.UUID
) -> None:
    async with factory() as session, user_transaction(session, user_id) as s:
        await s.execute(INSERT_USAGE, {"id": uuid.uuid4(), "user_id": user_id})


@pytest.fixture
async def seeded(
    session_factory: async_sessionmaker[AsyncSession],
    two_users: tuple[uuid.UUID, uuid.UUID],
) -> tuple[uuid.UUID, uuid.UUID]:
    """One usage row for each of two users."""
    user_a, user_b = two_users
    await _insert_for(session_factory, user_a)
    await _insert_for(session_factory, user_b)
    return user_a, user_b


async def test_user_sees_only_their_own_rows(
    session_factory: async_sessionmaker[AsyncSession],
    seeded: tuple[uuid.UUID, uuid.UUID],
) -> None:
    """T-2.6: user B cannot see user A's usage."""
    _user_a, user_b = seeded

    async with session_factory() as session, user_transaction(session, user_b) as s:
        visible = await s.scalar(COUNT_USAGE)

    assert visible == 1, f"user B saw {visible} rows, so user A's row leaked"


async def test_no_identity_sees_nothing(
    session_factory: async_sessionmaker[AsyncSession],
    seeded: tuple[uuid.UUID, uuid.UUID],
) -> None:
    """T-2.7: with no claim, the query returns zero rows, not every row.

    This is the case that catches a missing role switch. Without
    SET LOCAL ROLE authenticated the connecting role keeps rolbypassrls, the
    policy is never evaluated, and this returns every row in the table.
    """
    async with session_factory() as session, user_transaction(session, None) as s:
        visible = await s.scalar(COUNT_USAGE)

    assert visible == 0, (
        f"no-identity transaction saw {visible} rows. "
        "Row Level Security is not binding: check SET LOCAL ROLE in user_transaction."
    )


async def test_identity_does_not_survive_the_transaction(
    session_factory: async_sessionmaker[AsyncSession],
    two_users: tuple[uuid.UUID, uuid.UUID],
) -> None:
    """T-2.8: a pooled connection cannot carry identity or role forward."""
    user_a, _user_b = two_users

    async with session_factory() as session:
        async with user_transaction(session, user_a):
            pass
        role = await session.scalar(text("SELECT current_user"))
        claims = await session.scalar(
            text("SELECT current_setting('request.jwt.claims', true)")
        )

    assert role == "postgres", f"role leaked out of the transaction as {role}"
    assert not claims, f"claims leaked out of the transaction as {claims!r}"


async def test_every_user_table_is_locked_down(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """T-2.9: rule T2 as a standing guard.

    Fails the day someone adds a table holding user data without a policy, which
    is exactly how T2 erodes. alembic_version is excluded: it holds no user data.
    """
    query = text(
        "SELECT c.relname, c.relrowsecurity, c.relforcerowsecurity, "
        "  (SELECT count(*) FROM pg_policy p WHERE p.polrelid = c.oid) AS policies "
        "FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace "
        "WHERE n.nspname = 'public' AND c.relkind = 'r' "
        "  AND c.relname <> 'alembic_version'"
    )
    async with session_factory() as session:
        rows = (await session.execute(query)).all()

    assert rows, "no application tables found; migrations may not have run"
    for name, enabled, forced, policies in rows:
        assert enabled, f"{name} does not have row level security enabled"
        assert forced, (
            f"{name} does not force row level security, so its owner bypasses it"
        )
        assert policies > 0, (
            f"{name} has row level security but no policy, so it denies everything"
        )
