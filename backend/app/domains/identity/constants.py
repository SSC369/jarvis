"""Limits and defaults for identity. No magic values elsewhere."""

from datetime import timedelta
from typing import Final

# Used only if the browser could not detect a timezone at all (Intl throws or
# returns undefined) and the client omits detectedTimezone entirely.
DEFAULT_TIMEZONE: Final = "UTC"

# FR-8: how long an account may sit unverified before purge_unverified_accounts
# (jobs.py) removes it, freeing its email for a later signup.
UNVERIFIED_ACCOUNT_TTL: Final = timedelta(hours=24)
