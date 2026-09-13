"""Limits and defaults for identity. No magic values elsewhere."""

from typing import Final

# Used only if the browser could not detect a timezone at all (Intl throws or
# returns undefined) and the client omits detectedTimezone entirely.
DEFAULT_TIMEZONE: Final = "UTC"
