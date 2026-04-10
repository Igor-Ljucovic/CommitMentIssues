from app.analyzers.general.total_commits_analyzer.total_commits_fetch import fetch_total_commits
from app.schemas.analysis_request_schemas import AnalysisSubcategoryConfig, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.analyzers.general.total_commits_analyzer.total_commits_constants import (
    TOTAL_COMMITS_METRIC_KEY,
    TOTAL_COMMITS_DISPLAY_NAME,
    BRANCH_NAME
)
from app.common.metric_status import MetricStatus


async def analyze_total_commits(
    repository: RepositoryInput,
    subcategory_config: AnalysisSubcategoryConfig | None,
) -> RepositoryMetricResult:
    owner, repository_name = repository.get_owner_and_repository_name()

    result = await fetch_total_commits(
        owner=owner,
        repository_name=repository_name,
    )

    return RepositoryMetricResult(
        metric_key=TOTAL_COMMITS_METRIC_KEY,
        display_name=TOTAL_COMMITS_DISPLAY_NAME,
        value=result[TOTAL_COMMITS_METRIC_KEY],
        weight=subcategory_config.weight,
        status=MetricStatus.SUCCESS,
        message=f'Commit count fetched from branch "{result[BRANCH_NAME]}".',
    )