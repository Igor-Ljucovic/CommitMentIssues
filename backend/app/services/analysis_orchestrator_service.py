from app.rating.file_rating_calculator import calculate_file_ratings
from app.rating.ranking.file_ranker import rank_files
from app.rating.ranking.metric_ranker import rank_metrics
from app.rating.ranking.repository_ranker import rank_repositories
from app.rating.repository_rating_calculator import calculate_repository_ratings
from app.rating.metric_rating.metric_rating_calculator import calculate_metric_ratings
from app.schemas.analysis_request_schemas import AnalysisRequest
from app.schemas.analysis_response_schemas import AnalysisResponse
from app.services.github_graphql_service import analyze_repositories_github_graphql
from app.services.openai_rest_service import analyze_repositories_openai_rest
from copy import deepcopy

from app.schemas.analysis_response_schemas import (
    FileAnalysisResult,
    RepositoryAnalysisResult,
)


async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    github_response = await analyze_repositories_github_graphql(request)
    openai_response = await analyze_repositories_openai_rest(request)

    response = merge_analysis_responses(
        github_response=github_response,
        openai_response=openai_response,
    )

    # the request contains the criteria for each of the metrics, 
    # the response doesn't, but gets the ratings for each metric
    response = calculate_metric_ratings(request, response)

    response = calculate_repository_ratings(response)
    response = calculate_file_ratings(response)
    
    response = rank_metrics(response)
    response = rank_repositories(response)
    response = rank_files(response)

    return response


def merge_analysis_responses(
    github_response: AnalysisResponse,
    openai_response: AnalysisResponse,
) -> AnalysisResponse:
    result = deepcopy(github_response)

    file_map: dict[tuple[int | None, str], FileAnalysisResult] = {
        (file_result.file_id, file_result.file_name): file_result
        for file_result in result.files
    }

    for openai_file in openai_response.files:
        file_key = (openai_file.file_id, openai_file.file_name)

        if file_key not in file_map:
            file_map[file_key] = deepcopy(openai_file)
            result.files.append(file_map[file_key])
            continue

        existing_file = file_map[file_key]
        _merge_repositories(existing_file, openai_file)

    result.warnings.extend(openai_response.warnings)

    return result


def _merge_repositories(
    existing_file: FileAnalysisResult,
    incoming_file: FileAnalysisResult,
) -> None:
    repository_map: dict[str, RepositoryAnalysisResult] = {
        repository.repository_url: repository
        for repository in existing_file.repositories
    }

    for incoming_repository in incoming_file.repositories:
        existing_repository = repository_map.get(incoming_repository.repository_url)

        if existing_repository is None:
            existing_file.repositories.append(deepcopy(incoming_repository))
            continue

        existing_repository.metrics.extend(deepcopy(incoming_repository.metrics))