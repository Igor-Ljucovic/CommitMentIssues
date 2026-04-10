from app.analyzers.collaboration.pull_request_acceptance_rate_analyzer.pull_request_acceptance_rate_constants import (
    PULL_REQUEST_ACCEPTANCE_RATE_METRIC_KEY,
    PULL_REQUEST_ACCEPTANCE_RATE_DISPLAY_NAME,
    PULL_REQUEST_ACCEPTANCE_RATE_CATEGORY_NAME,
    PULL_REQUEST_ACCEPTANCE_RATE_SUBCATEGORY_NAME,
    CLOSED_UNMERGED_PULL_REQUESTS,
    MERGED_PULL_REQUESTS,
)
from app.analyzers.collaboration.pull_request_acceptance_rate_analyzer.pull_request_acceptance_rate_fetch import (
    fetch_pull_request_acceptance_rate,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def get_pull_request_acceptance_rate_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        PULL_REQUEST_ACCEPTANCE_RATE_CATEGORY_NAME,
        PULL_REQUEST_ACCEPTANCE_RATE_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        result = await fetch_pull_request_acceptance_rate(
            owner=owner,
            repository_name=repository_name,
        )

        return RepositoryMetricResult(
            metric_key=PULL_REQUEST_ACCEPTANCE_RATE_METRIC_KEY,
            display_name=PULL_REQUEST_ACCEPTANCE_RATE_DISPLAY_NAME,
            value=result["pull_request_acceptance_rate"],
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            message=(
                f'Calculated from {result[MERGED_PULL_REQUESTS]} merged and '
                f'{result[CLOSED_UNMERGED_PULL_REQUESTS]} closed-unmerged pull requests.'
            ),
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=PULL_REQUEST_ACCEPTANCE_RATE_METRIC_KEY,
            display_name=PULL_REQUEST_ACCEPTANCE_RATE_DISPLAY_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            message=str(exc),
        )