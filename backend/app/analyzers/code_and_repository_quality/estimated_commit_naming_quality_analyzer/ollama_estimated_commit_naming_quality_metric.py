from app.analyzers.code_and_repository_quality.estimated_commit_naming_quality_analyzer.estimated_commit_naming_quality_constants import (
    COMMIT_MESSAGES,
    ESTIMATED_COMMIT_NAMING_QUALITY_CATEGORY_NAME,
    ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_KEY,
    ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_NAME,
    ESTIMATED_COMMIT_NAMING_QUALITY_SUBCATEGORY_NAME,
)
from app.analyzers.code_and_repository_quality.estimated_commit_naming_quality_analyzer.estimated_commit_naming_quality_fetch import (
    fetch_estimated_commit_naming_quality_data,
)
from app.analyzers.code_and_repository_quality.estimated_commit_naming_quality_analyzer.ai_estimated_commit_naming_quality_prompt import (
    build_estimated_commit_naming_quality_prompt,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.services.api.local_llm_service import analyze_metric_with_local_llm


async def get_ollama_estimated_commit_naming_quality_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        ESTIMATED_COMMIT_NAMING_QUALITY_CATEGORY_NAME,
        ESTIMATED_COMMIT_NAMING_QUALITY_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        result = await fetch_estimated_commit_naming_quality_data(
            owner=owner,
            repository_name=repository_name,
        )

        prompt = build_estimated_commit_naming_quality_prompt(result[COMMIT_MESSAGES])
        ai_result = await analyze_metric_with_local_llm(prompt)

        rating = ai_result.get("rating")
        explanation = ai_result.get("explanation")

        if not isinstance(rating, float):
            raise RuntimeError("Ollama did not return a valid numeric rating.")

        if not isinstance(explanation, str) or not explanation.strip():
            raise RuntimeError("Ollama did not return a valid explanation.")

        return RepositoryMetricResult(
            metric_key=ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_KEY,
            metric_name=ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_NAME,
            value=round(rating * 0.1, 2),
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            message=explanation,
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_KEY,
            metric_name=ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            message=str(exc),
        )