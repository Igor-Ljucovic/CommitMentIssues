from app.analyzers.documentation.github_wiki_total_commits_analyzer.github_wiki_total_commits_constants import (
    GITHUB_WIKI_TOTAL_COMMITS_DISPLAY_NAME,
    GITHUB_WIKI_TOTAL_COMMITS_METRIC_KEY,
)
from app.analyzers.documentation.github_wiki_total_commits_analyzer.github_wiki_total_commits_fetch import (
    fetch_github_wiki_total_commits,
)
from app.schemas.analysis_request_schemas import AnalysisSubcategoryConfig, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.common.metric_status import MetricStatus


async def analyze_github_wiki_total_commits(
    repository: RepositoryInput,
    subcategory_config: AnalysisSubcategoryConfig | None,
) -> RepositoryMetricResult:
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