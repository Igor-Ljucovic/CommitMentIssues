from app.services.github_graphql_service import analyze_repositories_github_graphql
from app.schemas.analysis_request_schemas import AnalysisRequest
from app.schemas.analysis_response_schemas import AnalysisResponse


async def analyze_repositories(request: AnalysisRequest) -> AnalysisResponse:
    return await analyze_repositories_github_graphql(request)