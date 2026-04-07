from app.analyzers.general.first_commit_date_analyzer.first_commit_date_analyzer import (
    analyze_first_commit_date,
)
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.analyzers.general.first_commit_date_analyzer.first_commit_date_constants import (
    FIRST_COMMIT_DATE_METRIC_KEY,
    FIRST_COMMIT_DATE_DISPLAY_NAME,
    FIRST_COMMIT_DATE_CATEGORY_NAME,
    FIRST_COMMIT_DATE_SUBCATEGORY_NAME,
)
from app.common.metric_status import MetricStatus


async def execute_first_commit_date(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    first_commit_date_config = request.get_subcategory_config(
        FIRST_COMMIT_DATE_CATEGORY_NAME,
        FIRST_COMMIT_DATE_SUBCATEGORY_NAME,
    )

    if first_commit_date_config is None:
        return None

    try:
        return await analyze_first_commit_date(
            repository=repository,
            subcategory_config=first_commit_date_config,
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=FIRST_COMMIT_DATE_METRIC_KEY,
            display_name=FIRST_COMMIT_DATE_DISPLAY_NAME,
            value=None,
            weight=None,
            rating=None,
            requirement_failed=None,
            status=MetricStatus.FAILED,
            message=str(exc),
        )