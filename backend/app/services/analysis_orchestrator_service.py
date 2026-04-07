from app.rating.repository_rating_calculator import calculate_repository_ratings
from app.schemas.analysis_request_schemas import AnalysisRequest
from app.schemas.analysis_response_schemas import AnalysisResponse
from app.services.github_graphql_service import analyze_repositories_github_graphql


async def analyze_repositories(request: AnalysisRequest) -> AnalysisResponse:
    github_analysis_response = await analyze_repositories_github_graphql(request)

    analysis_response_with_repository_ratings = calculate_repository_ratings(
        analysis_response=github_analysis_response,
    )

    return analysis_response_with_repository_ratings