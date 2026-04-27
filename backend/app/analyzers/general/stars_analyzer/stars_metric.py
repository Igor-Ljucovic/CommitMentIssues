from app.analyzers.general.stars_analyzer.stars_fetch import fetch_stars
from app.analyzers.general.stars_analyzer.stars_constants import (
    STARS_METRIC_KEY,
    STARS_METRIC_NAME,
    STARS_CATEGORY_NAME,
    STARS_SUBCATEGORY_NAME,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def get_stars_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        STARS_CATEGORY_NAME,
        STARS_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        result = await fetch_stars(
            owner=owner,
            repository_name=repository_name,
        )

        return RepositoryMetricResult(
            metric_key=STARS_METRIC_KEY,
            metric_name=STARS_METRIC_NAME,
            value=result[STARS_METRIC_KEY],
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            message="Repository star count fetched successfully.",
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=STARS_METRIC_KEY,
            metric_name=STARS_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            message=str(exc),
        )