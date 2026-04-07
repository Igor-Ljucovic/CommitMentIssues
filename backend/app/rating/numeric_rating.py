from typing import Any

from app.rating.common import (
    FAILED_REQUIREMENT_RANGE_RATING,
    value_to_rating,
    is_in_range,
)
from app.schemas.analysis_request_schemas import (
    AnalysisSubcategoryConfig,
    DateRange,
    NumericRange,
)


def calculate_numeric_rating(
    value: Any,
    subcategory_config: AnalysisSubcategoryConfig,
) -> tuple[float, bool]:
    numeric_value = to_float(value)

    requirement_range = get_numeric_range_or_none(
        subcategory_config.requirement_range
    )
    recommended_range = get_numeric_range_or_none(
        subcategory_config.recommended_range
    )
    ideal_range = get_numeric_range_or_none(
        subcategory_config.ideal_range
    )

    if (
        requirement_range is not None
        and not is_in_range(
            numeric_value,
            requirement_range.get_min_float(),
            requirement_range.get_max_float(),
        )
    ):
        return FAILED_REQUIREMENT_RANGE_RATING, True

    rating = value_to_rating(
        value=numeric_value,
        recommended_min=recommended_range.get_min_float() if recommended_range else None,
        recommended_max=recommended_range.get_max_float() if recommended_range else None,
        ideal_min=ideal_range.get_min_float() if ideal_range else None,
        ideal_max=ideal_range.get_max_float() if ideal_range else None,
    )

    return round(rating, 2), False


def has_any_numeric_range_criteria(config: AnalysisSubcategoryConfig) -> bool:
    return any(
        isinstance(range_value, NumericRange) and range_value.has_any_value()
        for range_value in [
            config.requirement_range,
            config.recommended_range,
            config.ideal_range,
        ]
    )


def get_numeric_range_or_none(
    range_value: NumericRange | DateRange | None,
) -> NumericRange | None:
    if range_value is None:
        return None
    if not isinstance(range_value, NumericRange):
        raise ValueError("Expected a numeric range configuration.")
    if not range_value.has_any_value():
        return None
    return range_value


def to_float(value: Any) -> float:
    if value is None:
        raise ValueError("Metric value is missing and cannot be rated.")

    text = str(value).strip()
    if not text:
        raise ValueError("Metric value is empty and cannot be rated.")

    try:
        return float(text)
    except (TypeError, ValueError) as exc:
        raise ValueError(f'Value "{value}" is not a valid number for rating.') from exc