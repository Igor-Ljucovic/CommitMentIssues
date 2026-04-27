from app.services.github_graphql_service import fetch_github_graphql_resource
from app.analyzers.general.languages_used_analyzer.languages_used_query import (
    LANGUAGES_USED_GRAPHQL_QUERY,
)
from app.analyzers.general.languages_used_analyzer.languages_used_constants import (
    LANGUAGES_USED_METRIC_KEY,
)


async def fetch_languages_used(
    owner: str,
    repository_name: str,
) -> dict:
    repository = await fetch_github_graphql_resource(
        query=LANGUAGES_USED_GRAPHQL_QUERY,
        variables={
            "owner": owner,
            "name": repository_name,
        },
    )

    languages = repository.get("languages")
    if languages is None:
        raise RuntimeError("Could not read repository languages.")

    language_edges = languages.get("edges") or []

    languages_used = [
        edge["node"]["name"]
        for edge in language_edges
        if edge.get("node") and edge["node"].get("name")
    ]

    return {
        "owner": repository["owner"]["login"],
        "repository_name": repository["name"],
        LANGUAGES_USED_METRIC_KEY: len(languages_used),
        "languages": languages_used,
    }