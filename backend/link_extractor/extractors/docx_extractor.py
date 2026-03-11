from pathlib import Path

from docx import Document

from link_extractor.github_links import (
    clean_url,
    extract_github_links_from_text,
    is_github_url,
)


def extract_links_from_docx(file_path: Path) -> set[str]:
    document = Document(file_path)
    links: set[str] = set()

    visible_text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    links.update(extract_github_links_from_text(visible_text))

    for rel in document.part.rels.values():
        target_ref = getattr(rel, "target_ref", None)
        if isinstance(target_ref, str):
            cleaned_url = clean_url(target_ref)
            if is_github_url(cleaned_url):
                links.add(cleaned_url)

    return links