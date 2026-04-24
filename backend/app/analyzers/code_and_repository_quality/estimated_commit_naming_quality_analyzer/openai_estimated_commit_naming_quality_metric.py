from app.analyzers.code_and_repository_quality.estimated_commit_naming_quality_analyzer.estimated_commit_naming_quality_constants import (
    COMMIT_MESSAGES,
    ESTIMATED_COMMIT_NAMING_QUALITY_CATEGORY_NAME,
    ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_KEY,
    ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_NAME,
    ESTIMATED_COMMIT_NAMING_QUALITY_SUBCATEGORY_NAME,
    NUM_CTX
)
from app.analyzers.code_and_repository_quality.estimated_commit_naming_quality_analyzer.estimated_commit_naming_quality_fetch import (
    fetch_estimated_commit_naming_quality_data,
)
from app.analyzers.code_and_repository_quality.estimated_commit_naming_quality_analyzer.ai_estimated_commit_naming_quality_prompt import (
    build_estimated_commit_naming_quality_prompt,
)
from app.services.openai_service import rate_metric_with_openai
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.core.config import settings


async def get_openai_estimated_commit_naming_quality_metric(
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

        prompt = build_estimated_commit_naming_quality_prompt(
            commit_messages=result[COMMIT_MESSAGES],
            num_ctx=subcategory_config.num_ctx,
        )
        ai_result = await rate_metric_with_openai(
            prompt=prompt, 
            model=settings.OPENAI_MODEL_GPT41MINI,
            num_ctx=NUM_CTX,
        )

        rating = ai_result.get("rating")
        explanation = ai_result.get("explanation")

        if not isinstance(rating, float):
            raise RuntimeError("OpenAI did not return a valid numeric rating.")

        if not isinstance(explanation, str) or not explanation.strip():
            raise RuntimeError("OpenAI did not return a valid explanation.")

        return RepositoryMetricResult(
            metric_key=ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_KEY,
            metric_name=ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_NAME,
            value=round(rating / 100, 2),
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