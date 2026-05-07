import os
import tarfile
from pathlib import Path

from app.analyzers.code_and_repository_quality.libraries_used_analyzer.libraries_used_constants import (
    EXTENSION_TO_LANGUAGE,
)
from app.analyzers.code_and_repository_quality.libraries_used_analyzer.detectors.python_detector import (
    get_local_python_identifiers_from_paths,
    get_python_declared_packages_from_content,
    parse_python_imports,
)
from app.analyzers.code_and_repository_quality.libraries_used_analyzer.detectors.javascript_detector import (
    get_js_declared_packages_from_content,
    parse_javascript_imports,
)
from app.analyzers.code_and_repository_quality.libraries_used_analyzer.detectors.csharp_detector import (
    get_csharp_libraries_from_content,
)
from app.analyzers.code_and_repository_quality.libraries_used_analyzer.detectors.java_detector import (
    get_java_libraries_from_content,
)

_CONFIG_FILENAMES = frozenset({
    "requirements.txt", "pyproject.toml",
    "package.json",
    "pom.xml", "build.gradle", "build.gradle.kts",
})


def fetch_libraries_used(tarball_path: Path) -> dict[str, set[str]]:
    all_paths: list[str] = []
    config_contents: dict[str, list[str]] = {name: [] for name in _CONFIG_FILENAMES}
    csproj_contents: list[str] = []
    source_files: list[tuple[str, str, str]] = []

    with tarfile.open(tarball_path, mode="r:gz") as tar:
        for member in tar:
            if not member.isfile():
                continue

            # GitHub tarballs prefix every path with a single top-level dir; strip it.
            name = member.name
            slash_idx = name.find("/")
            if slash_idx == -1:
                continue
            path = name[slash_idx + 1:]
            if not path:
                continue

            all_paths.append(path)

            file_obj = tar.extractfile(member)
            if file_obj is None:
                continue

            raw = file_obj.read()
            if b"\x00" in raw:
                continue

            try:
                content = raw.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    content = raw.decode("utf-8-sig")
                except UnicodeDecodeError:
                    continue

            filename = path.split("/")[-1].lower()
            _, ext = os.path.splitext(filename)

            if filename in _CONFIG_FILENAMES:
                config_contents[filename].append(content)
            elif filename.endswith(".csproj"):
                csproj_contents.append(content)
            else:
                language = EXTENSION_TO_LANGUAGE.get(ext)
                if language in ("python", "javascript"):
                    source_files.append((path, content, language))

    local_python = get_local_python_identifiers_from_paths(all_paths)
    python_declared = get_python_declared_packages_from_content(
        config_contents["requirements.txt"],
        config_contents["pyproject.toml"],
    )
    js_declared = get_js_declared_packages_from_content(config_contents["package.json"])
    csharp_libs = get_csharp_libraries_from_content(csproj_contents)
    java_libs = get_java_libraries_from_content(
        config_contents["pom.xml"],
        config_contents["build.gradle"] + config_contents["build.gradle.kts"],
    )

    libraries_by_language: dict[str, set[str]] = {
        lang: set() for lang in set(EXTENSION_TO_LANGUAGE.values())
    }
    libraries_by_language["csharp"] = csharp_libs
    libraries_by_language["java"] = java_libs

    for path, content, language in source_files:
        if language == "python":
            imports = parse_python_imports(content, local_python, python_declared)
        elif language == "javascript":
            imports = parse_javascript_imports(content, js_declared)
        libraries_by_language[language].update(imports)

    return libraries_by_language
