import re

_GRADLE_CONFIGS = (
    r'(?:implementation|api|compileOnly|runtimeOnly|'
    r'testImplementation|testCompileOnly|annotationProcessor)'
)


def get_java_libraries_from_content(
    pom_xml_contents: list[str],
    gradle_contents: list[str],
) -> set[str]:
    libraries: set[str] = set()
    for content in pom_xml_contents:
        libraries.update(_parse_pom_xml_config(content))
    for content in gradle_contents:
        libraries.update(_parse_build_gradle(content))
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
