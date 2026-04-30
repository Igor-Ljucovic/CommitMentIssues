from app.analyzers.documentation.estimated_github_wiki_quality_analyzer.estimated_github_wiki_quality_constants import (
    ESTIMATED_GITHUB_WIKI_QUALITY_CATEGORY_NAME,
    ESTIMATED_GITHUB_WIKI_QUALITY_METRIC_KEY,
    ESTIMATED_GITHUB_WIKI_QUALITY_METRIC_NAME,
    ESTIMATED_GITHUB_WIKI_QUALITY_SUBCATEGORY_NAME,
    NUM_CTX,
)
from app.analyzers.documentation.estimated_github_wiki_quality_analyzer.estimated_github_wiki_quality_fetch import (
    fetch_estimated_github_wiki_quality_input,
)
from app.analyzers.documentation.estimated_github_wiki_quality_analyzer.estimated_github_wiki_quality_prompt import (
    build_estimated_github_wiki_quality_prompt,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.services.openai_service import rate_metric_with_openai
from app.core.config import settings


async def get_github_wiki_quality_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        ESTIMATED_GITHUB_WIKI_QUALITY_CATEGORY_NAME,
        ESTIMATED_GITHUB_WIKI_QUALITY_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        wiki_data = await fetch_estimated_github_wiki_quality_input(
            owner=owner,
            repository_name=repository_name,
        )

        # Skip an unnecessary OpenAI API call if there's no GitHub Wiki Page
        if not wiki_data:
            return RepositoryMetricResult(
                metric_key=ESTIMATED_GITHUB_WIKI_QUALITY_METRIC_KEY,
                metric_name=ESTIMATED_GITHUB_WIKI_QUALITY_METRIC_NAME,
                value=0.0,
                weight=subcategory_config.weight,
                status=MetricStatus.SUCCESS,
                message="GitHub Wiki not enabled or empty.",
            )

        prompt = build_estimated_github_wiki_quality_prompt(
            wiki_data=wiki_data,
            num_ctx=NUM_CTX,
        )

        ai_result = await rate_metric_with_openai(
            prompt=prompt,
            model=settings.OPENAI_MODEL_GPT41MINI,
        )

        return RepositoryMetricResult(
            metric_key=ESTIMATED_GITHUB_WIKI_QUALITY_METRIC_KEY,
            metric_name=ESTIMATED_GITHUB_WIKI_QUALITY_METRIC_NAME,
            value=round(ai_result["rating"] / 100, 2),
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            message=ai_result["explanation"],
        )

    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=ESTIMATED_GITHUB_WIKI_QUALITY_METRIC_KEY,
            metric_name=ESTIMATED_GITHUB_WIKI_QUALITY_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            message=str(exc),
        )