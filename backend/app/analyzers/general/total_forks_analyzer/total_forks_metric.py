from app.analyzers.general.total_forks_analyzer.total_forks_fetch import (
    fetch_total_forks,
)
from app.analyzers.general.total_forks_analyzer.total_forks_constants import (
    TOTAL_FORKS_METRIC_KEY,
    TOTAL_FORKS_METRIC_NAME,
    TOTAL_FORKS_CATEGORY_NAME,
    TOTAL_FORKS_SUBCATEGORY_NAME,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def get_total_forks_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        TOTAL_FORKS_CATEGORY_NAME,
        TOTAL_FORKS_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        result = await fetch_total_forks(
            owner=owner,
            repository_name=repository_name,
        )

        return RepositoryMetricResult(
            metric_key=TOTAL_FORKS_METRIC_KEY,
            metric_name=TOTAL_FORKS_METRIC_NAME,
            value=result[TOTAL_FORKS_METRIC_KEY],
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            message="Fork count fetched successfully.",
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=TOTAL_FORKS_METRIC_KEY,
            metric_name=TOTAL_FORKS_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            message=str(exc),
        )