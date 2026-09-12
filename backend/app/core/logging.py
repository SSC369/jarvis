"""Structured logging, with secret redaction installed first.

Requirement FR-3 says no application log records the provider credential, at any
level. The redaction processor below is registered ahead of every other
processor so that nothing can render a secret before it is removed.

It is installed in slice 1, before any credential exists, so that no later slice
has to remember to add it.
"""

import logging
import sys
from collections.abc import Callable, MutableMapping
from typing import Any

import structlog

REDACTED = "[redacted]"

_MAX_REDACTION_DEPTH = 6


def _redact(value: Any, secrets: frozenset[str], depth: int = 0) -> Any:
    """Replace any secret found anywhere inside ``value``.

    Walks strings, mappings, and sequences. Depth is bounded because a log event
    should never be deep enough to need more, and an unbounded walk on a cyclic
    structure would hang the logger.
    """
    if depth > _MAX_REDACTION_DEPTH:
        return value

    if isinstance(value, str):
        for secret in secrets:
            if secret in value:
                value = value.replace(secret, REDACTED)
        return value

    if isinstance(value, MutableMapping):
        return {k: _redact(v, secrets, depth + 1) for k, v in value.items()}

    if isinstance(value, (list, tuple)):
        rebuilt = [_redact(v, secrets, depth + 1) for v in value]
        return type(value)(rebuilt)

    if isinstance(value, BaseException):
        # A provider error rendered into a traceback is the most common way a
        # credential reaches a log. Redact the message, not the exception type.
        return _redact(str(value), secrets, depth + 1)

    return value


def build_redactor(
    secrets: frozenset[str],
) -> Callable[[Any, str, MutableMapping[str, Any]], MutableMapping[str, Any]]:
    """Build a structlog processor that strips ``secrets`` from every event."""

    def redact_secrets(
        _logger: Any, _method_name: str, event_dict: MutableMapping[str, Any]
    ) -> MutableMapping[str, Any]:
        if not secrets:
            return event_dict
        return _redact(event_dict, secrets)  # type: ignore[no-any-return]

    return redact_secrets


def configure_logging(
    log_level: str, secrets: frozenset[str], json_output: bool
) -> None:
    """Configure structlog for the process. Call once, at startup."""
    logging.basicConfig(
        format="%(message)s", stream=sys.stdout, level=getattr(logging, log_level)
    )

    renderer: Any = (
        structlog.processors.JSONRenderer()
        if json_output
        else structlog.dev.ConsoleRenderer()
    )

    structlog.configure(
        processors=[
            build_redactor(secrets),
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level)
        ),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
