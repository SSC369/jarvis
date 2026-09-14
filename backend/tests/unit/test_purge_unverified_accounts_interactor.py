"""PurgeUnverifiedAccountsInteractor: T-1.6's own test. FR-8."""

import uuid
from datetime import UTC, datetime, timedelta

from app.domains.identity.interactors.purge_unverified_accounts import (
    PurgeUnverifiedAccountsInteractor,
)
from tests.fakes.fake_auth_account_repository import (
    FakeAuthAccountRepository,
    FakeUnverifiedAccount,
)


async def test_purges_only_accounts_older_than_the_grace_window() -> None:
    now = datetime.now(UTC)
    repository = FakeAuthAccountRepository()
    old_account = FakeUnverifiedAccount(
        user_id=uuid.uuid4(), created_at=now - timedelta(hours=25)
    )
    recent_account = FakeUnverifiedAccount(
        user_id=uuid.uuid4(), created_at=now - timedelta(hours=1)
    )
    repository.unverified_accounts = [old_account, recent_account]
    interactor = PurgeUnverifiedAccountsInteractor(auth_account_repository=repository)

    deleted_count = await interactor.purge_unverified_accounts()

    assert deleted_count == 1
    assert repository.unverified_accounts == [recent_account]


async def test_nothing_to_purge_returns_zero() -> None:
    interactor = PurgeUnverifiedAccountsInteractor(
        auth_account_repository=FakeAuthAccountRepository()
    )

    deleted_count = await interactor.purge_unverified_accounts()

    assert deleted_count == 0
