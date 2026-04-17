from app.analyzers.general.total_files_analyzer.total_files_constants import (
    DEFAULT_BRANCH_NAME,
    TOTAL_FILES_CATEGORY_NAME,
    TOTAL_FILES_METRIC_KEY,
    TOTAL_FILES_METRIC_NAME,
    TOTAL_FILES_SUBCATEGORY_NAME,
)
from app.analyzers.general.total_files_analyzer.total_files_fetch import (
    fetch_total_files,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def get_total_files_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        TOTAL_FILES_CATEGORY_NAME,
        TOTAL_FILES_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        result = await fetch_total_files(
            owner=owner,
            repository_name=repository_name,
        )

        return RepositoryMetricResult(
            metric_key=TOTAL_FILES_METRIC_KEY,
            metric_name=TOTAL_FILES_METRIC_NAME,
            value=result[TOTAL_FILES_METRIC_KEY],
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            message=(
                f'File count fetched from default branch '
                f'"{result[DEFAULT_BRANCH_NAME]}".'
            ),
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=TOTAL_FILES_METRIC_KEY,
            metric_name=TOTAL_FILES_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            message=str(exc),
        )