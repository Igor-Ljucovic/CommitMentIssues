from app.analyzers.collaboration.pull_request_acceptance_rate_analyzer.pull_request_acceptance_rate_fetch import fetch_pull_request_acceptance_rate
from app.rating.metric_rating_calculator import calculate_metric_rating
from app.schemas.analysis_request_schemas import AnalysisSubcategoryConfig, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def analyze_pull_request_acceptance_rate (
    repository: RepositoryInput,
    subcategory_config: AnalysisSubcategoryConfig | None,
) -> RepositoryMetricResult:
    owner, repository_name = repository.get_owner_and_repository_name()

    result = await fetch_pull_request_acceptance_rate (
        owner=owner,
        repository_name=repository_name,
    )
    
    pull_request_acceptance_rate  = result["pull_request_acceptance_rate"]

    rating, requirement_failed = calculate_metric_rating(
        value=pull_request_acceptance_rate ,
        subcategory_config=subcategory_config,
    )

    return RepositoryMetricResult(
        metric_key="pull_request_acceptance_rate",
        display_name="Pull Request Acceptance Rate",
        value=pull_request_acceptance_rate,
        rating=rating,
        requirement_failed=requirement_failed,
        status="success",
        message=(
            f'Calculated from {result["merged_pull_request_count"]} merged and '
            f'{result["closed_unmerged_pull_request_count"]} closed-unmerged pull requests.'
        ),
    )