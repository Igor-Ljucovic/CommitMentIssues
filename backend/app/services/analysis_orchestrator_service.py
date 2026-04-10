from app.rating.file_rating_calculator import calculate_file_ratings
from app.rating.ranking.file_ranker import rank_files
from app.rating.ranking.metric_ranker import rank_metrics
from app.rating.ranking.repository_ranker import rank_repositories
from app.rating.repository_rating_calculator import calculate_repository_ratings
from app.rating.metric_rating.metric_rating_calculator import calculate_metric_ratings
from app.schemas.analysis_request_schemas import AnalysisRequest
from app.schemas.analysis_response_schemas import AnalysisResponse
from app.services.github_graphql_service import analyze_repositories_github_graphql


async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    response = await analyze_repositories_github_graphql(request)

    # the request contains the criteria for each of the metrics, 
    # the response doesn't, but gets the ratings for each metric
    response = calculate_metric_ratings(request, response)
    response = calculate_repository_ratings(response)
    response = calculate_file_ratings(response)
    
    response = rank_metrics(response)
    response = rank_repositories(response)
    response = rank_files(response)

    return response