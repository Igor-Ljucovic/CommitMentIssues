import os
import tarfile
from pathlib import Path

from app.analyzers.general.total_lines_of_code_filtered_analyzer.total_lines_of_code_filtered_constants import (
    COUNTED_FILES,
    DEFAULT_BRANCH_NAME,
    EXCLUDED_FILE_EXTENSIONS,
    EXCLUDED_FILE_NAMES,
    EXCLUDED_PATH_PARTS,
    SKIPPED_FILES,
    SUPPORTED_CODE_FILE_EXTENSIONS,
    SUPPORTED_CODE_FILE_NAMES,
    TOTAL_LINES_OF_CODE_FILTERED_METRIC_KEY,
)
from app.core.config import GITHUB_REPOS_DIR
from app.services.github_rest_service import (
    fetch_github_rest_resource,
    download_github_tarball,
)


async def fetch_total_lines_of_code_filtered(
    owner: str,
    repository_name: str,
    tarball_path: Path | None = None,
) -> dict:
    default_branch: str | None = None

    if tarball_path is None:
        repository_data = await fetch_github_rest_resource(
            f"/repos/{owner}/{repository_name}"
        )
        default_branch = repository_data.get("default_branch")
        if not default_branch:
            raise RuntimeError("Could not determine the repository default branch.")

        GITHUB_REPOS_DIR.mkdir(parents=True, exist_ok=True)
        tarball_path = GITHUB_REPOS_DIR / f"{owner}-{repository_name}.tar.gz"

        if not tarball_path.exists():
            await download_github_tarball(
                f"/repos/{owner}/{repository_name}/tarball/{default_branch}",
                tarball_path,
            )

    total_lines_of_code = 0
    counted_files = 0
    skipped_files = 0

    with tarfile.open(tarball_path, mode="r:gz") as tar:
        for member in tar:
            if not member.isfile():
                continue

            name = member.name
            slash_idx = name.find("/")
            if slash_idx == -1:
                continue
            path = name[slash_idx + 1:]
            if not path:
                continue

            if not _is_supported_code_file(path):
                skipped_files += 1
                continue

            file_obj = tar.extractfile(member)
            if file_obj is None:
                continue

            line_count, is_text_file = _count_newlines_from_bytes(file_obj.read())

            if not is_text_file:
                skipped_files += 1
                continue

            total_lines_of_code += line_count
            counted_files += 1

    return {
        TOTAL_LINES_OF_CODE_FILTERED_METRIC_KEY: total_lines_of_code,
        COUNTED_FILES: counted_files,
        SKIPPED_FILES: skipped_files,
        DEFAULT_BRANCH_NAME: default_branch,
        "tarball_path": tarball_path,
    }


def _is_supported_code_file(path: str) -> bool:
    for part in EXCLUDED_PATH_PARTS:
        if part in path:
            return False

    filename = path.split("/")[-1].lower()
    name_no_ext, ext = os.path.splitext(filename)

    if filename in EXCLUDED_FILE_NAMES or name_no_ext in EXCLUDED_FILE_NAMES:
        return False

    if ext in EXCLUDED_FILE_EXTENSIONS:
        return False

    if filename in SUPPORTED_CODE_FILE_NAMES:
        return True

    return ext in SUPPORTED_CODE_FILE_EXTENSIONS


def _count_newlines_from_bytes(blob_bytes: bytes) -> tuple[int, bool]:
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
