from app.rating.metric_rating_calculator import calculate_metric_rating
from app.schemas.analysis_request_schemas import AnalysisSubcategoryConfig, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.services.github_data_service import get_total_commit_count_for_repository


async def analyze_total_commits(
    repository: RepositoryInput,
    subcategory_config: AnalysisSubcategoryConfig | None,
) -> RepositoryMetricResult:
    result = await get_total_commit_count_for_repository(repository)
    total_commit_count = result["total_commit_count"]

    rating, requirement_failed = calculate_metric_rating(
        value=total_commit_count,
        subcategory_config=subcategory_config,
    )

    return RepositoryMetricResult(
        metric_key="total_commits",
        display_name="Total Commits",
        value=total_commit_count,
        rating=rating,
        requirement_failed=requirement_failed,
        status="success",
        message=f'Commit count fetched from branch "{result["branch_name"]}".',
    )