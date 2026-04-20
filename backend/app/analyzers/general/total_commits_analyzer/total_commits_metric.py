from app.analyzers.general.total_commits_analyzer.total_commits_fetch import fetch_total_commits
from app.analyzers.general.total_commits_analyzer.total_commits_constants import (
    TOTAL_COMMITS_METRIC_KEY,
    TOTAL_COMMITS_METRIC_NAME,
    TOTAL_COMMITS_CATEGORY_NAME,
    TOTAL_COMMITS_SUBCATEGORY_NAME,
    BRANCH_NAME,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def get_total_commits_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        TOTAL_COMMITS_CATEGORY_NAME,
        TOTAL_COMMITS_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        result = await fetch_total_commits(
            owner=owner,
            repository_name=repository_name,
        )

        return RepositoryMetricResult(
            metric_key=TOTAL_COMMITS_METRIC_KEY,
            metric_name=TOTAL_COMMITS_METRIC_NAME,
            value=result[TOTAL_COMMITS_METRIC_KEY],
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            metadata={TOTAL_COMMITS_METRIC_KEY: result[TOTAL_COMMITS_METRIC_KEY]},
            message=f'Commit count fetched from branch "{result[BRANCH_NAME]}".',
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=TOTAL_COMMITS_METRIC_KEY,
            metric_name=TOTAL_COMMITS_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            metadata=None,
            message=str(exc),
        )