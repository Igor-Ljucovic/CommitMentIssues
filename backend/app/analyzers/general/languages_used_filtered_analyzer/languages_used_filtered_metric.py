from app.analyzers.general.languages_used_filtered_analyzer.languages_used_filtered_calculate import (
    languages_used_filtered_calculate,
)
from app.analyzers.general.languages_used_filtered_analyzer.languages_used_filtered_constants import (
    LANGUAGES_USED_FILTERED_METRIC_KEY,
    LANGUAGES_USED_FILTERED_METRIC_NAME,
    LANGUAGES_USED_FILTERED_CATEGORY_NAME,
    LANGUAGES_USED_FILTERED_SUBCATEGORY_NAME,
)
from app.analyzers.general.languages_used_analyzer.languages_used_constants import (
    LANGUAGES_USED_METRIC_KEY,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def get_languages_used_filtered_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        LANGUAGES_USED_FILTERED_CATEGORY_NAME,
        LANGUAGES_USED_FILTERED_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()
        
        result = await languages_used_filtered_calculate(
            owner=owner,
            repository_name=repository_name,
        )

        languages_used_filtered = result[LANGUAGES_USED_FILTERED_METRIC_KEY]
        languages_used = result[LANGUAGES_USED_METRIC_KEY]

        return RepositoryMetricResult(
            metric_key=LANGUAGES_USED_FILTERED_METRIC_KEY,
            metric_name=LANGUAGES_USED_FILTERED_METRIC_NAME,
            value=len(languages_used_filtered),
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            metadata={
                LANGUAGES_USED_METRIC_KEY: languages_used,
                LANGUAGES_USED_FILTERED_METRIC_KEY: languages_used_filtered
            },
            message=f"Repository Languages Used (filtered) fetched successfully.",
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=LANGUAGES_USED_FILTERED_METRIC_KEY,
            metric_name=LANGUAGES_USED_FILTERED_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            metadata=None,
            message=str(exc),
        )