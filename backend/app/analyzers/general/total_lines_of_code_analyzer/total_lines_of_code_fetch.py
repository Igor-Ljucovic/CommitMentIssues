import io
import tarfile

from app.analyzers.general.total_lines_of_code_analyzer.total_lines_of_code_constants import (
    COUNTED_FILES,
    DEFAULT_BRANCH_NAME,
    SKIPPED_BINARY_FILES,
    TOTAL_LINES_OF_CODE_METRIC_KEY,
)
from app.services.github_rest_service import (
    fetch_github_rest_resource,
    fetch_github_rest_bytes,
)


async def fetch_total_lines_of_code(
    owner: str,
    repository_name: str,
) -> dict:
    repository_data = await fetch_github_rest_resource(
        f"/repos/{owner}/{repository_name}"
    )

    default_branch = repository_data.get("default_branch")
    if not default_branch:
        raise RuntimeError("Could not determine the repository default branch.")

    # Single request for the entire repo content (tar file from GitHub's CDN).
    tarball_bytes = await fetch_github_rest_bytes(
        f"/repos/{owner}/{repository_name}/tarball/{default_branch}"
    )

    total_lines_of_code = 0
    counted_files = 0
    skipped_binary_files = 0

    with tarfile.open(fileobj=io.BytesIO(tarball_bytes), mode="r:gz") as tar:
        for member in tar:
            if not member.isfile():
                continue

            file_obj = tar.extractfile(member)
            if file_obj is None:
                continue

            file_bytes = file_obj.read()
            line_count, is_text_file = count_lines_from_bytes(file_bytes)

            if not is_text_file:
                skipped_binary_files += 1
                continue

            total_lines_of_code += line_count
            counted_files += 1

    return {
        "owner": repository_data.get("owner", {}).get("login", owner),
        "repository_name": repository_data.get("name", repository_name),
        DEFAULT_BRANCH_NAME: default_branch,
        COUNTED_FILES: counted_files,
        SKIPPED_BINARY_FILES: skipped_binary_files,
        TOTAL_LINES_OF_CODE_METRIC_KEY: total_lines_of_code,
    }


def count_lines_from_bytes(blob_bytes: bytes) -> tuple[int, bool]:
    # Counts total number of \n-s, not actual lines of code
    if not blob_bytes:
        return 0, True

    # Null byte presence is a reliable binary-file heuristic.
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