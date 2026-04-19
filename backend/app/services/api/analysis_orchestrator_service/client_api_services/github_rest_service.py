from app.analyzers.general.total_files_analyzer.total_files_metric import (
    get_total_files_metric,
)
from app.analyzers.general.total_lines_of_code_analyzer.total_lines_of_code_metric import (
    get_total_lines_of_code_metric,
)
from app.analyzers.general.total_files_filtered_analyzer.total_files_filtered_metric import (
    get_total_files_filtered_metric
)
from app.schemas.analysis_request_schemas import AnalysisRequest
from app.schemas.analysis_response_schemas import AnalysisResponse
from app.services.api.analysis_orchestrator_service.utils.client_api_helper_service import (
    run_repository_analysis
)


async def analyze_repositories_github_rest(
    request: AnalysisRequest,
) -> AnalysisResponse:
    return await run_repository_analysis(
        request=request,
        metric_executors=[
            get_total_files_metric,
            get_total_files_filtered_metric,
            # avoid using the "total_lines_of_code" metric since it downloads the
            # repo as a tar, counts all \n-s, can be bottlenecked by 1 large repo
            get_total_lines_of_code_metric,
        ],
        no_repositories_warning=(
            "No repositories were provided in the analysis request, "
            "so GitHub REST-based metrics could not be calculated."
        ),
    )