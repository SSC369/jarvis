from uuid import UUID

from app.domains.identity.interfaces.dtos import ProfileDTO
from app.domains.identity.interfaces.repositories import ProfileRepository


class GetProfileInteractor:
    def __init__(self, *, profile_repository: ProfileRepository) -> None:
        self.profile_repository = profile_repository

    async def get_profile(self, *, user_id: UUID) -> ProfileDTO:
        """Return the caller's profile.

        No `profiles` row is not an error here (04.1-manual-signup-and-signin.md
        T-1.5's own acceptance check: "`me` returns `username: null` for a user
        with no profile row") — an account that predates the `handle_new_user()`
        trigger, or one the trigger otherwise missed, still gets a session and
        still needs `me` to resolve rather than throw.
        """
        profile = await self.profile_repository.get_for_user(user_id=user_id)
        if profile is not None:
            return profile
        return ProfileDTO(
            user_id=user_id, username=None, avatar_url=None, created_at=None
        )
