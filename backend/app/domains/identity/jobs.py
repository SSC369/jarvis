"""Identity's Procrastinate tasks. Thin: resolve collaborators, call one
interactor. See backend/.claude/rules/repo-rules.md section 14.

A task has no per-request `Context` to draw a database session from, so this
module opens its own engine and session factory, lazily, the first time a
task runs. That engine is separate from the one `app/main.py` builds for
GraphQL requests — a worker process (`procrastinate worker`) is typically a
different process from the web process, so sharing a pool across them is not
possible in general; a single combined process would open two pools, which
is a known simplification, noted in the feature dev log.
"""

from functools import lru_cache

import structlog
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.db import create_engine, create_session_factory
from app.core.deps import build_purge_unverified_accounts_interactor
from app.core.jobs import procrastinate_app
from app.core.settings import get_settings

logger = structlog.get_logger(__name__)


@lru_cache
def _session_factory() -> async_sessionmaker[AsyncSession]:
    return create_session_factory(create_engine(get_settings()))


@procrastinate_app.periodic(cron="0 * * * *")  # hourly, on the hour
@procrastinate_app.task(name="identity.purge_unverified_accounts")
async def purge_unverified_accounts(timestamp: int) -> None:
    """FR-8: delete every `auth.users` row still unverified 24 hours after
    signup, so its email can be used again.

    Runs on the service-role connection deliberately (rule T3): this is a
    background sweep across every user, never a request on one user's
    behalf, so it must not be scoped by Row Level Security the way a request
    session is. `AuthAccountRepository` is the only repository that reaches
    `auth.users` directly, and it never calls `user_transaction`.
    """
    async with _session_factory()() as session:
        interactor = build_purge_unverified_accounts_interactor(session)
        deleted_count = await interactor.purge_unverified_accounts()
    logger.info("identity.unverified_accounts_purged", deleted_count=deleted_count)
