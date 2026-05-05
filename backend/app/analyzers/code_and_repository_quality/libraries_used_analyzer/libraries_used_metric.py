from app.analyzers.code_and_repository_quality.libraries_used_analyzer.libraries_used_constants import (
    LIBRARIES_USED_CATEGORY_NAME,
    LIBRARIES_USED_METADATA_KEY,
    LIBRARIES_USED_METRIC_KEY,
    LIBRARIES_USED_METRIC_NAME,
    LIBRARIES_USED_SUBCATEGORY_NAME,
)
from app.analyzers.code_and_repository_quality.libraries_used_analyzer.libraries_used_fetch import (
    fetch_libraries_used,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult


async def get_libraries_used_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        LIBRARIES_USED_CATEGORY_NAME,
        LIBRARIES_USED_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        libraries_by_language = await fetch_libraries_used(
            owner=owner,
            repository_name=repository_name,
        )

        all_unique = {lib for libs in libraries_by_language.values() for lib in libs}
        detected_langs = [
            lang for lang, libs in libraries_by_language.items() if libs
        ]

        return RepositoryMetricResult(
            metric_key=LIBRARIES_USED_METRIC_KEY,
            metric_name=LIBRARIES_USED_METRIC_NAME,
            value=len(all_unique),
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            metadata={
                LIBRARIES_USED_METADATA_KEY: {
                    lang: sorted(libs)
                    for lang, libs in libraries_by_language.items()
                    if libs
                }
            },
            message=(
                f"Found {len(all_unique)} unique third-party "
                f"{'library' if len(all_unique) == 1 else 'libraries'}"
                f" across {', '.join(detected_langs) if detected_langs else 'no supported languages'}."
            ),
        )

    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=LIBRARIES_USED_METRIC_KEY,
            metric_name=LIBRARIES_USED_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            message=str(exc),
        )
