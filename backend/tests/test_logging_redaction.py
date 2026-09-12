"""Secret redaction cases. See 04.1-api-skeleton.md section 7, case T-1.6.

FR-3 says no application log records the credential, at any level. These cases
are the proof, and the exception case is the one that matters most: a credential
usually reaches a log through a provider error rendered into a traceback, not
through a deliberate log call.
"""

from app.core.logging import REDACTED, build_redactor

SECRET = "AIzaSy-not-a-real-key-000000"
SECRETS = frozenset({SECRET})


def _redact(event: dict[str, object]) -> dict[str, object]:
    return dict(build_redactor(SECRETS)(None, "info", event))


def test_secret_in_a_message_is_removed() -> None:
    result = _redact({"event": f"calling provider with {SECRET}"})

    assert SECRET not in str(result)
    assert REDACTED in str(result["event"])


def test_secret_in_a_nested_dict_is_removed() -> None:
    result = _redact({"event": "call", "request": {"headers": {"key": SECRET}}})

    assert SECRET not in str(result)


def test_secret_in_a_list_is_removed() -> None:
    result = _redact({"event": "call", "args": [SECRET, "safe"]})

    assert SECRET not in str(result)
    assert "safe" in str(result)


def test_secret_in_an_exception_is_removed() -> None:
    """The case that catches a credential inside a provider traceback."""
    result = _redact({"event": "failed", "error": ValueError(f"bad key {SECRET}")})

    assert SECRET not in str(result)


def test_no_secrets_configured_leaves_the_event_untouched() -> None:
    """Slice 1 has no secrets, so the processor must be a no-op, not a crash."""
    event = {"event": "hello", "count": 3}

    assert build_redactor(frozenset())(None, "info", dict(event)) == event
