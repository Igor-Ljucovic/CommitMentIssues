from app.rating.file_rating_calculator import calculate_file_ratings
from app.rating.repository_rating_calculator import calculate_repository_ratings
from app.schemas.analysis_request_schemas import AnalysisRequest
from app.schemas.analysis_response_schemas import AnalysisResponse
from app.services.github_graphql_service import analyze_repositories_github_graphql


async def analyze_repositories(request: AnalysisRequest) -> AnalysisResponse:
    analysis_response = await analyze_repositories_github_graphql(request)
    analysis_response = calculate_repository_ratings(analysis_response)
    analysis_response = calculate_file_ratings(analysis_response)

    return analysis_response