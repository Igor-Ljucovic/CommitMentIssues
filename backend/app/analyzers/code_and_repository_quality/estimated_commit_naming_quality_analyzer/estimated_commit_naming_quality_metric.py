from app.analyzers.code_and_repository_quality.estimated_commit_naming_quality_analyzer.estimated_commit_naming_quality_calculator import (
    calculate_estimated_commit_naming_quality_breakdown,
)
from app.analyzers.code_and_repository_quality.estimated_commit_naming_quality_analyzer.estimated_commit_naming_quality_constants import (
    BRANCH_NAME,
    COMMIT_MESSAGES,
    ESTIMATED_COMMIT_NAMING_QUALITY_CATEGORY_NAME,
    ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_KEY,
    ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_NAME,
    ESTIMATED_COMMIT_NAMING_QUALITY_SUBCATEGORY_NAME,
)
from app.analyzers.code_and_repository_quality.estimated_commit_naming_quality_analyzer.estimated_commit_naming_quality_fetch import (
    fetch_estimated_commit_naming_quality_data,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def get_estimated_commit_naming_quality_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        ESTIMATED_COMMIT_NAMING_QUALITY_CATEGORY_NAME,
        ESTIMATED_COMMIT_NAMING_QUALITY_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:   
        owner, repository_name = repository.get_owner_and_repository_name()

        result = await fetch_estimated_commit_naming_quality_data(
            owner=owner,
            repository_name=repository_name,
        )

        breakdown = calculate_estimated_commit_naming_quality_breakdown(
            commit_messages=result[COMMIT_MESSAGES],
        )

        return RepositoryMetricResult(
            metric_key=ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_KEY,
            metric_name=ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_NAME,
            value=round(breakdown.total_score * 0.1, 2),
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            # metadata is used for debugging only
            # metadata={
            #     "consistency_score": breakdown.consistency_score,
            #     "length_score": breakdown.length_score,
            #     "conventional_words_score": breakdown.conventional_words_score,
            #     "bad_practice_score": breakdown.bad_practice_score,
            #     "commit_names": breakdown.sampled_commits,
            # },
            message=(
                f'Commit naming quality calculated from '
                f'{len(breakdown.sampled_commits)} sampled commit names '
                f'on branch "{result[BRANCH_NAME]}".'
            ),
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_KEY,
            metric_name=ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            metadata=None,
            message=str(exc),
        )