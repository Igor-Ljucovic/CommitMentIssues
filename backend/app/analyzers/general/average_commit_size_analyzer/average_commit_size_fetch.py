from app.services.github_graphql_service import fetch_github_graphql_resource
from app.analyzers.general.average_commit_size_analyzer.average_commit_size_query import (
    AVERAGE_COMMIT_SIZE_GRAPHQL_QUERY,
)
from app.analyzers.general.average_commit_size_analyzer.average_commit_size_constants import (
    AVERAGE_COMMIT_SIZE_SAMPLE_SIZE,
    BRANCH_NAME,
    GITHUB_GRAPHQL_PAGE_SIZE_LIMIT,
    SAMPLED_COMMIT_NODES
)


async def fetch_average_commit_size(
    owner: str,
    repository_name: str,
) -> dict:
    sampled_commit_nodes: list[dict] = []
    after_cursor: str | None = None
    repository_info: dict | None = None
    default_branch_name: str | None = None

    while len(sampled_commit_nodes) < AVERAGE_COMMIT_SIZE_SAMPLE_SIZE:
        remaining = AVERAGE_COMMIT_SIZE_SAMPLE_SIZE - len(sampled_commit_nodes)
        page_size = min(GITHUB_GRAPHQL_PAGE_SIZE_LIMIT, remaining)

        repository = await fetch_github_graphql_resource(
            query=AVERAGE_COMMIT_SIZE_GRAPHQL_QUERY,
            variables={
                "owner": owner,
                "name": repository_name,
                "first": page_size,
                "after": after_cursor,
            },
        )

        repository_info = repository

        default_branch_ref = repository.get("defaultBranchRef")
        if default_branch_ref is None:
            raise ValueError("Repository does not have a default branch.")

        default_branch_name = default_branch_ref["name"]

        history = default_branch_ref.get("target", {}).get("history")
        if history is None:
            raise RuntimeError("Could not read commit history for the default branch.")

        page_nodes = history.get("nodes") or []
        sampled_commit_nodes.extend(page_nodes)

        page_info = history.get("pageInfo") or {}
        if not page_info.get("hasNextPage"):
            break

        after_cursor = page_info.get("endCursor")
        if after_cursor is None:
            break

    if repository_info is None:
        raise RuntimeError("Could not read repository data.")

    return {
        "owner": repository_info["owner"]["login"],
        "repository_name": repository_info["name"],
        BRANCH_NAME: default_branch_name,
        SAMPLED_COMMIT_NODES: sampled_commit_nodes
    }