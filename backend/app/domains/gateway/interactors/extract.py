"""The gateway's one use case: extract structure from a user's text.

Four steps, in this order, every time: allowance, provider, usage, result.
Step three runs for every path that reached step two, including every failure,
which is requirement FR-13 and the step most easily skipped on an error branch.
"""

import time
import uuid
from datetime import UTC, datetime
from typing import cast
from uuid import UUID

import structlog
from strawberry.scalars import JSON

from app.core.errors import DomainError
from app.core.settings import Settings
from app.domains.gateway.constants import PROVIDER_NAME
from app.domains.gateway.errors import (
    Extraction,
    ExtractionResult,
    MalformedResultError,
    ProviderTimeoutError,
    ProviderUnavailableError,
    SharedQuotaExhaustedError,
    UserLimitReachedError,
)
from app.domains.gateway.interfaces.dtos import ExtractionRequest, UsageRecord
from app.domains.gateway.interfaces.providers import ModelProvider
from app.domains.gateway.interfaces.repositories import UsageRepository
from app.domains.gateway.services.allowance_service import AllowanceService

logger = structlog.get_logger(__name__)

_OUTCOME_BY_ERROR: dict[type[DomainError], str] = {
    UserLimitReachedError: "user_limit_reached",
    SharedQuotaExhaustedError: "shared_quota_exhausted",
    ProviderUnavailableError: "provider_unavailable",
    ProviderTimeoutError: "provider_timeout",
    MalformedResultError: "malformed_result",
}


class ExtractInteractor:
    def __init__(
        self,
        provider: ModelProvider,
        usage_repository: UsageRepository,
        allowance_service: AllowanceService,
        settings: Settings,
    ) -> None:
        self.provider = provider
        self.usage_repository = usage_repository
        self.allowance_service = allowance_service
        self.settings = settings

    async def extract(
        self, *, user_id: UUID, request: ExtractionRequest
    ) -> ExtractionResult:
        """Run one extraction on behalf of one user.

        ``user_id`` comes from the request context and never from caller input,
        which is the mechanism behind FR-6. Validates first, then orchestrates:
        both validations run before the provider is ever called.
        """
        try:
            self._validate_gateway_enabled()
            await self._validate_allowance(user_id=user_id)
        except ProviderUnavailableError as error:
            return cast(ExtractionResult, error.to_gql())
        except UserLimitReachedError as error:
            await self._record_usage(
                user_id=user_id,
                model=self.settings.gemini_model,
                input_tokens=0,
                output_tokens=0,
                error=error,
                latency_ms=None,
            )
            return cast(ExtractionResult, error.to_gql())

        started = time.perf_counter()
        try:
            result = await self.provider.generate(request)
        except DomainError as error:
            elapsed_ms = int((time.perf_counter() - started) * 1000)
            await self._record_usage(
                user_id=user_id,
                model=self.settings.gemini_model,
                input_tokens=0,
                output_tokens=0,
                error=error,
                latency_ms=elapsed_ms,
            )
            return cast(ExtractionResult, error.to_gql())

        elapsed_ms = int((time.perf_counter() - started) * 1000)
        await self._record_usage(
            user_id=user_id,
            model=result.model,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            error=None,
            latency_ms=elapsed_ms,
        )
        return Extraction(
            data=cast(JSON, result.data),
            model=result.model,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
        )

    def _validate_gateway_enabled(self) -> None:
        """Refuse while the kill switch is off.

        Checked first and never recorded on failure: a disabled gateway is our
        fault, so it must not consume a user's daily count.
        """
        if not self.settings.gateway_enabled:
            raise ProviderUnavailableError()

    async def _validate_allowance(self, *, user_id: UUID) -> None:
        """Refuse a user who is out of headroom for the window."""
        allowance = await self.allowance_service.allowance_for(user_id=user_id)
        if not allowance.has_capacity:
            raise UserLimitReachedError(
                limit=allowance.limit, resets_at=allowance.resets_at
            )

    async def _record_usage(
        self,
        *,
        user_id: UUID,
        model: str,
        input_tokens: int,
        output_tokens: int,
        error: DomainError | None,
        latency_ms: int | None,
    ) -> None:
        """Write the usage row. Never raises.

        A failed insert after a successful provider call must not cost the
        caller the result they already paid for. FR-15 forbids losing usage
        *silently*, so the loss is logged at error and surfaces in NFR-3's
        reconciliation of provider calls against rows.
        """
        outcome = "success" if error is None else _OUTCOME_BY_ERROR[type(error)]
        usage = UsageRecord(
            id=uuid.uuid4(),
            user_id=user_id,
            provider=PROVIDER_NAME,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            outcome=outcome,
            latency_ms=latency_ms,
        )
        try:
            await self.usage_repository.record(
                usage=usage, occurred_at=datetime.now(UTC)
            )
        except Exception:
            logger.exception(
                "gateway.usage_not_recorded", user_id=str(user_id), outcome=outcome
            )
