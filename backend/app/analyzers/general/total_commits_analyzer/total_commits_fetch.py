from app.services.github_graphql_service import fetch_github_graphql_resource
from app.analyzers.general.total_commits_analyzer.total_commits_query import (
    TOTAL_COMMITS_GRAPHQL_QUERY,
)
from app.analyzers.general.total_commits_analyzer.total_commits_constants import (
    TOTAL_COMMITS_METRIC_KEY,
    BRANCH_NAME
)


async def fetch_total_commits(
    owner: str,
    repository_name: str,
) -> dict:
    repository = await fetch_github_graphql_resource(
        query=TOTAL_COMMITS_GRAPHQL_QUERY,
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

    total_commits = history.get("totalCount")
    if total_commits is None:
        raise RuntimeError("Could not read commit history for the default branch.")

    return {
        "owner": repository["owner"]["login"],
        "repository_name": repository["name"],
        BRANCH_NAME: default_branch_ref["name"],
        TOTAL_COMMITS_METRIC_KEY: total_commits,
    }