from typing import Any
from app.rating.metric_rating.common import DEFAULT_RATING
from app.rating.metric_rating.date_rating import calculate_date_rating, has_any_date_range_criteria
from app.rating.metric_rating.numeric_rating import calculate_numeric_rating, has_any_numeric_range_criteria
from app.schemas.analysis_request_schemas import AnalysisRequest, AnalysisSubcategoryConfig
from app.schemas.analysis_response_schemas import AnalysisResponse, RepositoryMetricResult


def calculate_metric_ratings(request: AnalysisRequest, response: AnalysisResponse) -> AnalysisResponse:
    for file in response.files:
        for repo in file.repositories:
            for metric in repo.metrics:
                subcategory_config = _find_subcategory_config(request, metric.metric_name)
                _apply_metric_rating(metric, subcategory_config)
    return response


def _find_subcategory_config(
    request: AnalysisRequest,
    metric_name: str,
) -> AnalysisSubcategoryConfig | None:
    for _, category in request.get_category_configs().items():
        config = category.subcategories.get(metric_name)
        if config is not None:
            return config
    return None


def _apply_metric_rating(
    result: RepositoryMetricResult,
    subcategory_config: AnalysisSubcategoryConfig | None,
) -> RepositoryMetricResult:
    rating, requirement_failed = _calculate_metric_rating(
        value=result.value,
        subcategory_config=subcategory_config,
    )
    result.rating = rating
    result.requirement_failed = requirement_failed
    return result


def _calculate_metric_rating(
    value: Any,
    subcategory_config: AnalysisSubcategoryConfig | None,
) -> tuple[float, bool]:
    if subcategory_config is None or not subcategory_config.has_any_rating_criteria():
        return DEFAULT_RATING, False
    if has_any_date_range_criteria(subcategory_config):
        return calculate_date_rating(value, subcategory_config)
    if has_any_numeric_range_criteria(subcategory_config):
        return calculate_numeric_rating(value, subcategory_config)
    return DEFAULT_RATING, False