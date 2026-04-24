from io import BytesIO

from pypdf import PdfReader

from app.services.file_service.github_links import (
    clean_url,
    extract_github_links_from_text,
    is_github_repo_url,
    normalize_github_repo_url,
)


def extract_links_from_pdf_bytes(file_bytes: bytes) -> list[str]:
    reader = PdfReader(BytesIO(file_bytes))
    links: set[str] = set()

    for page in reader.pages:
        text = page.extract_text()
        if text:
            links.update(extract_github_links_from_text(text))

        annotations = page.get("/Annots")
        if not annotations:
            continue

        for annotation in annotations:
            try:
                annotation_object = annotation.get_object()
                action = annotation_object.get("/A")

                if action and action.get("/S") == "/URI":
                    uri = action.get("/URI")
                    if isinstance(uri, str):
                        cleaned_url = clean_url(uri)
                        normalized_url = normalize_github_repo_url(cleaned_url)

                        if is_github_repo_url(normalized_url):
                            links.add(normalized_url)
            except Exception:
                continue

    return sorted(links)