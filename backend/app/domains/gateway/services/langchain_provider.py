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

    def __init__(self, api_key: str, model: str) -> None:
        self._model_name = model
        self._chat = ChatGoogleGenerativeAI(model=model, google_api_key=api_key)

    async def generate(self, request: ExtractionRequest) -> ProviderResult:
        """Call the model under a timeout, retrying only a failed connection."""
        last_error: Exception | None = None

        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                async with asyncio.timeout(PROVIDER_TIMEOUT_SECONDS):
                    return await self._invoke(request)

            except TimeoutError as exc:
                # Never retried. The first attempt may still be running at the
                # provider, and a retry would double the spend. FR-20.
                raise ProviderTimeoutError(PROVIDER_TIMEOUT_SECONDS) from exc

            except ModelRateLimitError as exc:
                raise SharedQuotaExhaustedError() from exc

            except ModelTimeoutError as exc:
                raise ProviderTimeoutError(PROVIDER_TIMEOUT_SECONDS) from exc

            except (ModelAuthenticationError, ModelPermissionDeniedError) as exc:
                # A rejected credential is an operator problem, not a user one.
                # Logged distinctly, surfaced generically: the caller learns
                # nothing about our key. FR-2.
                logger.error("gateway.credential_rejected", reason=type(exc).__name__)
                raise ProviderUnavailableError() from exc

            except OutputParserException as exc:
                raise MalformedResultError(reason=str(exc)[:200]) from exc

            except ModelConnectionError as exc:
                # The only retryable failure: a connection that never
                # established, so nothing was charged and nothing ran. FR-20.
                last_error = exc
                if attempt < MAX_ATTEMPTS:
                    logger.warning("gateway.retrying", attempt=attempt)
                    await asyncio.sleep(RETRY_BACKOFF_SECONDS)
                    continue
                raise ProviderUnavailableError() from exc

            except ModelAPIError as exc:
                raise ProviderUnavailableError() from exc

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
            input_tokens=self._usage(response, "input_tokens"),
            output_tokens=self._usage(response, "output_tokens"),
            model=self._model_name,
        )

    @staticmethod
    def _usage(response: Any, field: str) -> int:
        """Token counts, from the provider rather than estimated. FR-11.

        Zero when the provider omits them, which is honest: a recorded zero is
        visibly wrong in reconciliation, an invented estimate is not.
        """
        raw = response.get("raw") if isinstance(response, dict) else None
        metadata = getattr(raw, "usage_metadata", None) or {}
        return int(metadata.get(field, 0))
