from app.analyzers.documentation.estimated_readme_quality_analyzer.estimated_readme_quality_metric import (
    get_github_readme_quality_metric,
)
from app.schemas.analysis_request_schemas import AnalysisRequest
from app.schemas.analysis_response_schemas import AnalysisResponse
from app.services.api.analysis_orchestrator_service.utils.client_api_helper_service import (
    run_repository_analysis,
)


async def analyze_repositories_openai_rest(
    request: AnalysisRequest,
) -> AnalysisResponse:
    return await run_repository_analysis(
        request=request,
        metric_executors=[
            get_github_readme_quality_metric,
        ],
        no_repositories_warning=(
            "No repositories were provided in the analysis request, "
            "so AI-based metrics could not be calculated."
        ),
    )