from app.analyzers.general.total_files_analyzer.total_files_constants import (
    DEFAULT_BRANCH_NAME,
    TOTAL_FILES_METRIC_KEY,
)
from app.analyzers.common.tree_utils import (
    count_matching_tree_entries,
)
from app.services.github_rest_service import fetch_github_rest_resource


async def fetch_total_files(
    owner: str,
    repository_name: str,
) -> dict:
    repository_data = await fetch_github_rest_resource(
        f"/repos/{owner}/{repository_name}"
    )

    default_branch = repository_data.get("default_branch")
    if not default_branch:
        raise RuntimeError("Could not determine the repository default branch.")

    # "tree" - list of all items in the repository (in the JSON format)
    tree_data = await fetch_github_rest_resource(
        f"/repos/{owner}/{repository_name}/git/trees/{default_branch}",
        params={"recursive": "1"},
    )

    if tree_data.get("truncated") is True:
        raise RuntimeError(
            "Repository tree is too large for a single recursive Git tree request."
        )

    tree_entries = tree_data.get("tree")
    if not isinstance(tree_entries, list):
        raise RuntimeError("Could not read repository tree entries.")

    total_files =  total_files = count_matching_tree_entries(
        tree_entries,
        # Blob = file, tree = directory
        predicate=lambda entry: entry.get("type") == "blob"
    )

    return {
        # "login" = GitHub username/organization name
        "owner": repository_data.get("owner", {}).get("login", owner),
        "repository_name": repository_data.get("name", repository_name),
        DEFAULT_BRANCH_NAME: default_branch,
        TOTAL_FILES_METRIC_KEY: total_files,
        # "tree_entries": tree_entries,
    }