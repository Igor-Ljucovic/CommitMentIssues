from app.analyzers.documentation.github_wiki_total_commits_analyzer.github_wiki_total_commits_analyzer import (
    analyze_github_wiki_total_commits,
)
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.analyzers.documentation.github_wiki_total_commits_analyzer.github_wiki_total_commits_constants import (
    GITHUB_WIKI_TOTAL_COMMITS_METRIC_KEY,
    GITHUB_WIKI_TOTAL_COMMITS_DISPLAY_NAME,
    GITHUB_WIKI_TOTAL_COMMITS_CATEGORY_NAME,
    GITHUB_WIKI_TOTAL_COMMITS_SUBCATEGORY_NAME,
)

async def execute_github_wiki_total_commits(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    github_wiki_total_commits_config = request.get_subcategory_config(
        GITHUB_WIKI_TOTAL_COMMITS_CATEGORY_NAME,
        GITHUB_WIKI_TOTAL_COMMITS_SUBCATEGORY_NAME,
    )

    if github_wiki_total_commits_config is None:
        return None

    try:
        return await analyze_github_wiki_total_commits(
            repository=repository,
            subcategory_config=github_wiki_total_commits_config,
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=GITHUB_WIKI_TOTAL_COMMITS_METRIC_KEY,
            display_name=GITHUB_WIKI_TOTAL_COMMITS_DISPLAY_NAME,
            value=None,
            rating=None,
            requirement_failed=None,
            status="failed",
            message=str(exc),
        )