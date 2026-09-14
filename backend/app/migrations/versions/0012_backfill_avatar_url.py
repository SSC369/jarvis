"""One-time backfill: populate avatar_url for profiles created before
0011_profile_avatar_url added the column and the trigger that sets it.

Revision ID: 0012_backfill_avatar_url
Revises: 0011_profile_avatar_url
Create Date: 2026-09-15

`handle_new_user()` only fires on `auth.users` INSERT, never on a repeat
sign-in, so an account created before 0011 landed has `avatar_url = NULL`
forever even though `auth.users.raw_user_meta_data` already carries a real
`avatar_url`/`picture` from Google (Supabase keeps that column current on
each OAuth sign-in; only `profiles`, the table this app owns, was stale).
Confirmed live 2026-09-15 against the real dev project: an account created
2026-09-14, before this column existed, had a populated
`raw_user_meta_data->>'avatar_url'` and a null `profiles.avatar_url`.

Data-only, not reversible in the usual sense: `downgrade()` cannot tell a
row this backfilled from one that already had a value some other way, so it
is a no-op rather than guessing which rows to null back out.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0012_backfill_avatar_url"
down_revision: str | None = "0011_profile_avatar_url"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
            UPDATE public.profiles AS p
            SET avatar_url = COALESCE(
                au.raw_user_meta_data ->> 'avatar_url',
                au.raw_user_meta_data ->> 'picture'
            )
            FROM auth.users AS au
            WHERE au.id = p.id
              AND p.avatar_url IS NULL
              AND COALESCE(
                    au.raw_user_meta_data ->> 'avatar_url',
                    au.raw_user_meta_data ->> 'picture'
                  ) IS NOT NULL
            """
        )
    )


def downgrade() -> None:
    # No-op: a data backfill, not a schema change. See module docstring for
    # why there is nothing safe to revert.
    pass
