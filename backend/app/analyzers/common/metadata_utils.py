from typing import TypeVar

from app.schemas.analysis_response_schemas import RepositoryMetricResult

T = TypeVar("T")


def get_metadata_value(
    prior_results: list[RepositoryMetricResult],
    metric_keys: list[str],
    key: str,
    expected_type: type[T],
) -> T | None:
    metric = next(
        (
            metric
            for metric in prior_results
            if metric.metric_key in metric_keys
        ),
        None,
    )

    if metric is None or metric.metadata is None:
        return None

    value = metric.metadata.get(key)

    if not isinstance(value, expected_type):
        return None

    return value