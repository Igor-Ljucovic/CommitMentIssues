import re
import sys

from tree_sitter import Language, Parser
import tree_sitter_python as tspython

from app.analyzers.code_and_repository_quality.libraries_used_analyzer.detectors.detector_utils import (
    fetch_blob_text,
    walk_nodes,
    get_node_text,
)

_PYTHON_STDLIB: frozenset[str] = frozenset(sys.stdlib_module_names)

_parser: Parser | None = None


def get_local_python_identifiers(tree_items: list) -> frozenset[str]:
    """Returns names that should be treated as local Python identifiers (not 3rd-party)"""
    names: set[str] = set()
    for item in tree_items:
        item_type = item.get("type")
        path = item.get("path", "")
        parts = path.split("/")

        if item_type == "tree":
            names.add(parts[-1])
        elif item_type == "blob":
            filename = parts[-1]
            if filename == "__init__.py" and len(parts) >= 2:
                names.add(parts[-2])
            elif filename.endswith(".py"):
                stem = filename[:-3]
                if stem and stem != "__init__":
                    names.add(stem)
    return frozenset(names)


def parse_python_imports(
    source_code: str,
    local_packages: frozenset[str],
    python_declared: frozenset[str],
) -> set[str]:
    tree = _get_parser().parse(source_code.encode("utf-8"))
    results: set[str] = set()
    for node in walk_nodes(tree.root_node, {"import_statement", "import_from_statement"}):
        if node.type == "import_statement":
            for child in node.children:
                if child.type == "dotted_name":
                    top = get_node_text(child).split(".")[0]
                    if _keep(top, local_packages, python_declared):
                        results.add(top)
                elif child.type == "aliased_import":
                    for sub in child.children:
                        if sub.type == "dotted_name":
                            top = get_node_text(sub).split(".")[0]
                            if _keep(top, local_packages, python_declared):
                                results.add(top)
                            break
        elif node.type == "import_from_statement":
            for child in node.children:
                if child.type == "dotted_name":
                    top = get_node_text(child).split(".")[0]
                    if _keep(top, local_packages, python_declared):
                        results.add(top)
                    break
    return results


async def get_python_declared_packages(
    owner: str,
    repository_name: str,
    tree_items: list,
) -> frozenset[str]:
    """Read requirements.txt/pyproject.toml and return declared package names."""
    declared: set[str] = set()
    config_files = {"requirements.txt", "pyproject.toml"}
    for item in tree_items:
        if item.get("type") != "blob":
            continue
        filename = item.get("path", "").split("/")[-1].lower()
        if filename not in config_files:
            continue
        blob_sha = item.get("sha")
        if not blob_sha:
            continue
        text = await fetch_blob_text(owner, repository_name, blob_sha)
        if not text:
            continue
        if filename == "requirements.txt":
            declared.update(_parse_requirements_txt(text))
        elif filename == "pyproject.toml":
            declared.update(_parse_pyproject_toml(text))
    return frozenset(declared)


def _parse_requirements_txt(content: str) -> set[str]:
    packages: set[str] = set()
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        name = re.split(r"[>=<!;\[\s]", line)[0].strip()
        if name:
            packages.add(name.lower())
    return packages


def _parse_pyproject_toml(content: str) -> set[str]:
    packages: set[str] = set()
    in_deps = False
    for line in content.splitlines():
        stripped = line.strip()
        if re.match(r'^\[.*dependencies.*\]', stripped, re.IGNORECASE):
            in_deps = True
            continue
        if stripped.startswith("[") and in_deps:
            in_deps = False
        if in_deps and stripped and not stripped.startswith("#"):
            name = re.split(r"[>=<!;\[\s\"']", stripped)[0].strip()
            if name:
                packages.add(name.lower())
    return packages


def _get_parser() -> Parser:
    global _parser
    if _parser is None:
        raw = tspython.language()
        lang = raw if isinstance(raw, Language) else Language(raw)
        _parser = Parser(lang)
    return _parser


def _keep(top: str, local_packages: frozenset[str], python_declared: frozenset[str]) -> bool:
    if not top or top in _PYTHON_STDLIB or top in local_packages:
        return False
    if python_declared:
        normalized = top.lower().replace("-", "_")
        return any(d.replace("-", "_") == normalized for d in python_declared)
    return True
