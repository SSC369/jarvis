"""tasks: the first and only record type this epic ships.

Revision ID: 0003_tasks
Revises: 0002_ai_user_limit
Create Date: 2026-09-13

Requirement FR-43: overdue is computed at query time (build plan section 3),
never stored, so there is no column for it here.

Rule T2: Row Level Security is enabled, forced, and given a policy in the same
migration that creates the table.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0003_tasks"
down_revision: str | None = "0002_ai_user_limit"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None

TASK_STATUSES = ("pending", "done")
TASK_ORIGINS = ("command", "edit")


def upgrade() -> None:
    op.execute(sa.text("CREATE TYPE task_status AS ENUM " + str(TASK_STATUSES)))
    op.execute(sa.text("CREATE TYPE record_origin AS ENUM " + str(TASK_ORIGINS)))

    op.create_table(
        "tasks",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("due_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "status",
            postgresql.ENUM(*TASK_STATUSES, name="task_status", create_type=False),
            nullable=False,
        ),
        sa.Column(
            "origin",
            postgresql.ENUM(*TASK_ORIGINS, name="record_origin", create_type=False),
            nullable=False,
        ),
        sa.Column("original_input", sa.Text(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
    )

    # The records view lists a user's tasks, soonest due first (FR-25), and
    # /tasks does the same. Without this it is a sequential scan per call.
    op.create_index("ix_tasks_user_due", "tasks", ["user_id", "due_at"])

    _lock_down("tasks")


def downgrade() -> None:
    op.drop_index("ix_tasks_user_due", table_name="tasks")
    op.drop_table("tasks")
    op.execute(sa.text("DROP TYPE IF EXISTS task_status"))
    op.execute(sa.text("DROP TYPE IF EXISTS record_origin"))


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
