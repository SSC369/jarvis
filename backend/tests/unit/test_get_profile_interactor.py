"""GetProfileInteractor: T-1.5's own tests. No create-on-read, unlike
settings — a profile is created only by the handle_new_user() trigger."""

import uuid
from datetime import UTC, datetime

from app.domains.identity.interactors.get_profile import GetProfileInteractor
from app.domains.identity.interfaces.dtos import ProfileDTO
from tests.fakes.fake_profile_repository import FakeProfileRepository


async def test_returns_the_caller_s_profile() -> None:
    user_id = uuid.uuid4()
    repository = FakeProfileRepository()
    repository.rows[user_id] = ProfileDTO(
        user_id=user_id, username="sai", avatar_url=None, created_at=datetime.now(UTC)
    )
    interactor = GetProfileInteractor(profile_repository=repository)

    profile = await interactor.get_profile(user_id=user_id)

    assert profile.username == "sai"


async def test_a_profile_with_no_username_is_returned_as_is() -> None:
    """A Google-only account has no username; that is not an error."""
    user_id = uuid.uuid4()
    repository = FakeProfileRepository()
    repository.rows[user_id] = ProfileDTO(
        user_id=user_id, username=None, avatar_url=None, created_at=datetime.now(UTC)
    )
    interactor = GetProfileInteractor(profile_repository=repository)

    profile = await interactor.get_profile(user_id=user_id)

    assert profile.username is None


async def test_a_google_avatar_is_returned_as_is() -> None:
    """FR-21: a Google-provided avatar passes through unchanged."""
    user_id = uuid.uuid4()
    repository = FakeProfileRepository()
    repository.rows[user_id] = ProfileDTO(
        user_id=user_id,
        username="user_1a2b3c4d",
        avatar_url="https://lh3.googleusercontent.com/a/example",
        created_at=datetime.now(UTC),
    )
    interactor = GetProfileInteractor(profile_repository=repository)

    profile = await interactor.get_profile(user_id=user_id)

    assert profile.avatar_url == "https://lh3.googleusercontent.com/a/example"


async def test_no_row_at_all_returns_a_null_username_not_an_error() -> None:
    """04.1-manual-signup-and-signin.md T-1.5's own acceptance check: "`me`
    returns `username: null` for a user with no profile row." An account
    that predates the handle_new_user() trigger (or one it otherwise missed)
    still has a session and still needs `me` to resolve, not throw."""
    user_id = uuid.uuid4()
    interactor = GetProfileInteractor(profile_repository=FakeProfileRepository())

    profile = await interactor.get_profile(user_id=user_id)

    assert profile.user_id == user_id
    assert profile.username is None
