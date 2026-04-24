from collections.abc import Callable
from typing import TypeVar

from app.schemas.analysis_response_schemas import RepositoryMetricResult

T = TypeVar("T")


CHARACTERS_PER_TOKEN_ESTIMATE = 3.5
RESERVED_OUTPUT_TOKENS = 300


def prompt_character_limit(
    num_ctx: int,
    reserved_output_tokens: int = RESERVED_OUTPUT_TOKENS,
) -> int:
    token_limit = max(num_ctx - reserved_output_tokens, 0)
    
    return int(token_limit * CHARACTERS_PER_TOKEN_ESTIMATE)


def get_metadata_value(
    prior_results: list[RepositoryMetricResult],
    predicate: Callable[[RepositoryMetricResult], bool],
    key: str,
    expected_type: type[T],
) -> T | None:
    metric = next(
        (
            metric
            for metric in prior_results
            if predicate(metric)
        ),
        None,
    )

    if metric is None or metric.metadata is None:
        return None

    value = metric.metadata.get(key)

    if not isinstance(value, expected_type):
        return None

    return value