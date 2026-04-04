from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from app.schemas.analysis_request_schemas import (
    AnalysisSubcategoryConfig,
    DateRange,
    NumericRange,
)


DEFAULT_RATING = 10.0
FAILED_REQUIREMENT_RANGE_RATING = -1.0
MIN_RATING = 0.0
MAX_RATING = 10.0


def calculate_metric_rating(
    value: Any,
    subcategory_config: AnalysisSubcategoryConfig | None,
) -> tuple[float, bool]:
    if subcategory_config is None or not subcategory_config.has_any_rating_criteria():
        return DEFAULT_RATING, False

    if _has_any_date_range_criteria(subcategory_config):
        return _calculate_date_rating(value, subcategory_config)

    if _has_any_numeric_range_criteria(subcategory_config):
        return _calculate_numeric_rating(value, subcategory_config)

    return DEFAULT_RATING, False


def _calculate_numeric_rating(
    value: Any,
    subcategory_config: AnalysisSubcategoryConfig,
) -> tuple[float, bool]:
    numeric_value = _to_decimal(value)

    hard_requirement_range = _get_numeric_range_or_none(
        subcategory_config.requirementRange
    )
    recommended_range = _get_numeric_range_or_none(
        subcategory_config.recommendedRange
    )
    ideal_range = _get_numeric_range_or_none(
        subcategory_config.idealRange
    )

    if (
        hard_requirement_range is not None
        and not _is_in_numeric_range(numeric_value, hard_requirement_range)
    ):
        return FAILED_REQUIREMENT_RANGE_RATING, True

    rating = _calculate_numeric_or_date_style_rating(
        value=numeric_value,
        hard_requirement_min=(
            hard_requirement_range.get_min_decimal()
            if hard_requirement_range
            else None
        ),
        hard_requirement_max=(
            hard_requirement_range.get_max_decimal()
            if hard_requirement_range
            else None
        ),
        recommended_min=(
            recommended_range.get_min_decimal()
            if recommended_range
            else None
        ),
        recommended_max=(
            recommended_range.get_max_decimal()
            if recommended_range
            else None
        ),
        ideal_min=ideal_range.get_min_decimal() if ideal_range else None,
        ideal_max=ideal_range.get_max_decimal() if ideal_range else None,
    )

    return float(round(rating, 2)), False


def _calculate_date_rating(
    value: Any,
    subcategory_config: AnalysisSubcategoryConfig,
) -> tuple[float, bool]:
    date_value = _to_date(value)
    ordinal_value = Decimal(date_value.toordinal())

    hard_requirement_range = _get_date_range_or_none(
        subcategory_config.requirementRange
    )
    recommended_range = _get_date_range_or_none(
        subcategory_config.recommendedRange
    )
    ideal_range = _get_date_range_or_none(
        subcategory_config.idealRange
    )

    if (
        hard_requirement_range is not None
        and not _is_in_date_range(date_value, hard_requirement_range)
    ):
        return FAILED_REQUIREMENT_RANGE_RATING, True

    rating = _calculate_numeric_or_date_style_rating(
        value=ordinal_value,
        hard_requirement_min=(
            _date_to_decimal_ordinal(hard_requirement_range.get_after_date())
            if hard_requirement_range
            else None
        ),
        hard_requirement_max=(
            _date_to_decimal_ordinal(hard_requirement_range.get_before_date())
            if hard_requirement_range
            else None
        ),
        recommended_min=(
            _date_to_decimal_ordinal(recommended_range.get_after_date())
            if recommended_range
            else None
        ),
        recommended_max=(
            _date_to_decimal_ordinal(recommended_range.get_before_date())
            if recommended_range
            else None
        ),
        ideal_min=(
            _date_to_decimal_ordinal(ideal_range.get_after_date())
            if ideal_range
            else None
        ),
        ideal_max=(
            _date_to_decimal_ordinal(ideal_range.get_before_date())
            if ideal_range
            else None
        ),
    )

    return float(round(rating, 2)), False


def _calculate_numeric_or_date_style_rating(
    value: Decimal,
    hard_requirement_min: Decimal | None,
    hard_requirement_max: Decimal | None,
    recommended_min: Decimal | None,
    recommended_max: Decimal | None,
    ideal_min: Decimal | None,
    ideal_max: Decimal | None,
) -> Decimal:

    if ideal_min is not None or ideal_max is not None:
        if _is_in_simple_range(value, ideal_min, ideal_max):
            return Decimal("10")

    if recommended_min is None and recommended_max is None:
        return Decimal("10")

    if not _is_in_simple_range(value, recommended_min, recommended_max):
        return Decimal("0")

    if ideal_min is not None or ideal_max is not None:
        return _scale_value_between_recommended_and_ideal(
            value=value,
            recommended_min=recommended_min,
            recommended_max=recommended_max,
            ideal_min=ideal_min,
            ideal_max=ideal_max,
        )

    return _scale_inside_range_with_center_peak(
        value=value,
        range_min=recommended_min,
        range_max=recommended_max,
    )


def _scale_value_between_recommended_and_ideal(
    value: Decimal,
    recommended_min: Decimal | None,
    recommended_max: Decimal | None,
    ideal_min: Decimal | None,
    ideal_max: Decimal | None,
) -> Decimal:
    """
    Example:
    recommended = [10, 40]
    ideal = [25, 40]

    20 is 10/15 of the way from 10 to 25 => 6.66/10
    12 is 2/15 of the way from 10 to 25 => 1.33/10
    """

    if _is_in_simple_range(value, ideal_min, ideal_max):
        return Decimal("10")

    if ideal_min is not None and value < ideal_min:
        if recommended_min is None:
            return Decimal("0")

        distance_total = ideal_min - recommended_min
        if distance_total <= 0:
            return Decimal("0")

        distance_progress = value - recommended_min
        if distance_progress <= 0:
            return Decimal("0")

        return _clamp_decimal((distance_progress / distance_total) * Decimal("10"))

    if ideal_max is not None and value > ideal_max:
        if recommended_max is None:
            return Decimal("0")

        distance_total = recommended_max - ideal_max
        if distance_total <= 0:
            return Decimal("0")

        distance_progress = recommended_max - value
        if distance_progress <= 0:
            return Decimal("0")

        return _clamp_decimal((distance_progress / distance_total) * Decimal("10"))

    return Decimal("10")


def _scale_inside_range_with_center_peak(
    value: Decimal,
    range_min: Decimal | None,
    range_max: Decimal | None,
) -> Decimal:
    """
    Used when ideal range is missing but recommended range exists.

    Rule:
    - center of recommended range = rating 10
    - edges of recommended range = rating 0
    - linear interpolation in between (1/3 of the points 1/3 of the way through)
    """

    if range_min is None and range_max is None:
        return Decimal("10")

    if range_min is not None and range_max is not None:
        if range_max <= range_min:
            return Decimal("0")

        midpoint = (range_min + range_max) / Decimal("2")
        half_width = (range_max - range_min) / Decimal("2")

        if half_width == 0:
            return Decimal("10") if value == midpoint else Decimal("0")

        distance_from_center = abs(value - midpoint)
        if distance_from_center >= half_width:
            return Decimal("0")

        return _clamp_decimal(
            (Decimal("1") - (distance_from_center / half_width)) * Decimal("10")
        )

    return Decimal("10")


def _has_any_numeric_range_criteria(config: AnalysisSubcategoryConfig) -> bool:
    return any(
        isinstance(range_value, NumericRange) and range_value.has_any_value()
        for range_value in [
            config.requirementRange,
            config.recommendedRange,
            config.idealRange,
        ]
    )


def _has_any_date_range_criteria(config: AnalysisSubcategoryConfig) -> bool:
    return any(
        isinstance(range_value, DateRange) and range_value.has_any_value()
        for range_value in [
            config.requirementRange,
            config.recommendedRange,
            config.idealRange,
        ]
    )


def _get_numeric_range_or_none(
    range_value: NumericRange | DateRange | None,
) -> NumericRange | None:
    if range_value is None:
        return None
    if not isinstance(range_value, NumericRange):
        raise ValueError("Expected a numeric range configuration.")
    if not range_value.has_any_value():
        return None
    return range_value


def _get_date_range_or_none(
    range_value: NumericRange | DateRange | None,
) -> DateRange | None:
    if range_value is None:
        return None
    if not isinstance(range_value, DateRange):
        raise ValueError("Expected a date range configuration.")
    if not range_value.has_any_value():
        return None
    return range_value


def _to_decimal(value: Any) -> Decimal:
    if value is None:
        raise ValueError("Metric value is missing and cannot be rated.")

    try:
        return Decimal(str(value).strip())
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f'Value "{value}" is not a valid number for rating.') from exc


def _to_date(value: Any) -> date:
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


def _is_in_numeric_range(value: Decimal, range_value: NumericRange) -> bool:
    return _is_in_simple_range(
        value=value,
        min_value=range_value.get_min_decimal(),
        max_value=range_value.get_max_decimal(),
    )


def _is_in_date_range(value: date, range_value: DateRange) -> bool:
    after_date = range_value.get_after_date()
    before_date = range_value.get_before_date()

    if after_date is not None and value < after_date:
        return False

    if before_date is not None and value > before_date:
        return False

    return True


def _is_in_simple_range(
    value: Decimal,
    min_value: Decimal | None,
    max_value: Decimal | None,
) -> bool:
    if min_value is not None and value < min_value:
        return False

    if max_value is not None and value > max_value:
        return False

    return True


def _date_to_decimal_ordinal(value: date | None) -> Decimal | None:
    if value is None:
        return None
    return Decimal(value.toordinal())


def _clamp_decimal(value: Decimal) -> Decimal:
    if value < Decimal("0"):
        return Decimal("0")
    if value > Decimal("10"):
        return Decimal("10")
    return value