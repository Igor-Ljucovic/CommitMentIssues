from app.analyzers.documentation.github_wiki_total_commits_analyzer.github_wiki_total_commits_constants import (
    GITHUB_WIKI_TOTAL_COMMITS_METRIC_KEY,
    GITHUB_WIKI_TOTAL_COMMITS_DISPLAY_NAME,
    GITHUB_WIKI_TOTAL_COMMITS_CATEGORY_NAME,
    GITHUB_WIKI_TOTAL_COMMITS_SUBCATEGORY_NAME,
)
from app.analyzers.documentation.github_wiki_total_commits_analyzer.github_wiki_total_commits_fetch import (
    fetch_github_wiki_total_commits,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def get_github_wiki_total_commits_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        GITHUB_WIKI_TOTAL_COMMITS_CATEGORY_NAME,
        GITHUB_WIKI_TOTAL_COMMITS_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        result = await fetch_github_wiki_total_commits(
            owner=owner,
            repository_name=repository_name,
        )

        return RepositoryMetricResult(
            metric_key=GITHUB_WIKI_TOTAL_COMMITS_METRIC_KEY,
            display_name=GITHUB_WIKI_TOTAL_COMMITS_DISPLAY_NAME,
            value=result[GITHUB_WIKI_TOTAL_COMMITS_METRIC_KEY],
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            message="GitHub wiki total commits fetched successfully.",
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=GITHUB_WIKI_TOTAL_COMMITS_METRIC_KEY,
            display_name=GITHUB_WIKI_TOTAL_COMMITS_DISPLAY_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            message=str(exc),
        )