"""Settings cases. See 04.1-api-skeleton.md section 7."""

import pytest
from pydantic import ValidationError

from app.core.settings import Settings


def test_unknown_key_is_rejected() -> None:
    """T-1.4: a key Settings does not declare stops the process."""
    with pytest.raises(ValidationError):
        Settings(unexpected_key="value")  # type: ignore[call-arg]


def test_invalid_environment_is_rejected() -> None:
    """T-1.3: a value outside the allowed set stops the process."""
    with pytest.raises(ValidationError):
        Settings(environment="prod")  # type: ignore[arg-type]


def test_invalid_log_level_is_rejected() -> None:
    """A misspelled log level is caught at startup, not at the first log call."""
    with pytest.raises(ValidationError):
        Settings(log_level="VERBOSE")  # type: ignore[arg-type]


def test_database_password_is_redactable() -> None:
    """The database password is tracked so the log redactor strips it.

    A connection error renders the DSN, and the DSN carries the password. This
    replaces the slice 1 case that asserted no secrets existed. Slice 3 adds the
    provider credential and extends this.
    """
    secrets = Settings().secret_values()

    assert secrets, "the database password must be tracked for redaction"
    assert all(s for s in secrets), "an empty string would redact everything"
