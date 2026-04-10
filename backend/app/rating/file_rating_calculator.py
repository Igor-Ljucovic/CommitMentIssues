from copy import deepcopy

from app.schemas.analysis_response_schemas import AnalysisResponse


def calculate_file_ratings(
    analysis_response: AnalysisResponse,
) -> AnalysisResponse:
    result = deepcopy(analysis_response)

    for file_result in result.files:
        rating_sum = 0.0
        rated_repository_count = 0

        requirement_failed_repositories: list[str] = []
        status_failed_repositories: list[str] = []

        for repository in file_result.repositories:
            repository_rating = (
                float(repository.rating)
                if repository.rating is not None
                else None
            )

            if repository_rating is not None:
                rating_sum += repository_rating
                rated_repository_count += 1

            if repository.requirement_failed_metrics:
                requirement_failed_repositories.append(repository.repository_url)

            if repository.status_failed_metrics:
                status_failed_repositories.append(repository.repository_url)

        file_result.rating = (
            round(rating_sum / rated_repository_count, 2)
            if rated_repository_count > 0
            else 0.0
        )

        if requirement_failed_repositories:
            file_result.requirement_failed_repositories = requirement_failed_repositories

        if status_failed_repositories:
            file_result.status_failed_repositories = status_failed_repositories

    return result