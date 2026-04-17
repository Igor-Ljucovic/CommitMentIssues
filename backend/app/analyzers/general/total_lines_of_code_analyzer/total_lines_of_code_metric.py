from app.analyzers.general.total_lines_of_code_analyzer.total_lines_of_code_constants import (
    COUNTED_FILES,
    DEFAULT_BRANCH_NAME,
    SKIPPED_BINARY_FILES,
    TOTAL_LINES_OF_CODE_CATEGORY_NAME,
    TOTAL_LINES_OF_CODE_METRIC_KEY,
    TOTAL_LINES_OF_CODE_METRIC_NAME,
    TOTAL_LINES_OF_CODE_SUBCATEGORY_NAME,
)
from app.analyzers.general.total_lines_of_code_analyzer.total_lines_of_code_fetch import (
    fetch_total_lines_of_code,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def get_total_lines_of_code_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        TOTAL_LINES_OF_CODE_CATEGORY_NAME,
        TOTAL_LINES_OF_CODE_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        result = await fetch_total_lines_of_code(
            owner=owner,
            repository_name=repository_name,
        )

        return RepositoryMetricResult(
            metric_key=TOTAL_LINES_OF_CODE_METRIC_KEY,
            metric_name=TOTAL_LINES_OF_CODE_METRIC_NAME,
            value=result[TOTAL_LINES_OF_CODE_METRIC_KEY],
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            message=(
                f'Line count fetched from default branch "{result[DEFAULT_BRANCH_NAME]}". '
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