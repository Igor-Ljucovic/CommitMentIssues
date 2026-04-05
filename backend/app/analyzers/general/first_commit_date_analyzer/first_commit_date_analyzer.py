from app.analyzers.general.first_commit_date_analyzer.first_commit_date_fetch import fetch_first_commit_date
from app.rating.metric_rating_calculator import calculate_metric_rating
from app.schemas.analysis_request_schemas import AnalysisSubcategoryConfig, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def analyze_first_commit_date(
    repository: RepositoryInput,
    subcategory_config: AnalysisSubcategoryConfig | None,
) -> RepositoryMetricResult:
    owner, repository_name = repository.get_owner_and_repository_name()

    result = await fetch_first_commit_date(
        owner=owner,
        repository_name=repository_name,
    )
    
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