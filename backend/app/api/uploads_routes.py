from fastapi import APIRouter, File, HTTPException, UploadFile, status

from backend.app.schemas.upload_schemas import UploadResponse
from app.services.file_service import process_uploaded_files

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("", response_model=UploadResponse, status_code=status.HTTP_200_OK)
async def upload_files(files: list[UploadFile] = File(...)) -> UploadResponse:
    try:
        return await process_uploaded_files(files)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc