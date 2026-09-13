"""The only names other domains may import from identity.

Empty: no other domain needs identity's settings yet. Present per
backend/.claude/rules/repo-rules.md section 6.2 — "a domain with no
``public.py`` may not be imported" — kept as an empty file rather than
omitted, so it exists the day something does need it.
"""

__all__: list[str] = []
