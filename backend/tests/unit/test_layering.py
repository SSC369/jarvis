"""Structural rules, enforced rather than reviewed.

Every case here corresponds to a rule in backend/.claude/rules/repo-rules.md that
was previously only prose. The first one exists because the prose did not stop
the gateway's Gemini client being written into `adapters/`, where section 6
reserves that folder for the cross-domain anticorruption layer.

A rule nobody can break by accident does not need a test. These are the ones you
can.
"""

import ast
import pathlib

DOMAINS = pathlib.Path("app/domains")
VENDOR_ROOTS = {
    "langchain_core",
    "langchain_google_genai",
    "google",
    "openai",
    "anthropic",
}


def _imports(path: pathlib.Path) -> list[str]:
    tree = ast.parse(path.read_text())
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
        elif isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
    return names


def _modules(*parts: str) -> list[pathlib.Path]:
    return [
        p
        for p in DOMAINS.glob("/".join(("*", *parts)))
        if p.suffix == ".py" and p.name != "__init__.py"
    ]


def test_adapters_exist_only_to_reach_another_domain() -> None:
    """Section 6: `adapters/` is the cross-domain anticorruption layer.

    A file there that imports no other domain's `public.py` is not an adapter. It
    is a service in the wrong folder, which is what section 6.4 warns about when
    it says two different things get called adapters.
    """
    offenders = [
        str(module)
        for module in _modules("adapters", "*.py")
        if not any(
            i.startswith("app.domains.") and i.endswith(".public")
            for i in _imports(module)
        )
    ]

    assert not offenders, (
        f"{offenders} sit in adapters/ but reach no other domain. "
        "A vendor client belongs in services/, per section 4."
    )


def test_only_services_and_adapters_touch_a_vendor_sdk() -> None:
    """Section 4: interactors never call a vendor directly."""
    offenders = []
    for module in DOMAINS.rglob("*.py"):
        if module.parent.name in {"services", "adapters"}:
            continue
        vendors = {i.split(".")[0] for i in _imports(module)} & VENDOR_ROOTS
        if vendors:
            offenders.append(f"{module} imports {sorted(vendors)}")

    assert not offenders, offenders


def test_domains_reach_each_other_only_through_public() -> None:
    """Section 6.2: nothing but `public.py` may cross a domain boundary."""
    offenders = []
    for module in DOMAINS.rglob("*.py"):
        own_domain = module.relative_to(DOMAINS).parts[0]
        for imported in _imports(module):
            if not imported.startswith("app.domains."):
                continue
            other = imported.split(".")[2]
            if other != own_domain and not imported.endswith(".public"):
                offenders.append(f"{module} imports {imported}")

    assert not offenders, offenders


def test_domain_dependencies_are_acyclic() -> None:
    """Section 6.3: a cycle means two domains are one wearing two names."""
    edges: dict[str, set[str]] = {}
    for module in DOMAINS.rglob("*.py"):
        own = module.relative_to(DOMAINS).parts[0]
        for imported in _imports(module):
            if imported.startswith("app.domains."):
                other = imported.split(".")[2]
                if other != own:
                    edges.setdefault(own, set()).add(other)

    def reaches(start: str, target: str, seen: set[str]) -> bool:
        for nxt in edges.get(start, set()):
            if nxt == target:
                return True
            if nxt not in seen and reaches(nxt, target, seen | {nxt}):
                return True
        return False

    cycles = [
        f"{a} <-> {b}" for a, outs in edges.items() for b in outs if reaches(b, a, {b})
    ]

    assert not cycles, cycles


def test_every_domain_publishes_a_contract() -> None:
    """Section 6.2: a domain with no `public.py` exposes nothing."""
    missing = [
        d.name
        for d in DOMAINS.iterdir()
        if d.is_dir() and d.name != "__pycache__" and not (d / "public.py").exists()
    ]

    assert not missing, f"{missing} have no public.py, so nothing may import them"
