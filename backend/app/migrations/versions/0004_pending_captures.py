"""pending_captures: one unanswered question, until answered or discarded.

Revision ID: 0004_pending_captures
Revises: 0003_tasks
Create Date: 2026-09-13

Requirement FR-37: answerable "at any later point," so this survives a
restart and more than one instance, unlike a session or an in-memory cache
(build plan AD-2). No expiry column: build plan section 10 Q1, answered
"never" in V1.

Rule T2: Row Level Security is enabled, forced, and given a policy in the
same migration that creates the table.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0004_pending_captures"
down_revision: str | None = "0003_tasks"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None

MISSING_FIELDS = ("title", "due_at")


def upgrade() -> None:
    op.execute(
        sa.text(
            "CREATE TYPE pending_capture_missing_field AS ENUM " + str(MISSING_FIELDS)
        )
    )

    op.create_table(
        "pending_captures",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("command_name", sa.Text(), nullable=False),
        sa.Column("known_title", sa.Text(), nullable=True),
        sa.Column(
            "missing_field",
            postgresql.ENUM(
                *MISSING_FIELDS,
                name="pending_capture_missing_field",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("original_input", sa.Text(), nullable=False),
        sa.Column("asked_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
    )

    _lock_down("pending_captures")


def downgrade() -> None:
    op.drop_table("pending_captures")
    op.execute(sa.text("DROP TYPE IF EXISTS pending_capture_missing_field"))


def _lock_down(table: str) -> None:
    """Enable, force, grant and police. All four, or isolation does not bind.

    See 0001_ai_usage for why each of the four statements is required.
    """
    op.execute(sa.text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY"))
    op.execute(sa.text(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY"))
    op.execute(
        sa.text(f"GRANT SELECT, INSERT, UPDATE, DELETE ON {table} TO authenticated")
    )
    op.execute(
        sa.text(
            f"CREATE POLICY {table}_own_rows ON {table} FOR ALL "
            "USING (user_id = NULLIF("
            "current_setting('request.jwt.claims', true)::jsonb ->> 'sub', ''"
            ")::uuid)"
        )
    )
