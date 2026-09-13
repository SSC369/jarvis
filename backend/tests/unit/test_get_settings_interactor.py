"""First-read creation and idempotent re-reads. FR-28."""

import uuid

from app.domains.identity.interactors.dtos import GetSettingsInputDTO
from app.domains.identity.interactors.get_settings import GetSettingsInteractor
from tests.fakes.fake_settings_repository import FakeSettingsRepository


async def test_first_call_creates_a_row_with_the_detected_timezone() -> None:
    """T-2.10."""
    user_id = uuid.uuid4()
    repository = FakeSettingsRepository()
    interactor = GetSettingsInteractor(settings_repository=repository)

    settings = await interactor.get_settings(
        dto=GetSettingsInputDTO(user_id=user_id, detected_timezone="Asia/Kolkata")
    )

    assert settings.timezone == "Asia/Kolkata"


async def test_second_call_returns_the_same_row_not_a_new_one() -> None:
    """T-2.10."""
    user_id = uuid.uuid4()
    repository = FakeSettingsRepository()
    interactor = GetSettingsInteractor(settings_repository=repository)

    first = await interactor.get_settings(
        dto=GetSettingsInputDTO(user_id=user_id, detected_timezone="Asia/Kolkata")
    )
    second = await interactor.get_settings(
        dto=GetSettingsInputDTO(user_id=user_id, detected_timezone="America/New_York")
    )

    assert second.timezone == "Asia/Kolkata"
    assert second.created_at == first.created_at


async def test_no_detected_timezone_falls_back_to_default() -> None:
    user_id = uuid.uuid4()
    repository = FakeSettingsRepository()
    interactor = GetSettingsInteractor(settings_repository=repository)

    settings = await interactor.get_settings(
        dto=GetSettingsInputDTO(user_id=user_id, detected_timezone=None)
    )

    assert settings.timezone == "UTC"
