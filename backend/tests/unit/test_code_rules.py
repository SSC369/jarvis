"""Names, enforced rather than reviewed.

backend/.claude/rules/code-rules.md section 6 bans single-letter and
placeholder variable and parameter names in `app/`. This walks every function
by AST and rejects them, the same way test_layering.py enforces the boundary
rules of repo-rules.md section 6 instead of leaving them to review.
"""

import ast
import pathlib

APP = pathlib.Path("app")

BANNED_NAMES = {
    "a",
    "e",
    "x",
    "s",
    "k",
    "v",
    "this",
    "that",
    "obj",
    "tmp",
    "data",
    "value",
    "res",
    "ret",
}

# Framework-mandated names (Strawberry's resolver argument), and the
# deliberately-unused placeholder. Section 6's own exemption.
EXEMPT_NAMES = {"info", "_"}


def _python_files() -> list[pathlib.Path]:
    return [path for path in APP.rglob("*.py") if path.name != "__init__.py"]


def _class_level_field_targets(tree: ast.AST) -> set[int]:
    """Identity of every `name: Type` target declared directly in a class body.

    A dataclass or Strawberry type field is a public name a caller depends on,
    not a local variable, and section 6 exempts it. Identity, not name, is
    compared: a local variable elsewhere in the same file with the same name is
    still checked.
    """
    targets: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for statement in node.body:
                if isinstance(statement, ast.AnnAssign) and isinstance(
                    statement.target, ast.Name
                ):
                    targets.add(id(statement.target))
    return targets


def _banned_names_in(path: pathlib.Path) -> set[str]:
    tree = ast.parse(path.read_text())
    exempt_targets = _class_level_field_targets(tree)
    found: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.arg):
            if node.arg in BANNED_NAMES and node.arg not in EXEMPT_NAMES:
                found.add(node.arg)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            if id(node) in exempt_targets:
                continue
            if node.id in BANNED_NAMES and node.id not in EXEMPT_NAMES:
                found.add(node.id)

    return found


def test_no_banned_variable_or_parameter_names() -> None:
    offenders = {
        str(path): sorted(names)
        for path in _python_files()
        if (names := _banned_names_in(path))
    }

    assert not offenders, (
        f"{offenders} use a name code-rules.md section 6 bans. "
        "Name the value for what it holds here, not its shape."
    )
