from app.clients.github_graphql_client import fetch_total_commit_count
from app.schemas.analysis_request_schemas import RepositoryInput


async def get_total_commit_count_for_repository(
    repository: RepositoryInput,
) -> dict:
    owner, repository_name = repository.get_owner_and_repository_name()

    return await fetch_total_commit_count(
        owner=owner,
        repository_name=repository_name,
    )