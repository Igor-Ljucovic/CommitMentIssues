from app.analyzers.general.total_commits_analyzer.total_commits_analyzer import (
    analyze_total_commits,
)
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.analyzers.general.total_commits_analyzer.total_commits_constants import (
    TOTAL_COMMITS_METRIC_KEY,
    TOTAL_COMMITS_DISPLAY_NAME,
    TOTAL_COMMITS_CATEGORY_NAME,
    TOTAL_COMMITS_SUBCATEGORY_NAME,
)
from app.common.metric_status import MetricStatus


async def execute_total_commits(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    total_commits_config = request.get_subcategory_config(
        TOTAL_COMMITS_CATEGORY_NAME,
        TOTAL_COMMITS_SUBCATEGORY_NAME,
    )

    if total_commits_config is None:
        return None

    try:
        return await analyze_total_commits(
            repository=repository,
            subcategory_config=total_commits_config,
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=TOTAL_COMMITS_METRIC_KEY,
            display_name=TOTAL_COMMITS_DISPLAY_NAME,
            value=None,
            weight=None,
            rating=None,
            requirement_failed=None,
            status=MetricStatus.FAILED,
            message=str(exc),
        )