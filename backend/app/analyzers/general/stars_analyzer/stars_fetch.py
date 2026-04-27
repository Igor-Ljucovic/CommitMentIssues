from app.clients.github_graphql_client import execute_github_graphql_query
from app.analyzers.general.stars_analyzer.stars_query import (
    TOTAL_STARS_GRAPHQL_QUERY,
)
from app.analyzers.general.stars_analyzer.stars_constants import (
    STARS_METRIC_KEY,
)


async def fetch_stars(
    owner: str,
    repository_name: str,
) -> dict:
    response = await execute_github_graphql_query(
        query=TOTAL_STARS_GRAPHQL_QUERY,
        variables={
            "owner": owner,
            "name": repository_name,
        },
    )

    repository = response.get("data", {}).get("repository")
    if repository is None:
        raise ValueError("Repository was not found or is not accessible.")

    stars = repository.get("stars")
    if stars is None:
        raise RuntimeError("Could not read repository star count.")

    return {
        "owner": repository["repository_owner"]["login"],
        "repository_name": repository["repository_name"],
        STARS_METRIC_KEY: stars,
    }