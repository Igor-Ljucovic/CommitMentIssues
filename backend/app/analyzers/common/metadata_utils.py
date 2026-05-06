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


def get_transient_value(
    prior_results: list[RepositoryMetricResult],
    metric_keys: list[str],
    key: str,
    expected_type: type[T],
) -> T | None:
    """Like get_metadata_value, but reads from _transient instead of metadata.
    Used to pass large non-JSON-serializable values between metric phases without
    including them in the API response (path to a cached repository tarball
    downloaded by one metric and reused by others)."""
    metric = next(
        (
            metric
            for metric in prior_results
            if metric.metric_key in metric_keys
        ),
        None,
    )

    if metric is None:
        return None

    value = metric._transient.get(key)

    if not isinstance(value, expected_type):
        return None

    return value