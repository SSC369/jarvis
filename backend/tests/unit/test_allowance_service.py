"""Allowance cases. See 04.3 section 8."""

import uuid

from app.domains.gateway.constants import DEFAULT_REQUESTS_PER_DAY
from app.domains.gateway.services.allowance_service import AllowanceService
from tests.fakes.fake_usage_repository import FakeUsageRepository


async def test_user_under_their_limit_has_capacity() -> None:
    """T-3.2."""
    service = AllowanceService(FakeUsageRepository(limit=20, used=5))

    allowance = await service.allowance_for(user_id=uuid.uuid4())

    assert allowance.has_capacity
    assert allowance.remaining == 15


async def test_user_at_their_limit_has_none() -> None:
    """T-3.1."""
    service = AllowanceService(FakeUsageRepository(limit=20, used=20))

    allowance = await service.allowance_for(user_id=uuid.uuid4())

    assert not allowance.has_capacity
    assert allowance.remaining == 0


async def test_user_over_their_limit_reports_zero_not_negative() -> None:
    service = AllowanceService(FakeUsageRepository(limit=20, used=25))

    allowance = await service.allowance_for(user_id=uuid.uuid4())

    assert allowance.remaining == 0


async def test_no_limit_row_falls_back_to_the_default() -> None:
    """T-3.3: a user with no row is limited, never unlimited.

    Failing open on a spend control is the wrong failure.
    """
    service = AllowanceService(FakeUsageRepository(limit=None, used=0))

    allowance = await service.allowance_for(user_id=uuid.uuid4())

    assert allowance.limit == DEFAULT_REQUESTS_PER_DAY


async def test_reset_time_is_in_the_future() -> None:
    """T-3.4: FR-9 says the refusal tells the user when it resets."""
    from datetime import UTC, datetime

    service = AllowanceService(FakeUsageRepository(limit=20, used=20))
    now = datetime.now(UTC)

    allowance = await service.allowance_for(user_id=uuid.uuid4(), now=now)

    assert allowance.resets_at > now
