from app.services.github_graphql_service import fetch_github_graphql_resource
from app.analyzers.general.total_branches_analyzer.total_branches_query import (
    TOTAL_BRANCHES_GRAPHQL_QUERY,
)
from app.analyzers.general.total_branches_analyzer.total_branches_constants import (
    TOTAL_BRANCHES_METRIC_KEY,
)


async def fetch_total_branches(
    owner: str,
    repository_name: str,
) -> dict:
    repository = await fetch_github_graphql_resource(
        query=TOTAL_BRANCHES_GRAPHQL_QUERY,
        variables={
            "owner": owner,
            "name": repository_name,
        },
    )

    refs = repository.get("refs")
    if refs is None:
        raise RuntimeError("Could not read repository branches.")

    total_branches = refs.get("totalCount")
    if total_branches is None:
        raise RuntimeError("Could not read total branch count.")

    return {
        "owner": repository["owner"]["login"],
        "repository_name": repository["name"],
        TOTAL_BRANCHES_METRIC_KEY: total_branches,
    }