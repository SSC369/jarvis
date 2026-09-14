"""profiles: one row per user, a 1:1 extension of auth.users.

Revision ID: 0007_profiles
Revises: 0006_capture_turns
Create Date: 2026-09-14

Requirement FR-3: a username is unique ignoring case. `username` is nullable
(a Google-only account, added in slice 3, has none) and the uniqueness is
enforced by a case-insensitive expression index rather than a `UNIQUE`
column constraint, because a plain column constraint cannot lower() the
value first. A standard unique index already treats every NULL as distinct
from every other NULL, so this does not stop two profiles both having no
username.

The `handle_new_user()` trigger is what actually creates a profile: this
table is never written to from a request. FR-1, FR-2 rely on Supabase Auth
rolling the `auth.users` insert and this trigger's `profiles` insert back
together as one transaction, so a username collision here (raised by the
unique index) fails the whole signup and leaves no orphaned `auth.users` row.

Rule T2: Row Level Security is enabled, forced, and given a policy in the
same migration that creates the table. The key column is `id`, not
`user_id` — this is a 1:1 extension of the auth user, not an owned child
row — so the policy is written out directly rather than reusing the
`user_id`-shaped helper other migrations use.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0007_profiles"
down_revision: str | None = "0006_capture_turns"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "profiles",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("username", sa.Text(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["id"], ["auth.users.id"], ondelete="CASCADE"),
    )
    op.execute(
        sa.text(
            "CREATE UNIQUE INDEX ix_profiles_username_lower "
            "ON profiles (lower(username))"
        )
    )

    _lock_down()
    _create_handle_new_user_trigger()


def downgrade() -> None:
    op.execute(sa.text("DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users"))
    op.execute(sa.text("DROP FUNCTION IF EXISTS public.handle_new_user()"))
    op.drop_table("profiles")


def _lock_down() -> None:
    """Enable, force, grant and police. All four, or isolation does not bind.

    See 0001_ai_usage for why each of the four statements is required. The
    policy differs from that helper only in its key column: `id`, because
    `profiles` is keyed by the user's own id, not a `user_id` foreign key.
    """
    op.execute(sa.text("ALTER TABLE profiles ENABLE ROW LEVEL SECURITY"))
    op.execute(sa.text("ALTER TABLE profiles FORCE ROW LEVEL SECURITY"))
    op.execute(
        sa.text("GRANT SELECT, INSERT, UPDATE, DELETE ON profiles TO authenticated")
    )
    op.execute(
        sa.text(
            "CREATE POLICY profiles_own_rows ON profiles FOR ALL "
            "USING (id = NULLIF("
            "current_setting('request.jwt.claims', true)::jsonb ->> 'sub', ''"
            ")::uuid)"
        )
    )


def _create_handle_new_user_trigger() -> None:
    """Create one profile row the moment Supabase Auth inserts a user.

    `SECURITY DEFINER` runs the function as its owner (the migration role),
    which holds `rolbypassrls` on this database (see core/db.py's module
    docstring) — required because the row that inserts `auth.users` is
    Supabase Auth's own service role, not a caller with a `profiles` grant.
    `search_path` is pinned so a session-level search_path change cannot
    redirect `profiles` to another schema.
    """
    op.execute(
        sa.text(
            """
            CREATE OR REPLACE FUNCTION public.handle_new_user()
            RETURNS trigger
            LANGUAGE plpgsql
            SECURITY DEFINER
            SET search_path = public
            AS $$
            BEGIN
                INSERT INTO public.profiles (id, username, created_at)
                VALUES (
                    NEW.id,
                    NEW.raw_user_meta_data ->> 'username',
                    now()
                );
                RETURN NEW;
            END;
            $$;
            """
        )
    )
    op.execute(
        sa.text(
            "CREATE TRIGGER on_auth_user_created "
            "AFTER INSERT ON auth.users "
            "FOR EACH ROW EXECUTE FUNCTION public.handle_new_user()"
        )
    )
