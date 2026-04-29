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
from app.analyzers.general.total_files_filtered_analyzer.total_files_filtered_constants import (
    TOTAL_FILES_FILTERED_METRIC_KEY,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.analyzers.common.metadata_utils import get_metadata_value


async def _get_total_files_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
    *,
    total_files: int | None = None,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        TOTAL_FILES_CATEGORY_NAME,
        TOTAL_FILES_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()
        default_branch_name: str | None = None

        if total_files is None:
            result = await fetch_total_files(
                owner=owner,
                repository_name=repository_name,
            )
            total_files = len(result[TOTAL_FILES_METRIC_KEY])
            default_branch_name = result[DEFAULT_BRANCH_NAME]

        return RepositoryMetricResult(
            metric_key=TOTAL_FILES_METRIC_KEY,
            metric_name=TOTAL_FILES_METRIC_NAME,
            value=total_files,
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            message=(
                f'File count fetched from default branch '
                f'"{default_branch_name}".'
                if default_branch_name is not None
                else "File count reused from Total Files (filtered) metric."
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


async def get_total_files_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
    prior_results: list[RepositoryMetricResult],
) -> RepositoryMetricResult | None:
    return await _get_total_files_metric(
        request,
        repository,
        total_files=get_metadata_value(
            prior_results,
            [TOTAL_FILES_FILTERED_METRIC_KEY],
            TOTAL_FILES_METRIC_KEY,
            int,
        ),
    )