from app.analyzers.general.total_files_filtered_analyzer.total_files_filtered_constants import (
    DEFAULT_BRANCH_NAME,
    TOTAL_FILES_FILTERED_CATEGORY_NAME,
    TOTAL_FILES_FILTERED_METRIC_KEY,
    TOTAL_FILES_FILTERED_METRIC_NAME,
    TOTAL_FILES_FILTERED_SUBCATEGORY_NAME,
)
from app.analyzers.general.total_files_analyzer.total_files_constants import (
    TOTAL_FILES_METRIC_KEY,
)
from app.analyzers.general.total_files_filtered_analyzer.total_files_filtered_calculate import (
    total_files_filtered_calculate,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def get_total_files_filtered_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        TOTAL_FILES_FILTERED_CATEGORY_NAME,
        TOTAL_FILES_FILTERED_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        result = await total_files_filtered_calculate(
            owner=owner,
            repository_name=repository_name,
        )

        total_files_filtered = result[TOTAL_FILES_FILTERED_METRIC_KEY]
        total_files = result[TOTAL_FILES_METRIC_KEY]
        
        return RepositoryMetricResult(
            metric_key=TOTAL_FILES_FILTERED_METRIC_KEY,
            metric_name=TOTAL_FILES_FILTERED_METRIC_NAME,
            value=total_files_filtered,
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            # TOTAL_FILES_METRIC_KEY is used in another
            # metric to reduce redundant API calls
            metadata={TOTAL_FILES_METRIC_KEY: total_files},
            message=(
                f'Successfully fetched total file count from default branch '
                f'"{result[DEFAULT_BRANCH_NAME]}".'
            ),
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=TOTAL_FILES_FILTERED_METRIC_KEY,
            metric_name=TOTAL_FILES_FILTERED_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            metadata=None,
            message=str(exc),
        )