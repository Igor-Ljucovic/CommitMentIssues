from app.rating.file_rating_calculator import calculate_file_ratings
from app.rating.ranking.file_ranker import rank_files
from app.rating.ranking.metric_ranker import rank_metrics
from app.rating.ranking.repository_ranker import rank_repositories
from app.rating.repository_rating_calculator import calculate_repository_ratings
from app.rating.metric_rating.metric_rating_calculator import calculate_metric_ratings
from app.schemas.analysis_request_schemas import AnalysisRequest
from app.schemas.analysis_response_schemas import AnalysisResponse
from app.services.api.analysis_orchestrator_service.client_api_services.github_graphql_service import (
    analyze_repositories_github_graphql
)
from app.services.api.analysis_orchestrator_service.client_api_services.github_rest_service import (
    analyze_repositories_github_rest
)
from app.services.api.analysis_orchestrator_service.client_api_services.openai_rest_service import (
    analyze_repositories_openai_rest
)
from app.services.internal.analysis_response_merge_service import merge_analysis_responses


async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    github_graphql_response = await analyze_repositories_github_graphql(request)
    github_rest_response = await analyze_repositories_github_rest(request)
    openai_rest_response = await analyze_repositories_openai_rest(request)

    response = merge_analysis_responses(
        [
            github_graphql_response,
            github_rest_response,
            openai_rest_response,
        ]
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