from typing import Any

from app.analyzers.general.median_commit_size_analyzer.median_commit_size_calculate import (
    median_commit_size_calculate,
)
from app.analyzers.general.average_commit_size_analyzer.average_commit_size_calculate import (
    average_commit_size_calculate,
)
from app.analyzers.general.average_commit_size_analyzer.average_commit_size_constants import (
    AVERAGE_COMMIT_SIZE_METRIC_KEY,
    COMMIT_SIZE_SAMPLES,
)
from app.analyzers.general.median_commit_size_analyzer.median_commit_size_constants import (
    MEDIAN_COMMIT_SIZE_METRIC_KEY,
    MEDIAN_COMMIT_SIZE_METRIC_NAME,
    MEDIAN_COMMIT_SIZE_CATEGORY_NAME,
    MEDIAN_COMMIT_SIZE_SUBCATEGORY_NAME,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.analyzers.common.metadata_utils import get_metadata_value


async def _get_median_commit_size_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
    *,
    commit_size_samples: list[dict[str, Any]] | None = None
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        MEDIAN_COMMIT_SIZE_CATEGORY_NAME,
        MEDIAN_COMMIT_SIZE_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        if commit_size_samples is None:
            result = await average_commit_size_calculate(
                owner=owner,
                repository_name=repository_name,
            )
            commit_size_samples = result[COMMIT_SIZE_SAMPLES]

        median_commit_size = await median_commit_size_calculate(commit_size_samples)

        return RepositoryMetricResult(
            metric_key=MEDIAN_COMMIT_SIZE_METRIC_KEY,
            metric_name=MEDIAN_COMMIT_SIZE_METRIC_NAME,
            value=median_commit_size,
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            message=('Median Commit Size calculated successfully'),
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=MEDIAN_COMMIT_SIZE_METRIC_KEY,
            metric_name=MEDIAN_COMMIT_SIZE_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            metadata=None,
            message=str(exc),
        )
    

async def get_median_commit_size_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
    prior_results: list[RepositoryMetricResult],
) -> RepositoryMetricResult | None:
    return await _get_median_commit_size_metric(
        request,
        repository,
        commit_size_samples=get_metadata_value(
            prior_results,
            lambda metric: metric.metric_key == AVERAGE_COMMIT_SIZE_METRIC_KEY,
            COMMIT_SIZE_SAMPLES,
            list,
        ),
    )