"""The only names other domains may import from the gateway.

A domain's public surface is its contract. Adding a name here is a deliberate
act, reviewed like an API change, because from that moment other domains may
depend on it. See backend/.claude/rules/repo-rules.md section 6.

A consumer declares its own port and writes an adapter against these names. It
does not import anything else from this package.

The published entry point is an interactor rather than a wrapper service. The
gateway's whole surface is one use case, and a class that exists only to forward
to it would be ceremony. See ruleset section 6, amended 2026-09-12.
"""

from app.domains.gateway.errors import (
    Extraction,
    ExtractionResult,
    MalformedResult,
    ProviderTimeout,
    ProviderUnavailable,
    SharedQuotaExhausted,
    UserLimitReached,
)
from app.domains.gateway.interactors.extract import ExtractInteractor
from app.domains.gateway.interfaces.dtos import ExtractionRequest

__all__ = [
    "ExtractInteractor",
    "Extraction",
    "ExtractionRequest",
    "ExtractionResult",
    "MalformedResult",
    "ProviderTimeout",
    "ProviderUnavailable",
    "SharedQuotaExhausted",
    "UserLimitReached",
]
