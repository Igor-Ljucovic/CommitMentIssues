from pathlib import Path

from pypdf import PdfReader

from link_extractor.github_links import (
    clean_url,
    extract_github_links_from_text,
    is_github_url,
)


def extract_links_from_pdf(file_path: Path) -> set[str]:
    reader = PdfReader(str(file_path))
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
                        if is_github_url(cleaned_url):
                            links.add(cleaned_url)
            except Exception:
                continue

    return links