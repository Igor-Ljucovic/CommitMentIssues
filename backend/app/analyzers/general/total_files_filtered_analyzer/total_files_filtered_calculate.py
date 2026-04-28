from pathlib import PurePosixPath

from app.analyzers.general.total_files_filtered_analyzer.total_files_filtered_constants import (
    SUPPORTED_CODE_FILE_NAMES,
    SUPPORTED_CODE_FILE_EXTENSIONS,
    EXCLUDED_PATH_PARTS,
)
from app.analyzers.general.total_files_analyzer.total_files_constants import (
    TOTAL_FILES_METRIC_KEY
)
from app.analyzers.general.total_files_filtered_analyzer.total_files_filtered_constants import (
    TOTAL_FILES_FILTERED_METRIC_KEY,
    DEFAULT_BRANCH_NAME
)
from app.analyzers.general.total_files_analyzer.total_files_fetch import fetch_total_files
from app.analyzers.common.tree_utils import count_matching_tree_entries


async def total_files_filtered_calculate(
    owner: str,
    repository_name: str,
) -> dict:
    result = await fetch_total_files(
        owner=owner,
        repository_name=repository_name,
    )

    total_files_filtered = count_matching_tree_entries(
        result[TOTAL_FILES_METRIC_KEY], predicate=is_supported_code_file
    )

    print(total_files_filtered)
    print(len(result[TOTAL_FILES_METRIC_KEY]))

    return {
        "owner": result["owner"],
        "repository_name": result["repository_name"],
        DEFAULT_BRANCH_NAME: result[DEFAULT_BRANCH_NAME],
        TOTAL_FILES_METRIC_KEY: len(result[TOTAL_FILES_METRIC_KEY]),
        TOTAL_FILES_FILTERED_METRIC_KEY: total_files_filtered,
    }


def is_supported_code_file(entry: dict) -> bool:
    # blob = file, tree = directory
    if entry.get("type") != "blob":
        return False

    path = entry.get("path")
    if not isinstance(path, str) or not path.strip():
        return False

    normalized_path = path.lower()

    if any(path_part in normalized_path for path_part in EXCLUDED_PATH_PARTS):
        return False

    file_path = PurePosixPath(normalized_path)
    file_name = file_path.name

    if file_name in SUPPORTED_CODE_FILE_NAMES:
        return True

    suffixes = file_path.suffixes

    for index in range(len(suffixes)):
        combined_suffix = "".join(suffixes[index:])
        if combined_suffix in SUPPORTED_CODE_FILE_EXTENSIONS:
            return True

    return False