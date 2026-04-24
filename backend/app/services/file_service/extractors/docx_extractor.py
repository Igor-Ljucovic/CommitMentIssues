from io import BytesIO

from docx import Document

from app.services.file_service.github_links import (
    clean_url,
    extract_github_links_from_text,
    is_github_repo_url,
    normalize_github_repo_url,
)


def extract_links_from_docx_bytes(file_bytes: bytes) -> list[str]:
    document = Document(BytesIO(file_bytes))
    links: set[str] = set()

    visible_text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    links.update(extract_github_links_from_text(visible_text))

    for rel in document.part.rels.values():
        target_ref = getattr(rel, "target_ref", None)
        if isinstance(target_ref, str):
            cleaned_url = clean_url(target_ref)
            normalized_url = normalize_github_repo_url(cleaned_url)

            if is_github_repo_url(normalized_url):
                links.add(normalized_url)

    return sorted(links)