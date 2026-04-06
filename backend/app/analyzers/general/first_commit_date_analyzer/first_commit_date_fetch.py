from app.clients.github_graphql_client import execute_github_graphql_query
from app.analyzers.general.first_commit_date_analyzer.first_commit_date_query import FIRST_COMMIT_DATE_GRAPHQL_QUERY


async def fetch_first_commit_date(
    owner: str,
    repository_name: str,
) -> dict:
    cursor = None
    last_commit_date = None
    branch_name = None
    repository_owner = None
    resolved_repository_name = None

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

        branch_name = default_branch_ref["name"]
        repository_owner = repository["owner"]["login"]
        resolved_repository_name = repository["name"]

        history = default_branch_ref.get("target", {}).get("history", {})
        nodes = history.get("nodes", [])

        if not nodes:
            raise RuntimeError("Could not read commit history for the default branch.")

        last_commit_date = nodes[-1].get("committedDate")
        if last_commit_date is None:
            raise RuntimeError("Could not read committedDate for the first commit.")

        page_info = history.get("pageInfo", {})
        has_next_page = page_info.get("hasNextPage")
        end_cursor = page_info.get("endCursor")

        if not has_next_page:
            break

        cursor = end_cursor

        if cursor is None:
            raise RuntimeError("GitHub pagination did not return an end cursor.")

    return {
        "owner": repository_owner,
        "repository_name": resolved_repository_name,
        "branch_name": branch_name,
        "first_commit_date": last_commit_date[:10],
    }