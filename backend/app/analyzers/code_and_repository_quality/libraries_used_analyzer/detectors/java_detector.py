import re

from app.analyzers.code_and_repository_quality.libraries_used_analyzer.detectors.detector_utils import (
    fetch_blob_text,
)

_GRADLE_CONFIGS = (
    r'(?:implementation|api|compileOnly|runtimeOnly|'
    r'testImplementation|testCompileOnly|annotationProcessor)'
)


async def get_java_libraries(
    owner: str,
    repository_name: str,
    tree_items: list,
) -> set[str]:
    """Read pom.xml (Maven) and build.gradle (Groovy) files and return 
    declared Maven/Gradle dependencies (since Java projects use 1 of these 2)."""
    libraries: set[str] = set()
    build_files = {"pom.xml", "build.gradle", "build.gradle.kts"}
    for item in tree_items:
        if item.get("type") != "blob":
            continue
        filename = item.get("path", "").split("/")[-1].lower()
        if filename not in build_files:
            continue
        blob_sha = item.get("sha")
        if not blob_sha:
            continue
        text = await fetch_blob_text(owner, repository_name, blob_sha)
        if not text:
            continue
        if filename == "pom.xml":
            libraries.update(_parse_pom_xml_config(text))
        else:
            libraries.update(_parse_build_gradle(text))
    return libraries


def _parse_pom_xml_config(content: str) -> set[str]:
    """Extract groupId:artifactId from <dependency> blocks (skips <parent> and <plugin>)."""
    packages: set[str] = set()
    for dep in re.finditer(r'<dependency>(.*?)</dependency>', content, re.DOTALL | re.IGNORECASE):
        text = dep.group(1)
        g = re.search(r'<groupId>\s*([^<]+?)\s*</groupId>', text, re.IGNORECASE)
        a = re.search(r'<artifactId>\s*([^<]+?)\s*</artifactId>', text, re.IGNORECASE)
        if g and a:
            gid = g.group(1).strip()
            aid = a.group(1).strip()
            if "${" not in gid and "${" not in aid:
                packages.add(f"{gid}:{aid}")
    return packages


def _parse_build_gradle(content: str) -> set[str]:
    """Extract groupId:artifactId from Groovy build.gradle or Kotlin build.gradle.kts."""
    packages: set[str] = set()
    # String notation: implementation 'group:artifact[:version]' or ("g:a[:v]")
    for m in re.finditer(
        _GRADLE_CONFIGS + r"""\s*[\("']+([^"':\s]+):([^"':\s]+)[^"']*["']+""",
        content,
    ):
        packages.add(f"{m.group(1)}:{m.group(2)}")
    for m in re.finditer(
        _GRADLE_CONFIGS + r"""[^'"\n]*group:\s*['"]([^'"]+)['"]\s*,\s*name:\s*['"]([^'"]+)['"]""",
        content,
    ):
        packages.add(f"{m.group(1)}:{m.group(2)}")
    return packages