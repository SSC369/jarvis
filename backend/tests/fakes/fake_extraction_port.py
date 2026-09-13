"""An in-memory ExtractionPort that returns or raises on command."""

from typing import Any, cast
from uuid import UUID

from strawberry.scalars import JSON

from app.domains.gateway.public import Extraction, ExtractionResult


class FakeExtractionPort:
    def __init__(
        self,
        *,
        result: ExtractionResult | None = None,
        results: list[ExtractionResult] | None = None,
    ) -> None:
        """``results``, when given, is returned one at a time per call, so a
        test can script a sequence (e.g. a title-missing answer to a
        due-date question)."""
        self._result = result
        self._results = list(results) if results is not None else None
        self.calls: list[str] = []

    async def extract(
        self,
        *,
        user_id: UUID,
        prompt: str,
        schema: dict[str, Any],
        instruction: str,
    ) -> ExtractionResult:
        self.calls.append(prompt)
        if self._results is not None:
            return self._results.pop(0)
        assert self._result is not None
        return self._result


def extraction(*, title: str | None = None, due_at: str | None = None) -> Extraction:
    data: dict[str, Any] = {}
    if title is not None:
        data["title"] = title
    if due_at is not None:
        data["due_at"] = due_at
    return Extraction(
        data=cast(JSON, data), model="fake", input_tokens=1, output_tokens=1
    )
