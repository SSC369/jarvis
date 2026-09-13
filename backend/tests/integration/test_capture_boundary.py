"""Row Level Security boundary tests for capture's two tables.

Rule T7: a case where user A requests user B's row and receives nothing.
T-1.11 (tasks), T-1.12 (pending_captures). The standing guard in
test_rls_boundary.py's test_every_user_table_is_locked_down already proves
both tables have RLS enabled, forced and policied; these prove the policy
actually excludes another user's row, not just that one exists.
"""

import uuid
from datetime import UTC, datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.sql import text

from app.core.db import user_transaction

INSERT_TASK = text(
    "INSERT INTO tasks (id, user_id, title, status, origin, created_at, updated_at) "
    "VALUES (:id, :user_id, 'a task', 'pending', 'command', now(), now())"
)
COUNT_TASKS = text("SELECT count(*) FROM tasks")

INSERT_PENDING = text(
    "INSERT INTO pending_captures "
    "(id, user_id, command_name, missing_field, question_text, "
    "original_input, asked_at) "
    "VALUES (:id, :user_id, '/add-task', 'title', "
    "'What should the task be called?', '/add-task', :asked_at)"
)
COUNT_PENDING = text("SELECT count(*) FROM pending_captures")


@pytest.fixture
async def seeded_tasks(
    session_factory: async_sessionmaker[AsyncSession],
    two_users: tuple[uuid.UUID, uuid.UUID],
) -> tuple[uuid.UUID, uuid.UUID]:
    user_a, user_b = two_users
    for user_id in (user_a, user_b):
        async with (
            session_factory() as session,
            user_transaction(session, user_id) as s,
        ):
            await s.execute(INSERT_TASK, {"id": uuid.uuid4(), "user_id": user_id})
    return user_a, user_b


@pytest.fixture
async def seeded_pending_captures(
    session_factory: async_sessionmaker[AsyncSession],
    two_users: tuple[uuid.UUID, uuid.UUID],
) -> tuple[uuid.UUID, uuid.UUID]:
    user_a, user_b = two_users
    for user_id in (user_a, user_b):
        async with (
            session_factory() as session,
            user_transaction(session, user_id) as s,
        ):
            await s.execute(
                INSERT_PENDING,
                {"id": uuid.uuid4(), "user_id": user_id, "asked_at": datetime.now(UTC)},
            )
    return user_a, user_b


async def test_user_sees_only_their_own_tasks(
    session_factory: async_sessionmaker[AsyncSession],
    seeded_tasks: tuple[uuid.UUID, uuid.UUID],
) -> None:
    """T-1.11: user A's task is invisible to user B."""
    _user_a, user_b = seeded_tasks

    async with session_factory() as session, user_transaction(session, user_b) as s:
        visible = await s.scalar(COUNT_TASKS)

    assert visible == 1, f"user B saw {visible} task rows, so user A's task leaked"


async def test_user_sees_only_their_own_pending_captures(
    session_factory: async_sessionmaker[AsyncSession],
    seeded_pending_captures: tuple[uuid.UUID, uuid.UUID],
) -> None:
    """T-1.12: user A's pending capture is invisible to user B."""
    _user_a, user_b = seeded_pending_captures

    async with session_factory() as session, user_transaction(session, user_b) as s:
        visible = await s.scalar(COUNT_PENDING)

    assert visible == 1, (
        f"user B saw {visible} pending_captures rows, so user A's leaked"
    )
