import asyncio
import os

from app.analyzers.code_and_repository_quality.libraries_used_analyzer.libraries_used_constants import (
    EXTENSION_TO_LANGUAGE,
)
from app.analyzers.code_and_repository_quality.libraries_used_analyzer.detectors.detector_utils import (
    fetch_with_retry,
    fetch_blob_text,
)
from app.analyzers.code_and_repository_quality.libraries_used_analyzer.detectors.python_detector import (
    get_local_python_identifiers,
    get_python_declared_packages,
    parse_python_imports,
)
from app.analyzers.code_and_repository_quality.libraries_used_analyzer.detectors.javascript_detector import (
    get_js_declared_packages,
    parse_javascript_imports,
)
from app.analyzers.code_and_repository_quality.libraries_used_analyzer.detectors.csharp_detector import (
    get_csharp_libraries,
)
from app.analyzers.code_and_repository_quality.libraries_used_analyzer.detectors.java_detector import (
    get_java_libraries,
)


async def fetch_libraries_used(
    owner: str,
    repository_name: str,
) -> dict[str, set[str]]:
    repository_data = await fetch_with_retry(f"/repos/{owner}/{repository_name}")

    default_branch = repository_data.get("default_branch")
    if not default_branch:
        raise RuntimeError("Could not determine the repository default branch.")

    tree_data = await fetch_with_retry(
        f"/repos/{owner}/{repository_name}/git/trees/{default_branch}",
        params={"recursive": "1"},
    )
    tree_items = tree_data.get("tree", [])

    # Fetch all config-based language libraries lists in parallel
    csharp_libs, python_declared, js_declared, java_libs = await asyncio.gather(
        get_csharp_libraries(owner, repository_name, tree_items),
        get_python_declared_packages(owner, repository_name, tree_items),
        get_js_declared_packages(owner, repository_name, tree_items),
        get_java_libraries(owner, repository_name, tree_items),
    )

    libraries_by_language: dict[str, set[str]] = {
        lang: set() for lang in set(EXTENSION_TO_LANGUAGE.values())
    }
    libraries_by_language["csharp"] = csharp_libs
    libraries_by_language["java"] = java_libs

    # Tree-sitter parsing for Python and JavaScript (C# and Java are config-only)
    local_python = get_local_python_identifiers(tree_items)
    for item in tree_items:
        if item.get("type") != "blob":
            continue

        path = item.get("path", "")
        _, ext = os.path.splitext(path.lower())
        language = EXTENSION_TO_LANGUAGE.get(ext)
        if language is None or language in ("csharp", "java"):
            continue

        blob_sha = item.get("sha")
        if not blob_sha:
            continue

        source_code = await fetch_blob_text(owner, repository_name, blob_sha)
        if source_code is None:
            continue

        if language == "python":
            imports = parse_python_imports(source_code, local_python, python_declared)
        elif language == "javascript":
            imports = parse_javascript_imports(source_code, js_declared)
        else:
            continue

        libraries_by_language[language].update(imports)

    return libraries_by_language
