from app.services.github_graphql_service import fetch_github_graphql_resource
from app.analyzers.collaboration.pull_request_acceptance_rate_analyzer.pull_request_acceptance_rate_query import (
    PULL_REQUEST_ACCEPTANCE_RATE_GRAPHQL_QUERY,
)
from app.analyzers.collaboration.pull_request_acceptance_rate_analyzer.pull_request_acceptance_rate_constants import (
    PULL_REQUEST_ACCEPTANCE_RATE_METRIC_KEY,
    CLOSED_UNMERGED_PULL_REQUESTS,
    MERGED_PULL_REQUESTS,
    RESOLVED_PULL_REQUESTS,
)


async def fetch_pull_request_acceptance_rate(
    owner: str,
    repository_name: str,
) -> dict:
    repository = await fetch_github_graphql_resource(
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

    merged_pull_requests = merged_prs.get("totalCount")
    closed_unmerged_pull_requests = closed_prs.get("totalCount")

    if merged_pull_requests is None or closed_unmerged_pull_requests is None:
        raise RuntimeError("Could not read pull request counts from GitHub.")

    resolved_pull_requests = merged_pull_requests + closed_unmerged_pull_requests

    if resolved_pull_requests == 0:
        acceptance_rate = 0.00
    else:
        acceptance_rate = round((merged_pull_requests / resolved_pull_requests) * 100, 2)

    return {
        "owner": repository["owner"]["login"],
        "repository_name": repository["name"],
        MERGED_PULL_REQUESTS: merged_pull_requests,
        CLOSED_UNMERGED_PULL_REQUESTS: closed_unmerged_pull_requests,
        RESOLVED_PULL_REQUESTS: resolved_pull_requests,
        PULL_REQUEST_ACCEPTANCE_RATE_METRIC_KEY: acceptance_rate,
    }