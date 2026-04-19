from pathlib import PurePosixPath

from app.analyzers.general.total_files_filtered_analyzer.total_files_filtered_constants import (
    SUPPORTED_CODE_FILE_NAMES,
    SUPPORTED_CODE_FILE_EXTENSIONS,
    EXCLUDED_PATH_PARTS,
)


def total_files_filtered_calculate(tree_entries):
    return sum(
            1
            for entry in tree_entries
            if _should_count_file(entry)
        )


def _should_count_file(entry: dict) -> bool:
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