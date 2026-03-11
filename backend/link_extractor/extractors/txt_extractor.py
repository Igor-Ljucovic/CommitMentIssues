from pathlib import Path

from link_extractor.github_links import (
    extract_github_links_from_text
)


def extract_links_from_txt(file_path: Path) -> set[str]:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    return extract_github_links_from_text(text)