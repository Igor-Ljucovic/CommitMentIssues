from datetime import date, datetime
from typing import Any

from app.rating.metric_rating.common import (
    FAILED_REQUIREMENT_RANGE_RATING,
    value_to_rating,
)
from app.schemas.analysis_request_schemas import (
    AnalysisSubcategoryConfig,
    DateRange,
    NumericRange,
)


def calculate_date_rating(
    value: Any,
    subcategory_config: AnalysisSubcategoryConfig,
) -> tuple[float, bool]:
    date_value = to_date(value)
    ordinal_value = float(date_value.toordinal())

    requirement_range = get_date_range_or_none(subcategory_config.requirement_range)
    recommended_range = get_date_range_or_none(subcategory_config.recommended_range)
    ideal_range = get_date_range_or_none(subcategory_config.ideal_range)

    if (requirement_range is not None and not is_in_date_range(date_value, requirement_range)):
        return FAILED_REQUIREMENT_RANGE_RATING, True

    rating = value_to_rating(
        value=ordinal_value,
        recommended_min=(
            date_to_float_ordinal(recommended_range.get_after_date())
            if recommended_range
            else None
        ),
        recommended_max=(
            date_to_float_ordinal(recommended_range.get_before_date())
            if recommended_range
            else None
        ),
        ideal_min=(
            date_to_float_ordinal(ideal_range.get_after_date())
            if ideal_range
            else None
        ),
        ideal_max=(
            date_to_float_ordinal(ideal_range.get_before_date())
            if ideal_range
            else None
        ),
    )

    return round(rating, 2), False


def has_any_date_range_criteria(config: AnalysisSubcategoryConfig) -> bool:
    return any(
        isinstance(range_value, DateRange) and range_value.has_any_value()
        for range_value in [
            config.requirement_range,
            config.recommended_range,
            config.ideal_range,
        ]
    )


def get_date_range_or_none(
    range_value: NumericRange | DateRange | None,
) -> DateRange | None:
    if range_value is None:
        return None
    if not isinstance(range_value, DateRange):
        raise ValueError("Expected a date range configuration.")
    if not range_value.has_any_value():
        return None
    return range_value


def to_date(value: Any) -> date:
    if value is None:
        raise ValueError("Metric value is missing and cannot be rated.")

    if isinstance(value, date) and not isinstance(value, datetime):
        return value

    if isinstance(value, datetime):
        return value.date()

    text = str(value).strip()
    if not text:
        raise ValueError("Metric value is empty and cannot be rated as a date.")

    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f'Value "{value}" is not a valid ISO date.') from exc


def is_in_date_range(value: date, range_value: DateRange) -> bool:
    after_date = range_value.get_after_date()
    before_date = range_value.get_before_date()

    if after_date is not None and value < after_date:
        return False

    if before_date is not None and value > before_date:
        return False

    return True


def date_to_float_ordinal(value: date | None) -> float | None:
    if value is None:
        return None
    return float(value.toordinal())