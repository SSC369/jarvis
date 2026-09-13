"""T-3.12: the provider key never reaches a log. FR-3.

Slice 1 built the redactor and proved it works on a fabricated secret. This
proves the real credential is actually in the set it strips, which is the part
that breaks when someone adds a setting and forgets.
"""

from app.core.logging import REDACTED, build_redactor
from app.core.settings import get_settings


def test_the_provider_key_is_tracked_for_redaction() -> None:
    settings = get_settings()

    assert settings.gemini_api_key in settings.secret_values()


def test_the_key_is_stripped_from_an_exception_string() -> None:
    """The path a credential actually takes to a log: a provider traceback."""
    settings = get_settings()
    key = settings.gemini_api_key
    redact = build_redactor(settings.secret_values())

    event = redact(
        None, "error", {"event": "call failed", "error": ValueError(f"401 for {key}")}
    )

    assert key not in str(event)
    assert REDACTED in str(event)


def test_the_key_is_stripped_from_nested_request_data() -> None:
    settings = get_settings()
    key = settings.gemini_api_key
    redact = build_redactor(settings.secret_values())

    event = redact(
        None,
        "debug",
        {"event": "call", "request": {"headers": {"x-goog-api-key": key}}},
    )

    assert key not in str(event)
