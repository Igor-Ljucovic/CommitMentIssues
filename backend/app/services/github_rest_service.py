from app.schemas.analysis_request_schemas import AnalysisRequest
from app.schemas.analysis_response_schemas import AnalysisResponse
from app.services.client_api_helper_service import run_repository_analysis


async def analyze_repositories_github_rest(
    request: AnalysisRequest,
) -> AnalysisResponse:
    return await run_repository_analysis(
        request=request,
        metric_executors=[],
        no_repositories_warning=(
            "No repositories were provided in the analysis request, "
            "so GitHub REST-based metrics could not be calculated."
        ),
    )