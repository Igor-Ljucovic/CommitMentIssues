from app.analyzers.general.average_commits_per_month_analyzer.average_commits_per_month_constants import (
    AVERAGE_COMMITS_PER_MONTH_METRIC_KEY,
    AVERAGE_COMMITS_PER_MONTH_METRIC_NAME,
    AVERAGE_COMMITS_PER_MONTH_CATEGORY_NAME,
    AVERAGE_COMMITS_PER_MONTH_SUBCATEGORY_NAME,
)
from app.analyzers.general.average_commits_per_month_analyzer.average_commits_per_month_calculate import (
    calculate_average_commits_per_month,
)
from app.analyzers.general.total_commits_analyzer.total_commits_fetch import (
    fetch_total_commits,
)
from app.analyzers.general.first_commit_date_analyzer.first_commit_date_fetch import (
    fetch_first_commit_date,
)
from app.analyzers.general.last_commit_date_analyzer.last_commit_date_fetch import (
    fetch_last_commit_date,
)
from app.analyzers.general.last_commit_date_analyzer.last_commit_date_constants import (
    LAST_COMMIT_DATE_METRIC_KEY
)
from app.analyzers.general.total_commits_analyzer.total_commits_constants import (
    TOTAL_COMMITS_METRIC_KEY
)
from app.analyzers.general.first_commit_date_analyzer.first_commit_date_constants import (
    FIRST_COMMIT_DATE_METRIC_KEY
)
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput


async def get_average_commits_per_month_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        AVERAGE_COMMITS_PER_MONTH_CATEGORY_NAME,
        AVERAGE_COMMITS_PER_MONTH_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        fetch_total_commits_result = await fetch_total_commits(
            owner=owner,
            repository_name=repository_name,
        )

        fetch_first_commit_date_result = await fetch_first_commit_date(
            owner=owner,
            repository_name=repository_name,
        )

        fetch_last_commit_date_result = await fetch_last_commit_date(
            owner=owner,
            repository_name=repository_name,
        )

        avg_commits = calculate_average_commits_per_month(
            total_commits=fetch_total_commits_result[TOTAL_COMMITS_METRIC_KEY],
            first_commit_date=fetch_first_commit_date_result[FIRST_COMMIT_DATE_METRIC_KEY],
            last_commit_date=fetch_last_commit_date_result[LAST_COMMIT_DATE_METRIC_KEY],
        )

        return RepositoryMetricResult(
            metric_key=AVERAGE_COMMITS_PER_MONTH_METRIC_KEY,
            metric_name=AVERAGE_COMMITS_PER_MONTH_METRIC_NAME,
            value=round(avg_commits, 2),
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            message="Average commits per month calculated successfully.",
        )

    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=AVERAGE_COMMITS_PER_MONTH_METRIC_KEY,
            metric_name=AVERAGE_COMMITS_PER_MONTH_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            message=str(exc),
        )