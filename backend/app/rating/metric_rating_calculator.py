from typing import Any

from app.rating.common import DEFAULT_RATING
from app.rating.date_rating import (
    calculate_date_rating,
    has_any_date_range_criteria,
)
from app.rating.numeric_rating import (
    calculate_numeric_rating,
    has_any_numeric_range_criteria,
)
from app.schemas.analysis_request_schemas import AnalysisSubcategoryConfig


def calculate_metric_rating(
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