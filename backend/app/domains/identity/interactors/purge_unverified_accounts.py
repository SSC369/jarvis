from datetime import UTC, datetime

from app.domains.identity.constants import UNVERIFIED_ACCOUNT_TTL
from app.domains.identity.interfaces.repositories import AuthAccountRepository


class PurgeUnverifiedAccountsInteractor:
    def __init__(self, *, auth_account_repository: AuthAccountRepository) -> None:
        self.auth_account_repository = auth_account_repository

    async def purge_unverified_accounts(self) -> int:
        """Delete every ``auth.users`` row never verified within the grace
        window.

        FR-8: an account that has not confirmed its email 24 hours after
        signup is removed, freeing that email for a later signup attempt.

        Returns:
            How many rows were deleted, for the job's own log line.
        """
        cutoff = datetime.now(UTC) - UNVERIFIED_ACCOUNT_TTL
        return await self.auth_account_repository.delete_unverified_created_before(
            cutoff=cutoff
        )
