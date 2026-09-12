"""ai_user_limit: the per-user ceiling on model calls.

Revision ID: 0002_ai_user_limit
Revises: 0001_ai_usage
Create Date: 2026-09-12

Requirement FR-10 says the limit changes without a code change or a deploy, so
it is a row rather than a constant. ``plan`` carries one value in V1, exactly as
the PRD said it would; it exists so the column does not have to be added later.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_ai_user_limit"
down_revision: str | None = "0001_ai_usage"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None

DEFAULT_REQUESTS_PER_DAY = 20


def upgrade() -> None:
    op.create_table(
        "ai_user_limit",
        sa.Column("user_id", sa.Uuid(), primary_key=True),
        sa.Column("plan", sa.Text(), nullable=False, server_default="free"),
        sa.Column(
            "requests_per_day",
            sa.Integer(),
            nullable=False,
            server_default=str(DEFAULT_REQUESTS_PER_DAY),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.CheckConstraint(
            "requests_per_day >= 0", name="ck_requests_per_day_non_negative"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
    )
    _lock_down("ai_user_limit")


def downgrade() -> None:
    op.drop_table("ai_user_limit")


def _lock_down(table: str) -> None:
    """See 0001_ai_usage for why all four statements are required."""
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
