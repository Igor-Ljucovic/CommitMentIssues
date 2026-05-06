from pathlib import Path

from app.analyzers.general.total_lines_of_code_filtered_analyzer.total_lines_of_code_filtered_constants import (
    COUNTED_FILES,
    DEFAULT_BRANCH_NAME,
    SKIPPED_FILES,
    TOTAL_LINES_OF_CODE_FILTERED_CATEGORY_NAME,
    TOTAL_LINES_OF_CODE_FILTERED_METRIC_KEY,
    TOTAL_LINES_OF_CODE_FILTERED_METRIC_NAME,
    TOTAL_LINES_OF_CODE_FILTERED_SUBCATEGORY_NAME,
)
from app.analyzers.general.total_lines_of_code_filtered_analyzer.total_lines_of_code_filtered_fetch import (
    fetch_total_lines_of_code_filtered,
)
from app.analyzers.general.total_lines_of_code_analyzer.total_lines_of_code_constants import (
    TOTAL_LINES_OF_CODE_METRIC_KEY,
)
from app.analyzers.common.metadata_utils import get_transient_value
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def _get_total_lines_of_code_filtered_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
    *,
    tarball_path: Path | None = None,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        TOTAL_LINES_OF_CODE_FILTERED_CATEGORY_NAME,
        TOTAL_LINES_OF_CODE_FILTERED_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        result = await fetch_total_lines_of_code_filtered(
            owner=owner,
            repository_name=repository_name,
            tarball_path=tarball_path,
        )

        default_branch = result[DEFAULT_BRANCH_NAME]
        branch_info = (
            f'from default branch "{default_branch}". '
            if default_branch
            else "from cached tarball. "
        )

        metric_result = RepositoryMetricResult(
            metric_key=TOTAL_LINES_OF_CODE_FILTERED_METRIC_KEY,
            metric_name=TOTAL_LINES_OF_CODE_FILTERED_METRIC_NAME,
            value=result[TOTAL_LINES_OF_CODE_FILTERED_METRIC_KEY],
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            message=(
                f"Line count fetched {branch_info}"
                f"Counted {result[COUNTED_FILES]} code files and skipped "
                f"{result[SKIPPED_FILES]} non-code files."
            ),
        )
        metric_result._transient["tarball_path"] = result["tarball_path"]
        return metric_result

    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=TOTAL_LINES_OF_CODE_FILTERED_METRIC_KEY,
            metric_name=TOTAL_LINES_OF_CODE_FILTERED_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            message=str(exc),
        )


async def get_total_lines_of_code_filtered_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
    prior_results: list[RepositoryMetricResult],
) -> RepositoryMetricResult | None:
    return await _get_total_lines_of_code_filtered_metric(
        request,
        repository,
        tarball_path=get_transient_value(
            prior_results,
            [TOTAL_LINES_OF_CODE_METRIC_KEY],
            "tarball_path",
            Path,
        ),
    )
