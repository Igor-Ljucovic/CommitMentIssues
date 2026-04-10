from app.analyzers.general.first_commit_date_analyzer.first_commit_date_fetch import (
    fetch_first_commit_date
)
from app.schemas.analysis_request_schemas import AnalysisSubcategoryConfig, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.analyzers.general.first_commit_date_analyzer.first_commit_date_constants import (
    FIRST_COMMIT_DATE_METRIC_KEY,
    FIRST_COMMIT_DATE_DISPLAY_NAME,
    BRANCH_NAME
)
from app.common.metric_status import MetricStatus


async def analyze_first_commit_date(
    repository: RepositoryInput,
    subcategory_config: AnalysisSubcategoryConfig | None,
) -> RepositoryMetricResult:
    owner, repository_name = repository.get_owner_and_repository_name()

    result = await fetch_first_commit_date(
        owner=owner,
        repository_name=repository_name,
    )

    return RepositoryMetricResult(
        metric_key=FIRST_COMMIT_DATE_METRIC_KEY,
        display_name=FIRST_COMMIT_DATE_DISPLAY_NAME,
        value=result[FIRST_COMMIT_DATE_METRIC_KEY],
        weight=subcategory_config.weight,
        status=MetricStatus.SUCCESS,
        message=f'First commit date fetched from branch "{result[BRANCH_NAME]}".',
    )