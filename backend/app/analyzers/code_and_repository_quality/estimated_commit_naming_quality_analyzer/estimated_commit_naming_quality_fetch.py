from app.analyzers.code_and_repository_quality.estimated_commit_naming_quality_analyzer.estimated_commit_naming_quality_constants import (
    BRANCH_NAME,
    COMMIT_MESSAGES,
)
from app.analyzers.code_and_repository_quality.estimated_commit_naming_quality_analyzer.estimated_commit_naming_quality_query import (
    ESTIMATED_COMMIT_NAMING_QUALITY_GRAPHQL_QUERY,
)
from app.services.github_graphql_service import fetch_github_graphql_resource


async def fetch_estimated_commit_naming_quality_data(
    owner: str,
    repository_name: str,
) -> dict:
    commit_messages: list[str] = []
    cursor: str | None = None
    branch_name: str | None = None
    repository_owner: str | None = None
    repository_actual_name: str | None = None

    while True:
        repository = await fetch_github_graphql_resource(
            query=ESTIMATED_COMMIT_NAMING_QUALITY_GRAPHQL_QUERY,
            variables={
                "owner": owner,
                "name": repository_name,
                "cursor": cursor,
            },
        )

        if repository_owner is None:
            repository_owner = repository["owner"]["login"]
        if repository_actual_name is None:
            repository_actual_name = repository["name"]

        default_branch_ref = repository.get("defaultBranchRef")
        if default_branch_ref is None:
            raise ValueError("Repository does not have a default branch.")

        if branch_name is None:
            branch_name = default_branch_ref["name"]

        history = default_branch_ref.get("target", {}).get("history")
        if history is None:
            raise RuntimeError(
                "Could not read commit history for the default branch."
            )

        nodes = history.get("nodes")
        if nodes is None:
            raise RuntimeError(
                "Could not read commit history for the default branch."
            )

        for node in nodes:
            message_headline = node.get("messageHeadline")
            if isinstance(message_headline, str) and message_headline.strip():
                commit_messages.append(message_headline.strip())

        page_info = history.get("pageInfo")
        if page_info is None:
            raise RuntimeError("Could not read commit history pagination info.")

        has_next_page = page_info.get("hasNextPage")
        end_cursor = page_info.get("endCursor")

        if not has_next_page:
            break

        cursor = end_cursor

    if not commit_messages:
        raise RuntimeError("Repository does not contain any commit messages.")

    return {
        "owner": repository_owner,
        "repository_name": repository_actual_name,
        BRANCH_NAME: branch_name,
        COMMIT_MESSAGES: commit_messages,
    }