"""handle_new_user(): generate a username for a Google signup instead of
leaving the row without one.

Revision ID: 0010_google_username_fallback
Revises: 0009_auth_hooks
Create Date: 2026-09-15

Google never sends a `username` in `raw_user_meta_data` (it has no such
field to send), so every Google signup hit 0007_profiles.py's trigger with
a null username. This replaces `handle_new_user()` so that a null username
is generated instead: `'user_' || substr(NEW.id::text, 1, 8)`.

`auth.users.id` is a UUID, so a prefix collision across two different users
is not a realistic risk at V1's scale (04.3-google-sign-in.md §5); the
substring is not separately unique-checked here, only the existing
case-insensitive expression index on `profiles.username` (0007) still
applies to whatever the generated value is.

Everything else about the function — including the manual-signup path,
where `raw_user_meta_data ->> 'username'` is present and used as-is — is
unchanged from 0007.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0010_google_username_fallback"
down_revision: str | None = "0009_auth_hooks"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
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
                    COALESCE(
                        NEW.raw_user_meta_data ->> 'username',
                        'user_' || substr(NEW.id::text, 1, 8)
                    ),
                    now()
                );
                RETURN NEW;
            END;
            $$;
            """
        )
    )


def downgrade() -> None:
    # Restores 0007_profiles.py's original version verbatim. The trigger
    # itself (on_auth_user_created) is untouched by either migration, so
    # only the function body needs replacing back.
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
