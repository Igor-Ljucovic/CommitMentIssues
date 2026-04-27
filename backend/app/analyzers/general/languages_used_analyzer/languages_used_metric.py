from app.analyzers.general.languages_used_analyzer.languages_used_fetch import (
    fetch_languages_used,
)
from app.analyzers.general.languages_used_analyzer.languages_used_constants import (
    LANGUAGES_USED_METRIC_KEY,
    LANGUAGES_USED_METRIC_NAME,
    LANGUAGES_USED_CATEGORY_NAME,
    LANGUAGES_USED_SUBCATEGORY_NAME,
)
from app.analyzers.general.languages_used_filtered_analyzer.languages_used_filtered_constants import (
    LANGUAGES_USED_FILTERED_METRIC_KEY
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.analyzers.common.metadata_utils import get_metadata_value


async def _get_languages_used_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
    *,
    languages_used: list | None = None,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        LANGUAGES_USED_CATEGORY_NAME,
        LANGUAGES_USED_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        if languages_used is None:
            result = await fetch_languages_used(
                owner=owner,
                repository_name=repository_name,
            )

            languages_used = result[LANGUAGES_USED_METRIC_KEY]

        return RepositoryMetricResult(
            metric_key=LANGUAGES_USED_METRIC_KEY,
            metric_name=LANGUAGES_USED_METRIC_NAME,
            value=len(languages_used),
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            metadata={
                LANGUAGES_USED_METRIC_KEY: languages_used,
            },
            message=f"Repository Languages Used fetched successfully.",
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=LANGUAGES_USED_METRIC_KEY,
            metric_name=LANGUAGES_USED_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            metadata=None,
            message=str(exc),
        )
    

async def get_languages_used_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
    prior_results: list[RepositoryMetricResult],
) -> RepositoryMetricResult | None:
    return await _get_languages_used_metric(
        request,
        repository,
        languages_used=get_metadata_value(
            prior_results,
            lambda metric: metric.metric_key == LANGUAGES_USED_FILTERED_METRIC_KEY,
            LANGUAGES_USED_METRIC_KEY,
            list,
        ),
    )