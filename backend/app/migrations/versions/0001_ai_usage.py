"""ai_usage: one row per model call, counts only.

Revision ID: 0001_ai_usage
Revises:
Create Date: 2026-09-12

Requirement FR-11 records what a call cost in tokens. FR-12 forbids prompt or
response content from ever reaching this table, and the schema enforces that by
having no column that could hold it.

Rule T2: Row Level Security is enabled, forced, and given a policy in the same
migration that creates the table.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_ai_usage"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None

OUTCOMES = (
    "success",
    "user_limit_reached",
    "shared_quota_exhausted",
    "provider_unavailable",
    "provider_timeout",
    "malformed_result",
)


def upgrade() -> None:
    op.execute(sa.text("CREATE TYPE ai_call_outcome AS ENUM " + str(OUTCOMES)))

    op.create_table(
        "ai_usage",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("provider", sa.Text(), nullable=False),
        sa.Column("model", sa.Text(), nullable=False),
        sa.Column("input_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("output_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "estimated_cost_usd", sa.Numeric(12, 8), nullable=False, server_default="0"
        ),
        sa.Column(
            "outcome",
            # postgresql.ENUM, not sa.Enum: only the dialect type honours
            # create_type=False. sa.Enum re-issues CREATE TYPE inside
            # create_table and collides with the statement above.
            postgresql.ENUM(*OUTCOMES, name="ai_call_outcome", create_type=False),
            nullable=False,
        ),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        # Identity lives only in auth.users. There is no mirrored users table,
        # per decision AD-9, so nothing can drift out of step.
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
    )

    # The allowance check counts a user's calls in a window. Without this it is
    # a sequential scan on every model call.
    op.create_index("ix_ai_usage_user_created", "ai_usage", ["user_id", "created_at"])

    _lock_down("ai_usage")


def downgrade() -> None:
    op.drop_index("ix_ai_usage_user_created", table_name="ai_usage")
    op.drop_table("ai_usage")
    op.execute(sa.text("DROP TYPE IF EXISTS ai_call_outcome"))


def _lock_down(table: str) -> None:
    """Enable, force, grant and police. All four, or isolation does not bind.

    FORCE is required because the connecting role owns the table and an owner is
    otherwise exempt. The GRANT is required because the application switches to
    ``authenticated`` inside every request transaction, and that role holds only
    what it is granted. Omitting the grant produces a permission error, which is
    the right failure: loud, not silent.
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
