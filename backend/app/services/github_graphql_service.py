from app.clients.github_graphql_client import execute_github_graphql_query


async def fetch_github_graphql_resource(query: str, variables: dict) -> dict:
    data = await execute_github_graphql_query(query, variables)

    repository = data.get("data", {}).get("repository")
    if repository is None:
        raise ValueError("Repository was not found or is not accessible.")

    return repository