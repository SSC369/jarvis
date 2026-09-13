"""The LangChain provider. The only object in the process holding the key.

A service, not an adapter. Section 4 of the ruleset puts talking to Gemini in
`services/`, and reserves `adapters/` for the cross-domain anticorruption layer
of section 6. This file talks to a vendor and knows about no other domain.

It is the whole of the gateway's dependency on LangChain. Nothing above
`ModelProvider` imports it, so rule T4's boundary is ours: swapping framework or
vendor is this file and one line in `deps.py`.

Requirement FR-18 needs six distinguishable outcomes. LangChain 1.x normalises
provider failures into its own typed hierarchy (`ModelRateLimitError`,
`ModelTimeoutError`, `ModelConnectionError`), so the mapping below reads from
those rather than unwrapping to the Google SDK. Sub-plan 04.3 section 6.2
predicted the opposite and was wrong for this version; the correction is in the
dev log.
"""

import asyncio
from typing import Any

import structlog
from langchain_core.exceptions import (
    ModelAPIError,
    ModelAuthenticationError,
    ModelConnectionError,
    ModelPermissionDeniedError,
    ModelRateLimitError,
    ModelTimeoutError,
    OutputParserException,
)
from langchain_google_genai import ChatGoogleGenerativeAI

from app.domains.gateway.constants import (
    MAX_ATTEMPTS,
    PROVIDER_TIMEOUT_SECONDS,
    RETRY_BACKOFF_SECONDS,
)
from app.domains.gateway.errors import (
    MalformedResultError,
    ProviderTimeoutError,
    ProviderUnavailableError,
    SharedQuotaExhaustedError,
)
from app.domains.gateway.interfaces.dtos import ExtractionRequest, ProviderResult

logger = structlog.get_logger(__name__)


class LangChainGeminiProvider:
    """Implements ModelProvider over LangChain's Gemini binding."""

    def __init__(self, *, api_key: str, model: str) -> None:
        self._model_name = model
        self._chat = ChatGoogleGenerativeAI(model=model, google_api_key=api_key)

    async def generate(self, request: ExtractionRequest) -> ProviderResult:
        """Call the model under a timeout, retrying only a failed connection."""
        last_error: Exception | None = None

        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                async with asyncio.timeout(PROVIDER_TIMEOUT_SECONDS):
                    return await self._invoke(request)

            except TimeoutError as error:
                # Never retried. The first attempt may still be running at the
                # provider, and a retry would double the spend. FR-20.
                raise ProviderTimeoutError(PROVIDER_TIMEOUT_SECONDS) from error

            except ModelRateLimitError as error:
                raise SharedQuotaExhaustedError() from error

            except ModelTimeoutError as error:
                raise ProviderTimeoutError(PROVIDER_TIMEOUT_SECONDS) from error

            except (ModelAuthenticationError, ModelPermissionDeniedError) as error:
                # A rejected credential is an operator problem, not a user one.
                # Logged distinctly, surfaced generically: the caller learns
                # nothing about our key. FR-2.
                logger.error("gateway.credential_rejected", reason=type(error).__name__)
                raise ProviderUnavailableError() from error

            except OutputParserException as error:
                raise MalformedResultError(reason=str(error)[:200]) from error

            except ModelConnectionError as error:
                # The only retryable failure: a connection that never
                # established, so nothing was charged and nothing ran. FR-20.
                last_error = error
                if attempt < MAX_ATTEMPTS:
                    logger.warning("gateway.retrying", attempt=attempt)
                    await asyncio.sleep(RETRY_BACKOFF_SECONDS)
                    continue
                raise ProviderUnavailableError() from error

            except ModelAPIError as error:
                raise ProviderUnavailableError() from error

        raise ProviderUnavailableError() from last_error

    async def _invoke(self, request: ExtractionRequest) -> ProviderResult:
        structured = self._chat.with_structured_output(request.schema, include_raw=True)
        prompt = (
            f"{request.instruction}\n\n{request.prompt}"
            if request.instruction
            else request.prompt
        )
        response: Any = await structured.ainvoke(prompt)

        parsed = response.get("parsed") if isinstance(response, dict) else None
        if parsed is None:
            raise MalformedResultError(reason="the model returned no structured output")

        return ProviderResult(
            data=dict(parsed),
            input_tokens=self._read_token_count(
                response=response, field="input_tokens"
            ),
            output_tokens=self._read_token_count(
                response=response, field="output_tokens"
            ),
            model=self._model_name,
        )

    @staticmethod
    def _read_token_count(*, response: Any, field: str) -> int:
        """Token counts, from the provider rather than estimated. FR-11.

        Zero when the provider omits them, which is honest: a recorded zero is
        visibly wrong in reconciliation, an invented estimate is not.
        """
        raw = response.get("raw") if isinstance(response, dict) else None
        metadata = getattr(raw, "usage_metadata", None) or {}
        return int(metadata.get(field, 0))
