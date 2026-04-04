from app.rating.metric_rating_calculator import calculate_metric_rating
from app.schemas.analysis_request_schemas import AnalysisSubcategoryConfig, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.services.github_data_service import get_first_commit_date_for_repository


async def analyze_first_commit_date(
    repository: RepositoryInput,
    subcategory_config: AnalysisSubcategoryConfig | None,
) -> RepositoryMetricResult:
    result = await get_first_commit_date_for_repository(repository)
    first_commit_date = result["first_commit_date"]

    rating, requirement_failed = calculate_metric_rating(
        value=first_commit_date,
        subcategory_config=subcategory_config,
    )

    return RepositoryMetricResult(
        metric_key="first_commit_date",
        display_name="First Commit Date",
        value=first_commit_date,
        rating=rating,
        requirement_failed=requirement_failed,
        status="success",
        message=f'First commit date fetched from branch "{result["branch_name"]}".',
    )