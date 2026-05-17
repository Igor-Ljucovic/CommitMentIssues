from pathlib import Path

from app.analyzers.general.total_lines_of_code_analyzer.total_lines_of_code_constants import (
    COUNTED_FILES,
    SKIPPED_BINARY_FILES,
    TOTAL_LINES_OF_CODE_CATEGORY_NAME,
    TOTAL_LINES_OF_CODE_METRIC_KEY,
    TOTAL_LINES_OF_CODE_METRIC_NAME,
    TOTAL_LINES_OF_CODE_SUBCATEGORY_NAME,
)
from app.analyzers.general.total_lines_of_code_analyzer.total_lines_of_code_fetch import (
    fetch_total_lines_of_code,
)
from app.analyzers.common.metadata_utils import get_transient_value
from app.analyzers.common.constants import REPOSITORY_TARBALL_METRIC_KEY
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def _get_total_lines_of_code_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
    *,
    tarball_path: Path | None = None,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        TOTAL_LINES_OF_CODE_CATEGORY_NAME,
        TOTAL_LINES_OF_CODE_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    if tarball_path is None:
        return RepositoryMetricResult(
            metric_key=TOTAL_LINES_OF_CODE_METRIC_KEY,
            metric_name=TOTAL_LINES_OF_CODE_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            message="Repository tarball is not available.",
        )

    try:
        result = fetch_total_lines_of_code(tarball_path)

        return RepositoryMetricResult(
            metric_key=TOTAL_LINES_OF_CODE_METRIC_KEY,
            metric_name=TOTAL_LINES_OF_CODE_METRIC_NAME,
            value=result[TOTAL_LINES_OF_CODE_METRIC_KEY],
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            message=(
                f'Counted {result[COUNTED_FILES]} text files and skipped '
                f'{result[SKIPPED_BINARY_FILES]} binary files.'
            ),
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=TOTAL_LINES_OF_CODE_METRIC_KEY,
            metric_name=TOTAL_LINES_OF_CODE_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            message=str(exc),
        )


async def get_total_lines_of_code_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
    prior_results: list[RepositoryMetricResult],
) -> RepositoryMetricResult | None:
    return await _get_total_lines_of_code_metric(
        request,
        repository,
        tarball_path=get_transient_value(
            prior_results,
            [REPOSITORY_TARBALL_METRIC_KEY],
            "tarball_path",
            Path,
        ),
    )

get_total_lines_of_code_metric.metric_key = TOTAL_LINES_OF_CODE_METRIC_KEY
get_total_lines_of_code_metric.get_config = lambda req: req.get_subcategory_config(TOTAL_LINES_OF_CODE_CATEGORY_NAME, TOTAL_LINES_OF_CODE_SUBCATEGORY_NAME)
