from app.clients.github_graphql_client import execute_github_graphql_query
from app.analyzers.collaboration.pull_request_acceptance_rate_analyzer.pull_request_acceptance_rate_query import PULL_REQUEST_ACCEPTANCE_RATE_GRAPHQL_QUERY


async def fetch_pull_request_acceptance_rate(
    owner: str,
    repository_name: str,
) -> dict:
    repository = await execute_github_graphql_query(
        query=PULL_REQUEST_ACCEPTANCE_RATE_GRAPHQL_QUERY,
        variables={
            "owner": owner,
            "name": repository_name,
        },
    )

    merged_pull_request_count = (
        repository.get("mergedPullRequests", {}).get("totalCount")
    )
    closed_unmerged_pull_request_count = (
        repository.get("closedPullRequests", {}).get("totalCount")
    )

    if merged_pull_request_count is None or closed_unmerged_pull_request_count is None:
        raise RuntimeError("Could not read pull request counts from GitHub.")

    resolved_pull_request_count = (
        merged_pull_request_count + closed_unmerged_pull_request_count
    )

    if resolved_pull_request_count == 0:
        pull_request_acceptance_rate = 0.0
    else:
        pull_request_acceptance_rate = round(
            (merged_pull_request_count / resolved_pull_request_count) * 100,
            2,
        )

    return {
        "owner": repository["owner"]["login"],
        "repository_name": repository["name"],
        "merged_pull_request_count": merged_pull_request_count,
        "closed_unmerged_pull_request_count": closed_unmerged_pull_request_count,
        "resolved_pull_request_count": resolved_pull_request_count,
        "pull_request_acceptance_rate": pull_request_acceptance_rate,
    }