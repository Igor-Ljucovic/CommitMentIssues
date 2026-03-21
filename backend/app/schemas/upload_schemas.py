from pydantic import BaseModel


class UploadedFileResponse(BaseModel):
    id: int
    original_file_name: str
    github_links: list[str]

    class Config:
        from_attributes = True


class UploadResponse(BaseModel):
    total_files: int
    accepted_files: int
    rejected_file_names: list[str]
    files: list[UploadedFileResponse]