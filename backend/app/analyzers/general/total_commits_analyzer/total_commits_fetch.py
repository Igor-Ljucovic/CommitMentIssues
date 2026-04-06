from app.clients.github_graphql_client import execute_github_graphql_query
from app.analyzers.general.total_commits_analyzer.total_commits_query import TOTAL_COMMITS_GRAPHQL_QUERY


async def fetch_total_commits(
    owner: str,
    repository_name: str,
) -> dict:
    repository = await execute_github_graphql_query(
        query=TOTAL_COMMITS_GRAPHQL_QUERY,
        variables={
            "owner": owner,
            "name": repository_name,
        },
    )

    default_branch_ref = repository.get("defaultBranchRef")
    if default_branch_ref is None:
        raise ValueError("Repository does not have a default branch.")

    history = default_branch_ref.get("target", {}).get("history", {})
    total_commits = history.get("totalCount")

    if total_commits is None:
        raise RuntimeError("Could not read commit history for the default branch.")

    return {
        "owner": repository["owner"]["login"],
        "repository_name": repository["name"],
        "branch_name": default_branch_ref["name"],
        "total_commits": total_commits,
    }