import re

from app.analyzers.code_and_repository_quality.libraries_used_analyzer.detectors.detector_utils import (
    fetch_blob_text,
)


def parse_csproj_config(content: str) -> set[str]:
    """Extract NuGet package names from <PackageReference Include="..."> entries."""
    packages: set[str] = set()
    for match in re.finditer(
        r'<PackageReference\s+[^>]*Include\s*=\s*"([^"]+)"',
        content,
        re.IGNORECASE,
    ):
        name = match.group(1).strip()
        if name:
            packages.add(name)
    return packages


async def get_csharp_libraries(
    owner: str,
    repository_name: str,
    tree_items: list,
) -> set[str]:
    """Read all .csproj files and return declared NuGet package names."""
    libraries: set[str] = set()
    for item in tree_items:
        if item.get("type") != "blob":
            continue
        if not item.get("path", "").endswith(".csproj"):
            continue
        blob_sha = item.get("sha")
        if not blob_sha:
            continue
        text = await fetch_blob_text(owner, repository_name, blob_sha)
        if text:
            libraries.update(parse_csproj_config(text))
    return libraries
