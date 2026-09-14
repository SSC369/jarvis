"""capture_turns: a log of every capture attempt, retained after its outcome.

Revision ID: 0006_capture_turns
Revises: 0005_user_settings
Create Date: 2026-09-14

Requirement FR-44: every capture turn stays available independent of whether
it produced a task, so this is an insert-only log, never updated or deleted,
distinct from pending_captures which is deleted once resolved (FR-37).
question_text and answer_text are captured onto this table directly rather
than read from pending_captures at display time, because that row would
already be gone for a resolved question (04.4 sub-plan section 4).

Rule T2: Row Level Security is enabled, forced, and given a policy in the
same migration that creates the table.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0006_capture_turns"
down_revision: str | None = "0005_user_settings"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None

CAPTURE_TURN_OUTCOMES = ("task_created", "question_asked", "discarded", "refused")


def upgrade() -> None:
    op.execute(
        sa.text(
            "CREATE TYPE capture_turn_outcome AS ENUM " + str(CAPTURE_TURN_OUTCOMES)
        )
    )

    op.create_table(
        "capture_turns",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("input_text", sa.Text(), nullable=False),
        sa.Column(
            "outcome",
            postgresql.ENUM(
                *CAPTURE_TURN_OUTCOMES,
                name="capture_turn_outcome",
                create_type=False,
            ),
            nullable=False,
        ),
        # No foreign keys on the two ids below: the row a resulting_task_id or
        # resulting_pending_capture_id points at is routinely deleted (a task
        # can be deleted, a pending capture always is on resolution), and this
        # table exists to survive exactly that. See repo-rules.md section 6.2.
        sa.Column("resulting_task_id", sa.Uuid(), nullable=True),
        sa.Column("resulting_pending_capture_id", sa.Uuid(), nullable=True),
        sa.Column("question_text", sa.Text(), nullable=True),
        sa.Column("answer_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
    )
    op.create_index(
        "ix_capture_turns_user_created",
        "capture_turns",
        ["user_id", "created_at", "id"],
    )

    _lock_down("capture_turns")


def downgrade() -> None:
    op.drop_table("capture_turns")
    op.execute(sa.text("DROP TYPE IF EXISTS capture_turn_outcome"))


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
