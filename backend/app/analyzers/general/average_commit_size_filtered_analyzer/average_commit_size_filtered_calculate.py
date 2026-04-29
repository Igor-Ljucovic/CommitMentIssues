from typing import Any
from statistics import mean


async def average_commit_size_filtered_calculate(
    commit_size_samples: list[dict[str, Any]],
    outlier_multiplier: float
) -> int:
    """
    A commit is considered an outlier if its size is greater than:
        average_commit_size * outlier_multiplier

    Example:
        If the initial average commit size is 200 (INCLUDING outliers)
        and outlier_multiplier is 3.0, commits larger than 600 lines 
        will be ignored when recalculating the filtered average
    """
    commit_sizes = [
        (commit.get("additions") or 0)
        + (commit.get("deletions") or 0)
        for commit in commit_size_samples
    ]

    if not commit_sizes:
        return 0

    initial_average = mean(commit_sizes)

    filtered_commit_sizes = [
        commit_size
        for commit_size in commit_sizes
        if commit_size <= initial_average * outlier_multiplier
    ]

    if not filtered_commit_sizes:
        return round(initial_average)

    filtered_average = mean(filtered_commit_sizes)

    return round(filtered_average)