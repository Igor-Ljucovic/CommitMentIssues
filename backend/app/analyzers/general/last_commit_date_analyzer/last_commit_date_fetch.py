from app.services.github_graphql_service import fetch_github_graphql_resource
from app.analyzers.general.last_commit_date_analyzer.last_commit_date_query import (
    LAST_COMMIT_DATE_GRAPHQL_QUERY,
)
from app.analyzers.general.last_commit_date_analyzer.last_commit_date_constants import (
    LAST_COMMIT_DATE_METRIC_KEY,
    BRANCH_NAME,
)


async def fetch_last_commit_date(
    owner: str,
    repository_name: str,
) -> dict:
    repository = await fetch_github_graphql_resource(
        query=LAST_COMMIT_DATE_GRAPHQL_QUERY,
        variables={
            "owner": owner,
            "name": repository_name,
        },
    )

    default_branch_ref = repository.get("defaultBranchRef")
    if default_branch_ref is None:
        raise ValueError("Repository does not have a default branch.")

    history = default_branch_ref.get("target", {}).get("history")
    if history is None:
        raise RuntimeError("Could not read commit history for the default branch.")

    nodes = history.get("nodes", [])
    if not nodes:
        raise RuntimeError("No commits found in repository.")

    latest_commit_date = nodes[0].get("committedDate")
    if latest_commit_date is None:
        raise RuntimeError("Could not read committedDate for the last commit.")

    return {
        "owner": repository["owner"]["login"],
        "repository_name": repository["name"],
        BRANCH_NAME: default_branch_ref["name"],
        LAST_COMMIT_DATE_METRIC_KEY: latest_commit_date[:10],  # YYYY-MM-DD
    }