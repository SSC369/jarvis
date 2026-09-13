"""A ModelProvider that returns or raises on command."""

from app.domains.gateway.interfaces.dtos import ExtractionRequest, ProviderResult


class FakeProvider:
    def __init__(
        self, result: ProviderResult | None = None, raises: Exception | None = None
    ) -> None:
        self._result = result
        self._raises = raises
        self.calls = 0

    async def generate(self, request: ExtractionRequest) -> ProviderResult:
        self.calls += 1
        if self._raises is not None:
            raise self._raises
        assert self._result is not None
        return self._result
