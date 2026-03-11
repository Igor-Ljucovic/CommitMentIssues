from pydantic import BaseModel


class FileScanResult(BaseModel):
    file_name: str
    github_links: list[str]


class UploadResponse(BaseModel):
    total_files: int
    accepted_files: int
    rejected_files: int
    rejected_file_names: list[str]
    scanned_files: list[FileScanResult]
    unique_github_links: list[str]