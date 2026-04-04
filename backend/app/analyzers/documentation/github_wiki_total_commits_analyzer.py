from app.analyzers.rating.metric_rating_calculator import calculate_metric_rating
from app.schemas.analysis_request_schemas import AnalysisSubcategoryConfig, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.services.github_data_service import get_github_wiki_commit_count_for_repository


async def analyze_github_wiki_commit_count(
    repository: RepositoryInput,
    subcategory_config: AnalysisSubcategoryConfig | None,
) -> RepositoryMetricResult:
    result = await get_github_wiki_commit_count_for_repository(repository)
    wiki_commit_count = result["wiki_commit_count"]

    rating, requirement_failed = calculate_metric_rating(
        value=wiki_commit_count,
        subcategory_config=subcategory_config,
    )

    return RepositoryMetricResult(
        metric_key="github_wiki_commit_count",
        display_name="GitHub Wiki Commits",
        value=wiki_commit_count,
        rating=rating,
        requirement_failed=requirement_failed,
        status="success",
        message="GitHub wiki commit count fetched successfully.",
    )