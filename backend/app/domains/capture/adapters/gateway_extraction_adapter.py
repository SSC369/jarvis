"""Implements capture's ExtractionPort against the gateway domain."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from app.domains.gateway.public import (
    ExtractInteractor,
    ExtractionRequest,
    ExtractionResult,
)


class GatewayExtractionAdapter:
    def __init__(self, *, extract_interactor: ExtractInteractor) -> None:
        self.extract_interactor = extract_interactor

    async def extract(
        self,
        *,
        user_id: UUID,
        prompt: str,
        schema: dict[str, Any],
        instruction: str,
    ) -> ExtractionResult:
        # Kept short deliberately: constants.py documents why instruction and
        # schema description length measurably affect generation latency
        # against the 8 second budget.
        now_iso = datetime.now(UTC).isoformat()
        full_instruction = f"{instruction} Today is {now_iso}."
        return await self.extract_interactor.extract(
            user_id=user_id,
            request=ExtractionRequest(
                prompt=prompt, schema=schema, instruction=full_instruction
            ),
        )
