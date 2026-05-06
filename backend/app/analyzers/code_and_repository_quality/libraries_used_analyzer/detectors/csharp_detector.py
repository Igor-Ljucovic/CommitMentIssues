import re


def get_csharp_libraries_from_content(csproj_contents: list[str]) -> set[str]:
    libraries: set[str] = set()
    for content in csproj_contents:
        libraries.update(_parse_csproj_config(content))
    return libraries


def _parse_csproj_config(content: str) -> set[str]:
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
