from app.analyzers.general.average_commit_size_analyzer.average_commit_size_calculate import (
    average_commit_size_calculate,
)
from app.analyzers.general.average_commit_size_analyzer.average_commit_size_constants import (
    AVERAGE_COMMIT_SIZE_METRIC_KEY,
    AVERAGE_COMMIT_SIZE_METRIC_NAME,
    AVERAGE_COMMIT_SIZE_CATEGORY_NAME,
    AVERAGE_COMMIT_SIZE_SUBCATEGORY_NAME,
    BRANCH_NAME,
    SAMPLED_COMMITS_COUNT,
    TOTAL_ADDITIONS,
    TOTAL_DELETIONS,
    COMMIT_SIZE_SAMPLES
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def get_average_commit_size_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        AVERAGE_COMMIT_SIZE_CATEGORY_NAME,
        AVERAGE_COMMIT_SIZE_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        result = await average_commit_size_calculate(
            owner=owner,
            repository_name=repository_name,
        )

        total_additions = result[TOTAL_ADDITIONS]
        total_deletions = result[TOTAL_DELETIONS]
        commit_size_samples = result[COMMIT_SIZE_SAMPLES]

        return RepositoryMetricResult(
            metric_key=AVERAGE_COMMIT_SIZE_METRIC_KEY,
            metric_name=AVERAGE_COMMIT_SIZE_METRIC_NAME,
            value=result[AVERAGE_COMMIT_SIZE_METRIC_KEY],
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            metadata={
                SAMPLED_COMMITS_COUNT: len(commit_size_samples),
                TOTAL_ADDITIONS: total_additions,
                TOTAL_DELETIONS: total_deletions,
                COMMIT_SIZE_SAMPLES: commit_size_samples,
            },
            message=(
                f'Average commit size calculated from '
                f'{len(commit_size_samples)} commits on branch '
                f'"{result[BRANCH_NAME]}".'
            ),
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=AVERAGE_COMMIT_SIZE_METRIC_KEY,
            metric_name=AVERAGE_COMMIT_SIZE_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            metadata=None,
            message=str(exc),
        )