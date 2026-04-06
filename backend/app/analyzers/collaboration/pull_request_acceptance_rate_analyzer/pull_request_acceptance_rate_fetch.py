from app.clients.github_graphql_client import execute_github_graphql_query
from app.analyzers.collaboration.pull_request_acceptance_rate_analyzer.pull_request_acceptance_rate_query import (
    PULL_REQUEST_ACCEPTANCE_RATE_GRAPHQL_QUERY,
)


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

    merged_prs = repository.get("mergedPullRequests")
    closed_prs = repository.get("closedPullRequests")

    if merged_prs is None or closed_prs is None:
        raise RuntimeError("Could not read pull request data from GitHub.")

    merged_count = merged_prs.get("totalCount")
    closed_unmerged_count = closed_prs.get("totalCount")

    if merged_count is None or closed_unmerged_count is None:
        raise RuntimeError("Could not read pull request counts from GitHub.")

    resolved_count = merged_count + closed_unmerged_count

    if resolved_count == 0:
        acceptance_rate = 0.00
    else:
        acceptance_rate = round((merged_count / resolved_count) * 100, 2)

    return {
        "owner": repository["owner"]["login"],
        "repository_name": repository["name"],
        "merged_pull_request_count": merged_count,
        "closed_unmerged_pull_request_count": closed_unmerged_count,
        "resolved_pull_request_count": resolved_count,
        "pull_request_acceptance_rate": acceptance_rate,
    }