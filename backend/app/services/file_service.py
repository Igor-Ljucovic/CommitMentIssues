from io import BytesIO
from pathlib import Path

from docx import Document
from fastapi import UploadFile
from pypdf import PdfReader

from app.link_extractor.github_links import (
    clean_url,
    extract_github_links_from_text,
    is_github_repo_url,
    normalize_github_repo_url,
)
from backend.app.schemas.upload_schemas import UploadResponse, UploadedFileResponse
from app.utils.file_utils import is_allowed_file

def extract_links_from_txt_bytes(file_bytes: bytes) -> list[str]:
    text = file_bytes.decode("utf-8", errors="ignore")
    return sorted(extract_github_links_from_text(text))

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


def extract_github_links_from_file_bytes(file_name: str, file_bytes: bytes) -> list[str]:
    lower_name = file_name.lower()

    if lower_name.endswith(".txt"):
        return extract_links_from_txt_bytes(file_bytes)

    if lower_name.endswith(".docx"):
        return extract_links_from_docx_bytes(file_bytes)

    if lower_name.endswith(".pdf"):
        return extract_links_from_pdf_bytes(file_bytes)

    raise ValueError(f"Unsupported file type: {file_name}")


async def process_uploaded_files(files: list[UploadFile]) -> UploadResponse:
    if not files:
        raise ValueError("No files were uploaded.")

    rejected_file_names: list[str] = []
    accepted_files = 0
    response_files: list[UploadedFileResponse] = []
    
    for index, file in enumerate(files, start=1):
        file_name = file.filename or ""

        if not file_name or not is_allowed_file(file_name):
            rejected_file_names.append(file_name or "unknown_file")
            continue

        file_bytes = await file.read()
        github_links = extract_github_links_from_file_bytes(file_name, file_bytes)
        accepted_files += 1

        response_files.append(
            UploadedFileResponse(
                id=index,
                original_file_name=file_name,
                github_links=github_links,
            )
        )

    return UploadResponse(
        total_files=len(files),
        accepted_files=accepted_files,
        rejected_file_names=rejected_file_names,
        files=response_files,
    )