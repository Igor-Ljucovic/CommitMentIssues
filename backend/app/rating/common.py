DEFAULT_RATING = 10.0
FAILED_REQUIREMENT_RANGE_RATING = 0.0


def value_to_rating(
    value: float,
    recommended_min: float | None,
    recommended_max: float | None,
    ideal_min: float | None,
    ideal_max: float | None,
) -> float:
    if ideal_min is not None or ideal_max is not None:
        if is_in_range(value, ideal_min, ideal_max):
            return 10.0

    if recommended_min is None and recommended_max is None:
        return 10.0

    if not is_in_range(value, recommended_min, recommended_max):
        return 0.0

    if ideal_min is not None or ideal_max is not None:
        return scale_between_recommended_and_ideal(
            value=value,
            recommended_min=recommended_min,
            recommended_max=recommended_max,
            ideal_min=ideal_min,
            ideal_max=ideal_max,
        )

    return scale_towards_center(
        value=value,
        range_min=recommended_min,
        range_max=recommended_max,
    )


def scale_between_recommended_and_ideal(
    value: float,
    recommended_min: float | None,
    recommended_max: float | None,
    ideal_min: float | None,
    ideal_max: float | None,
) -> float:
    """
    Example:
    recommended = [10, 40]
    ideal = [25, 40]

    20 is 10/15 of the way from 10 to 25 => 6.66/10
    """

    if is_in_range(value, ideal_min, ideal_max):
        return 10.0

    if ideal_min is not None and value < ideal_min:
        if recommended_min is None:
            return 0.0

        distance_total = ideal_min - recommended_min
        if distance_total <= 0:
            return 0.0

        distance_progress = value - recommended_min
        if distance_progress <= 0:
            return 0.0

        return clamp_rating((distance_progress / distance_total) * 10.0)

    if ideal_max is not None and value > ideal_max:
        if recommended_max is None:
            return 0.0

        distance_total = recommended_max - ideal_max
        if distance_total <= 0:
            return 0.0

        distance_progress = recommended_max - value
        if distance_progress <= 0:
            return 0.0

        return clamp_rating((distance_progress / distance_total) * 10.0)

    return 10.0


def scale_towards_center(
    value: float,
    range_min: float | None,
    range_max: float | None,
) -> float:
    """
    - center = 10
    - edges = 0
    - 1/3 of the way from center to edge = 6.66
    """

    if range_min is None and range_max is None:
        return 10.0

    if range_min is not None and range_max is not None:
        if range_max <= range_min:
            return 0.0

        midpoint = (range_min + range_max) / 2.0
        half_width = (range_max - range_min) / 2.0

        if half_width == 0:
            return 10.0 if value == midpoint else 0.0

        distance_from_center = abs(value - midpoint)
        if distance_from_center >= half_width:
            return 0.0

        return clamp_rating((1.0 - (distance_from_center / half_width)) * 10.0)

    return 10.0


def is_in_range(
    value: float,
    min_value: float | None,
    max_value: float | None,
) -> bool:
    if min_value is not None and value < min_value:
        return False

    if max_value is not None and value > max_value:
        return False

    return True


def clamp_rating(value: float) -> float:
    if value < 0.0:
        return 0.0
    if value > 10.0:
        return 10.0
    return value