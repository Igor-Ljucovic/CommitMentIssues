from app.rating.file_rating_calculator import calculate_file_ratings
from app.rating.file_ranker import rank_files
from app.rating.metric_ranker import rank_metrics
from app.rating.repository_ranker import rank_repositories
from app.rating.repository_rating_calculator import calculate_repository_ratings
from app.schemas.analysis_request_schemas import AnalysisRequest
from app.schemas.analysis_response_schemas import AnalysisResponse
from app.services.github_graphql_service import analyze_repositories_github_graphql


async def analyze_repositories(request: AnalysisRequest) -> AnalysisResponse:
    response = await analyze_repositories_github_graphql(request)
    response = calculate_file_ratings(response)
    response = calculate_repository_ratings(response)
    response = rank_files(response)
    response = rank_repositories(response)
    response = rank_metrics(response)
    
    return response