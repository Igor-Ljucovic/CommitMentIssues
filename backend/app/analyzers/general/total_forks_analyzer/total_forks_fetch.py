from app.clients.github.github_graphql_client import execute_github_graphql_query
from app.analyzers.general.total_forks_analyzer.total_forks_query import (
    TOTAL_FORKS_GRAPHQL_QUERY,
)
from app.analyzers.general.total_forks_analyzer.total_forks_constants import (
    TOTAL_FORKS_METRIC_KEY,
)


async def fetch_total_forks(
    owner: str,
    repository_name: str,
) -> dict:
    repository = await execute_github_graphql_query(
        query=TOTAL_FORKS_GRAPHQL_QUERY,
        variables={
            "owner": owner,
            "name": repository_name,
        },
    )

    fork_count = repository.get("forkCount")
    if fork_count is None:
        raise RuntimeError("Could not read fork count for the repository.")

    return {
        "owner": repository["owner"]["login"],
        "repository_name": repository["name"],
        TOTAL_FORKS_METRIC_KEY: fork_count,
    }