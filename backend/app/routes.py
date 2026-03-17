from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models import FileScanResult, UploadResponse
from app.utils import is_allowed_file
from main import get_scan_results

router = APIRouter()

UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)


def clear_uploads_folder() -> None:
    for file_path in UPLOADS_DIR.iterdir():
        if file_path.is_file():
            file_path.unlink()

@router.post("/upload", response_model=UploadResponse)
async def upload_files(files: list[UploadFile] = File(...)) -> UploadResponse:
    if not files:
        raise HTTPException(status_code=400, detail="No files were uploaded.")
    
    clear_uploads_folder()
    
    rejected_file_names: list[str] = []
    accepted_count = 0

    for file in files:
        file_name = file.filename or ""

        if not file_name or not is_allowed_file(file_name):
            rejected_file_names.append(file_name or "unknown_file")
            continue

        file_bytes = await file.read()
        save_path = UPLOADS_DIR / file_name
        save_path.write_bytes(file_bytes)
        accepted_count += 1

    scan_results = get_scan_results(UPLOADS_DIR)

    scanned_files: list[FileScanResult] = []

    for file_name, links in sorted(scan_results.items()):
        sorted_links = sorted(links)
        scanned_files.append(
        FileScanResult(
            file_name=Path(file_name).name,
            github_links=sorted_links,
        )
    )

    return UploadResponse(
        total_files=len(files),
        accepted_files=accepted_count,
        rejected_file_names=rejected_file_names,
        scanned_files=scanned_files,
    )