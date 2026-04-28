from app.analyzers.general.total_branches_analyzer.total_branches_fetch import (
    fetch_total_branches,
)
from app.analyzers.general.total_branches_analyzer.total_branches_constants import (
    TOTAL_BRANCHES_METRIC_KEY,
    TOTAL_BRANCHES_METRIC_NAME,
    TOTAL_BRANCHES_CATEGORY_NAME,
    TOTAL_BRANCHES_SUBCATEGORY_NAME,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def get_total_branches_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        TOTAL_BRANCHES_CATEGORY_NAME,
        TOTAL_BRANCHES_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        result = await fetch_total_branches(
            owner=owner,
            repository_name=repository_name,
        )

        return RepositoryMetricResult(
            metric_key=TOTAL_BRANCHES_METRIC_KEY,
            metric_name=TOTAL_BRANCHES_METRIC_NAME,
            value=result[TOTAL_BRANCHES_METRIC_KEY],
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            message="Total branch count fetched successfully.",
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=TOTAL_BRANCHES_METRIC_KEY,
            metric_name=TOTAL_BRANCHES_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            message=str(exc),
        )