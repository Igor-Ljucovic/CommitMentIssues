from typing import Any

from statistics import median


async def median_commit_size_calculate(
    commit_size_samples: list[dict[str, Any]],
) -> int:
    commit_sizes = [
        (commit.get("additions") or 0)
        + (commit.get("deletions") or 0)
        for commit in commit_size_samples
    ]

    return (
        median(commit_sizes)
        if commit_sizes
        else 0
    )