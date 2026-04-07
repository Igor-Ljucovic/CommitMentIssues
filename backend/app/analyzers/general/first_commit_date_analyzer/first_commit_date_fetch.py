from app.clients.github_graphql_client import execute_github_graphql_query
from app.analyzers.general.first_commit_date_analyzer.first_commit_date_query import (
    FIRST_COMMIT_DATE_GRAPHQL_QUERY,
)
from app.analyzers.general.first_commit_date_analyzer.first_commit_date_constants import (
    FIRST_COMMIT_DATE_METRIC_KEY,
    BRANCH_NAME
)


async def fetch_first_commit_date(
    owner: str,
    repository_name: str,
) -> dict:
    cursor = None
    oldest_commit_date_seen = None

    while True:
        repository = await execute_github_graphql_query(
            query=FIRST_COMMIT_DATE_GRAPHQL_QUERY,
            variables={
                "owner": owner,
                "name": repository_name,
                "cursor": cursor,
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
            raise RuntimeError("Could not read commit history for the default branch.")

        oldest_commit_date_seen = nodes[-1].get("committedDate")
        if oldest_commit_date_seen is None:
            raise RuntimeError("Could not read committedDate for the first commit.")

        page_info = history.get("pageInfo", {})
        if not page_info.get("hasNextPage"):
            return {
                "owner": repository["owner"]["login"],
                "repository_name": repository["name"],
                BRANCH_NAME: default_branch_ref["name"],
                # [:10] for 1st 10 chars only (YYYY-MM-DD)
                FIRST_COMMIT_DATE_METRIC_KEY: oldest_commit_date_seen[:10],
            }

        cursor = page_info.get("endCursor")
        if cursor is None:
            raise RuntimeError("GitHub pagination did not return an end cursor.")