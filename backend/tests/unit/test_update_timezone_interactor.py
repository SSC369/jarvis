"""Changing the stored timezone, and refusing an invalid one. FR-28, error table."""

import uuid

import pytest

from app.domains.identity.graphql.errors import InvalidTimezoneError
from app.domains.identity.interactors.dtos import UpdateTimezoneInputDTO
from app.domains.identity.interactors.update_timezone import UpdateTimezoneInteractor
from tests.fakes.fake_settings_repository import FakeSettingsRepository


async def test_changes_the_stored_timezone() -> None:
    user_id = uuid.uuid4()
    repository = FakeSettingsRepository()
    interactor = UpdateTimezoneInteractor(settings_repository=repository)

    settings = await interactor.update_timezone(
        dto=UpdateTimezoneInputDTO(user_id=user_id, timezone="Europe/London")
    )

    assert settings.timezone == "Europe/London"


async def test_invalid_timezone_is_refused_and_nothing_is_stored() -> None:
    """T-2.12."""
    user_id = uuid.uuid4()
    repository = FakeSettingsRepository()
    interactor = UpdateTimezoneInteractor(settings_repository=repository)

    with pytest.raises(InvalidTimezoneError):
        await interactor.update_timezone(
            dto=UpdateTimezoneInputDTO(user_id=user_id, timezone="not/a/zone")
        )

    assert await repository.get_for_user(user_id=user_id) is None
