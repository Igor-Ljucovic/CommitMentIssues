from app.analyzers.collaboration.pull_request_acceptance_rate_analyzer.pull_request_acceptance_rate_analyzer import (
    analyze_pull_request_acceptance_rate,
)
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.analyzers.collaboration.pull_request_acceptance_rate_analyzer.pull_request_acceptance_rate_constants import (
    PULL_REQUEST_ACCEPTANCE_RATE_METRIC_KEY,
    PULL_REQUEST_ACCEPTANCE_RATE_DISPLAY_NAME,
    PULL_REQUEST_ACCEPTANCE_RATE_CATEGORY_NAME,
    PULL_REQUEST_ACCEPTANCE_RATE_SUBCATEGORY_NAME,
)

async def execute_pull_request_acceptance_rate(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    pull_request_acceptance_rate_config = request.get_subcategory_config(
        PULL_REQUEST_ACCEPTANCE_RATE_CATEGORY_NAME,
        PULL_REQUEST_ACCEPTANCE_RATE_SUBCATEGORY_NAME,
    )

    if pull_request_acceptance_rate_config is None:
        return None

    try:
        return await analyze_pull_request_acceptance_rate(
            repository=repository,
            subcategory_config=pull_request_acceptance_rate_config,
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=PULL_REQUEST_ACCEPTANCE_RATE_METRIC_KEY,
            display_name=PULL_REQUEST_ACCEPTANCE_RATE_DISPLAY_NAME,
            value=None,
            weight=None,
            rating=None,
            requirement_failed=None,
            status="failed",
            message=str(exc),
        )