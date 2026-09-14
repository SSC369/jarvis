"""profiles.avatar_url: FR-21, store the avatar Google provides, if any.

Revision ID: 0011_profile_avatar_url
Revises: 0010_google_username_fallback
Create Date: 2026-09-15

Google's OAuth metadata carries a picture under `avatar_url` and/or
`picture` (Supabase normalises to `avatar_url` for most providers but both
keys are observed in practice), so `handle_new_user()` coalesces both.
Manual signup never sets this: `auth.users.signUp()`'s `options.data` only
ever carries `username`, so a manually-created account's `avatar_url` stays
null, and `AppShell` falls back to its letter avatar for that case.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0011_profile_avatar_url"
down_revision: str | None = "0010_google_username_fallback"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("profiles", sa.Column("avatar_url", sa.Text(), nullable=True))

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
                INSERT INTO public.profiles (id, username, avatar_url, created_at)
                VALUES (
                    NEW.id,
                    COALESCE(
                        NEW.raw_user_meta_data ->> 'username',
                        'user_' || substr(NEW.id::text, 1, 8)
                    ),
                    COALESCE(
                        NEW.raw_user_meta_data ->> 'avatar_url',
                        NEW.raw_user_meta_data ->> 'picture'
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
    # Restores 0010's version verbatim, then drops the column.
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
    op.drop_column("profiles", "avatar_url")
