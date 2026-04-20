from app.analyzers.general.last_commit_date_analyzer.last_commit_date_fetch import (
    fetch_last_commit_date,
)
from app.analyzers.general.last_commit_date_analyzer.last_commit_date_constants import (
    LAST_COMMIT_DATE_METRIC_KEY,
    LAST_COMMIT_DATE_METRIC_NAME,
    LAST_COMMIT_DATE_CATEGORY_NAME,
    LAST_COMMIT_DATE_SUBCATEGORY_NAME,
    BRANCH_NAME,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def get_last_commit_date_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        LAST_COMMIT_DATE_CATEGORY_NAME,
        LAST_COMMIT_DATE_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        result = await fetch_last_commit_date(
            owner=owner,
            repository_name=repository_name,
        )

        return RepositoryMetricResult(
            metric_key=LAST_COMMIT_DATE_METRIC_KEY,
            metric_name=LAST_COMMIT_DATE_METRIC_NAME,
            value=result[LAST_COMMIT_DATE_METRIC_KEY],
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            metadata={LAST_COMMIT_DATE_METRIC_KEY: result[LAST_COMMIT_DATE_METRIC_KEY]},
            message=f'Last commit date fetched from branch "{result[BRANCH_NAME]}".',
        )

    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=LAST_COMMIT_DATE_METRIC_KEY,
            metric_name=LAST_COMMIT_DATE_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            metadata=None,
            message=str(exc),
        )