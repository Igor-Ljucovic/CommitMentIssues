from collections.abc import Callable
from typing import Any


def count_matching_tree_entries(
    tree_entries: list[dict[str, Any]],
    predicate: Callable[[dict[str, Any]], bool],
) -> int:
    return sum(
        1
        for entry in tree_entries
        if predicate(entry)
    )


def filter_matching_tree_entries(
    tree_entries: list[dict[str, Any]],
    predicate: Callable[[dict[str, Any]], bool],
) -> list[dict[str, Any]]:
    return [
        entry
        for entry in tree_entries
        if predicate(entry)
    ]