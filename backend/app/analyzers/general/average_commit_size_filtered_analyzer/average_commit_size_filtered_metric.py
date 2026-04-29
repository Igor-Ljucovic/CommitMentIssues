from typing import Any

from app.analyzers.general.average_commit_size_filtered_analyzer.average_commit_size_filtered_calculate import (
    average_commit_size_filtered_calculate,
)
from app.analyzers.general.average_commit_size_analyzer.average_commit_size_calculate import (
    average_commit_size_calculate,
)
from app.analyzers.general.average_commit_size_analyzer.average_commit_size_constants import (
    AVERAGE_COMMIT_SIZE_METRIC_KEY,
    COMMIT_SIZE_SAMPLES,
)
from app.analyzers.general.average_commit_size_filtered_analyzer.average_commit_size_filtered_constants import (
    AVERAGE_COMMIT_SIZE_FILTERED_METRIC_KEY,
    AVERAGE_COMMIT_SIZE_FILTERED_METRIC_NAME,
    AVERAGE_COMMIT_SIZE_FILTERED_CATEGORY_NAME,
    AVERAGE_COMMIT_SIZE_FILTERED_SUBCATEGORY_NAME,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.analyzers.common.metadata_utils import get_metadata_value


async def _get_average_commit_size_filtered_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
    *,
    commit_size_samples: list[dict[str, Any]] | None = None
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        AVERAGE_COMMIT_SIZE_FILTERED_CATEGORY_NAME,
        AVERAGE_COMMIT_SIZE_FILTERED_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        if commit_size_samples is None:
            # we are calling the average commit size to reduce redundant API calls
            result = await average_commit_size_calculate(
                owner=owner,
                repository_name=repository_name,
            )
            commit_size_samples = result[COMMIT_SIZE_SAMPLES]

        average_commit_size_filtered = await average_commit_size_filtered_calculate(
            commit_size_samples,
            # change the number on the frontend too if you change the one below
            4
        )

        return RepositoryMetricResult(
            metric_key=AVERAGE_COMMIT_SIZE_FILTERED_METRIC_KEY,
            metric_name=AVERAGE_COMMIT_SIZE_FILTERED_METRIC_NAME,
            value=average_commit_size_filtered,
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            metadata={COMMIT_SIZE_SAMPLES: commit_size_samples},
            message=('Median Commit Size calculated successfully'),
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=AVERAGE_COMMIT_SIZE_FILTERED_METRIC_KEY,
            metric_name=AVERAGE_COMMIT_SIZE_FILTERED_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            metadata=None,
            message=str(exc),
        )
    

async def get_average_commit_size_filtered_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
    prior_results: list[RepositoryMetricResult],
) -> RepositoryMetricResult | None:
    return await _get_average_commit_size_filtered_metric(
        request,
        repository,
        commit_size_samples=get_metadata_value(
            prior_results,
            [AVERAGE_COMMIT_SIZE_METRIC_KEY],
            COMMIT_SIZE_SAMPLES,
            list,
        ),
    )