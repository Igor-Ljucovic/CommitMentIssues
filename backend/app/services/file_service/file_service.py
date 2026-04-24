from fastapi import UploadFile

from app.schemas.upload_schemas import UploadResponse, UploadedFileResponse

from app.services.file_service.extractors.txt_extractor import extract_links_from_txt_bytes
from app.services.file_service.extractors.docx_extractor import extract_links_from_docx_bytes
from app.services.file_service.extractors.pdf_extractor import extract_links_from_pdf_bytes
from app.services.file_service.file_utils import is_allowed_file, get_file_extension


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


def extract_github_links_from_file_bytes(file_name: str, file_bytes: bytes) -> list[str]:
    ext = get_file_extension(file_name)

    if ext == ".txt":
        return extract_links_from_txt_bytes(file_bytes)

    if ext == ".docx":
        return extract_links_from_docx_bytes(file_bytes)

    if ext == ".pdf":
        return extract_links_from_pdf_bytes(file_bytes)

    raise ValueError(f"Unsupported file type: {file_name}")