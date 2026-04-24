from pathlib import Path

ALLOWED_EXTENSIONS = {".txt", ".docx", ".pdf"}


def get_file_extension(file_name: str) -> str:
    return Path(file_name).suffix.lower()


def is_allowed_file(file_name: str) -> bool:
    return get_file_extension(file_name) in ALLOWED_EXTENSIONS