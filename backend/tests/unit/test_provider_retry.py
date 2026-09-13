"""Retry and failure-mapping cases for the LangChain adapter. 04.3 section 8.

FR-20 says a failed call is retried only where retrying is safe and useful.
Exactly one failure qualifies: a connection that never established, so nothing
ran and nothing was charged. These cases pin that down, because the tempting
change is to retry everything.
"""

import pytest
from langchain_core.exceptions import (
    ModelAPIError,
    ModelAuthenticationError,
    ModelConnectionError,
    ModelRateLimitError,
    ModelTimeoutError,
    OutputParserException,
)

from app.domains.gateway.constants import MAX_ATTEMPTS
from app.domains.gateway.errors import (
    MalformedResultError,
    ProviderTimeoutError,
    ProviderUnavailableError,
    SharedQuotaExhaustedError,
)
from app.domains.gateway.interfaces.dtos import ExtractionRequest, ProviderResult
from app.domains.gateway.services.langchain_provider import LangChainGeminiProvider

REQUEST = ExtractionRequest(prompt="x", schema={"type": "object"})


class _Provider(LangChainGeminiProvider):
    """The real retry and mapping logic, with the network replaced."""

    def __init__(
        self, *failures: Exception, then: ProviderResult | None = None
    ) -> None:
        self.attempts = 0
        self._failures = list(failures)
        self._then = then
        self._model_name = "test-model"

    async def _invoke(self, request: ExtractionRequest) -> ProviderResult:
        self.attempts += 1
        if self._failures:
            raise self._failures.pop(0)
        if self._then is None:
            raise AssertionError("no result configured")
        return self._then


SUCCESS = ProviderResult(data={}, input_tokens=1, output_tokens=1, model="test-model")


async def test_connection_error_is_retried_then_succeeds() -> None:
    """T-3.7: the one retryable failure."""
    provider = _Provider(ModelConnectionError("no route"), then=SUCCESS)

    result = await provider.generate(REQUEST)

    assert result is SUCCESS
    assert provider.attempts == 2


async def test_connection_error_gives_up_after_max_attempts() -> None:
    """T-3.7: and it stops, rather than retrying forever."""
    provider = _Provider(*[ModelConnectionError("no route")] * 5)

    with pytest.raises(ProviderUnavailableError):
        await provider.generate(REQUEST)

    assert provider.attempts == MAX_ATTEMPTS


async def test_timeout_is_never_retried() -> None:
    """T-3.9: the first attempt may still be running, so a retry doubles spend."""
    provider = _Provider(ModelTimeoutError("slow"), then=SUCCESS)

    with pytest.raises(ProviderTimeoutError):
        await provider.generate(REQUEST)

    assert provider.attempts == 1


async def test_budget_exhaustion_is_a_timeout_not_an_outage() -> None:
    """T-3.6: FR-19's abandoned call is distinguishable from FR-18's outage."""

    class _Slow(_Provider):
        async def _invoke(self, request: ExtractionRequest) -> ProviderResult:
            self.attempts += 1
            raise TimeoutError

    provider = _Slow()

    with pytest.raises(ProviderTimeoutError):
        await provider.generate(REQUEST)

    assert provider.attempts == 1


@pytest.mark.parametrize(
    ("raised", "expected"),
    [
        (ModelRateLimitError("429"), SharedQuotaExhaustedError),
        (ModelAuthenticationError("bad key"), ProviderUnavailableError),
        (ModelAPIError("500"), ProviderUnavailableError),
        (OutputParserException("not json"), MalformedResultError),
    ],
)
async def test_each_provider_failure_maps_without_retrying(
    raised: Exception, expected: type[Exception]
) -> None:
    """T-3.8: none of these is retryable, and each maps to its own outcome."""
    provider = _Provider(raised, then=SUCCESS)

    with pytest.raises(expected):
        await provider.generate(REQUEST)

    assert provider.attempts == 1


async def test_quota_error_is_not_reported_as_an_outage() -> None:
    """FR-9: a user must be able to tell these apart, so we must too."""
    provider = _Provider(ModelRateLimitError("429"))

    with pytest.raises(SharedQuotaExhaustedError):
        await provider.generate(REQUEST)
