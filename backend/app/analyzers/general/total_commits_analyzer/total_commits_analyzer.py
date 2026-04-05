from app.analyzers.general.total_commits_analyzer.total_commits_fetch import fetch_total_commits
from app.rating.metric_rating_calculator import calculate_metric_rating
from app.schemas.analysis_request_schemas import AnalysisSubcategoryConfig, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def analyze_total_commits(
    repository: RepositoryInput,
    subcategory_config: AnalysisSubcategoryConfig | None,
) -> RepositoryMetricResult:
    owner, repository_name = repository.get_owner_and_repository_name()

    result = await fetch_total_commits(
        owner=owner,
        repository_name=repository_name,
    )

    total_commits = result["total_commits"]

    rating, requirement_failed = calculate_metric_rating(
        value=total_commits,
        subcategory_config=subcategory_config,
    )

    return RepositoryMetricResult(
        metric_key="total_commits",
        display_name="Total Commits",
        value=total_commits,
        rating=rating,
        requirement_failed=requirement_failed,
        status="success",
        message=f'Commit count fetched from branch "{result["branch_name"]}".',
    )