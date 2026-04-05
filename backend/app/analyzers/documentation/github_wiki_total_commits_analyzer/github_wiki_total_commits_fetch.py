from app.clients.github_graphql_client import _execute_github_graphql_query
from app.analyzers.documentation.github_wiki_total_commits_analyzer.github_wiki_total_commits_query import GITHUB_WIKI_ENABLED_QUERY


async def fetch_github_wiki_enabled(
    owner: str,
    repository_name: str,
) -> dict:
    repository = await _execute_github_graphql_query(
        query=GITHUB_WIKI_ENABLED_QUERY,
        variables={
            "owner": owner,
            "name": repository_name,
        },
    )

    has_wiki_enabled = repository.get("hasWikiEnabled")

    if has_wiki_enabled is None:
        raise RuntimeError("Could not read GitHub wiki enabled status.")

    return {
        "has_wiki_enabled": has_wiki_enabled,
    }