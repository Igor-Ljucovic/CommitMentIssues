from pathlib import Path

from link_extractor.extractors import (
    extract_links_from_docx,
    extract_links_from_pdf,
    extract_links_from_txt,
)


SUPPORTED_EXTENSIONS = {".txt", ".docx", ".pdf"}


def extract_links_by_file_type(file_path: Path) -> set[str]:
    suffix = file_path.suffix.lower()

    if suffix == ".txt":
        return extract_links_from_txt(file_path)

    if suffix == ".docx":
        return extract_links_from_docx(file_path)

    if suffix == ".pdf":
        return extract_links_from_pdf(file_path)

    raise ValueError(f"Unsupported file type: {suffix}")


def scan_folder(folder_path: Path) -> dict[str, set[str]]:
    results: dict[str, set[str]] = {}

    for file_path in folder_path.rglob("*"):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            links = extract_links_by_file_type(file_path)
            if links:
                results[str(file_path)] = links
        except Exception as exc:
            print(f"Skipping {file_path} because of error: {exc}")

    return results