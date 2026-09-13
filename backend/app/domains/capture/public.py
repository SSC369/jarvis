"""The only names other domains may import from capture.

Empty: nothing consumes capture yet. Kept for anatomy consistency with every
other domain, per backend/.claude/rules/repo-rules.md section 5 — a domain
with no public.py exposes nothing and may not be imported, per section 6.2,
so the file exists even though its contract is empty.
"""

__all__: list[str] = []
