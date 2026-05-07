import tarfile
from pathlib import Path

from app.analyzers.general.total_lines_of_code_analyzer.total_lines_of_code_constants import (
    COUNTED_FILES,
    SKIPPED_BINARY_FILES,
    TOTAL_LINES_OF_CODE_METRIC_KEY,
)


def fetch_total_lines_of_code(tarball_path: Path) -> dict:
    total_lines_of_code = 0
    counted_files = 0
    skipped_binary_files = 0

    with tarfile.open(tarball_path, mode="r:gz") as tar:
        for member in tar:
            if not member.isfile():
                continue

            file_obj = tar.extractfile(member)
            if file_obj is None:
                continue

            file_bytes = file_obj.read()
            line_count, is_text_file = count_newlines_from_bytes(file_bytes)

            if not is_text_file:
                skipped_binary_files += 1
                continue

            total_lines_of_code += line_count
            counted_files += 1

    return {
        COUNTED_FILES: counted_files,
        SKIPPED_BINARY_FILES: skipped_binary_files,
        TOTAL_LINES_OF_CODE_METRIC_KEY: total_lines_of_code,
    }


def count_newlines_from_bytes(blob_bytes: bytes) -> tuple[int, bool]:
    """Counts total number of newline characters, not actual lines of code"""
    if not blob_bytes:
        return 0, True

    if b"\x00" in blob_bytes:
        return 0, False

    try:
        text = blob_bytes.decode("utf-8")
    except UnicodeDecodeError:
        try:
            text = blob_bytes.decode("utf-8-sig")
        except UnicodeDecodeError:
            return 0, False

    return len(text.splitlines()), True
