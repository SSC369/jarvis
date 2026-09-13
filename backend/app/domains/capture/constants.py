"""Limits and the extraction contracts for capture. No magic values elsewhere.

Timezone-aware date resolution is a follow-up: slice 2's ``user_settings``
does not exist yet, so every relative date resolves against server UTC. The
adapter appends the reference moment; neither schema mentions it.

**Schema descriptions are kept terse on purpose.** A verbose description on
the ``due_at`` field was measured adding enough generation latency to push a
call from ~5.4s to ~10.7s, past the 8 second budget (NFR-2), with no gain in
accuracy. The detailed guidance lives in the instruction text instead, which
does not carry the same cost. See the dev log, slice 1.
"""

from typing import Any, Final

# Build plan AD-4. Every drawn example in 02-design.md is well under this, and
# it protects the gateway's TPM headroom cheaply.
MAX_INPUT_LENGTH: Final = 500

# The two commands this epic ships. FR-24 (narrowed 2026-09-13): completing,
# editing and deleting a task are records-view actions only, never commands.
KNOWN_COMMANDS: Final[tuple[str, ...]] = ("/add-task", "/tasks")

TASK_EXTRACTION_SCHEMA: Final[dict[str, Any]] = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "due_at": {"type": "string", "description": "ISO date if one is implied"},
    },
    "required": ["title"],
}

TASK_EXTRACTION_INSTRUCTION: Final = (
    "Extract the task title and, if implied, when it is due, as an absolute "
    "ISO 8601 datetime. Omit due_at if no date or time is implied."
)

# Used only to resolve the answer to a pending due-date question (FR-37,
# FR-38), where the answer is a date phrase with no task title in it, so the
# task schema's required "title" would not fit.
DUE_AT_ONLY_SCHEMA: Final[dict[str, Any]] = {
    "type": "object",
    "properties": {"due_at": {"type": "string"}},
    "required": ["due_at"],
}

DUE_AT_ONLY_INSTRUCTION: Final = (
    'The input answers "when is this due". Resolve it to an absolute ISO 8601 datetime.'
)
