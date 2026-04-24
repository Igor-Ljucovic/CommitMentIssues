from app.analyzers.documentation.estimated_readme_quality_analyzer.estimated_readme_quality_constants import (
    ESTIMATED_README_QUALITY_CATEGORY_NAME,
    ESTIMATED_README_QUALITY_METRIC_KEY,
    ESTIMATED_README_QUALITY_METRIC_NAME,
    ESTIMATED_README_QUALITY_SUBCATEGORY_NAME,
)
from app.analyzers.documentation.estimated_readme_quality_analyzer.estimated_readme_quality_fetch import (
    fetch_estimated_readme_quality_input,
)
from app.analyzers.documentation.estimated_readme_quality_analyzer.estimated_readme_quality_prompt import (
    build_estimated_readme_quality_prompt,
)
from app.common.metric_status import MetricStatus
from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.services.openai_service import rate_metric_with_openai
from app.core.config import settings


async def get_github_readme_quality_metric(
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> RepositoryMetricResult | None:
    subcategory_config = request.get_subcategory_config(
        ESTIMATED_README_QUALITY_CATEGORY_NAME,
        ESTIMATED_README_QUALITY_SUBCATEGORY_NAME,
    )

    if subcategory_config is None:
        return None

    try:
        owner, repository_name = repository.get_owner_and_repository_name()

        readme_data = await fetch_estimated_readme_quality_input(
            owner=owner,
            repository_name=repository_name,
        )

        prompt = build_estimated_readme_quality_prompt(readme_data=readme_data)
        ai_result = await rate_metric_with_openai(
            prompt=prompt, 
            model=settings.OPENAI_MODEL,
        )

        rating = round(float(ai_result["rating"]) / 100, 2)
        
        explanation = str(ai_result["explanation"]).strip()

        return RepositoryMetricResult(
            metric_key=ESTIMATED_README_QUALITY_METRIC_KEY,
            metric_name=ESTIMATED_README_QUALITY_METRIC_NAME,
            value=rating,
            weight=subcategory_config.weight,
            status=MetricStatus.SUCCESS,
            message=explanation,
        )
    except Exception as exc:
        return RepositoryMetricResult(
            metric_key=ESTIMATED_README_QUALITY_METRIC_KEY,
            metric_name=ESTIMATED_README_QUALITY_METRIC_NAME,
            value=None,
            weight=None,
            status=MetricStatus.FAILED,
            message=str(exc),
        )