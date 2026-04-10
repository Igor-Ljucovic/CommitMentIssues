from app.schemas.analysis_response_schemas import (
    AnalysisResponse,
    FileAnalysisResult,
    RepositoryAnalysisResult,
    RepositoryMetricResult,
)


EXCLUDED_METRIC_FIELDS = {"metric_key", "weight", "status", "message", "requirement_failed"}


def trim_analysis_response(response: AnalysisResponse) -> list[dict]:
    return [trim_file(file) for file in response.files]


def trim_file(file: FileAnalysisResult) -> dict:
    trimmed = file.model_dump()
    trimmed["repositories"] = [trim_repository(repo) for repo in file.repositories]

    _exclude_file_null_requirement_failed_repositories(trimmed)
    _exclude_file_null_status_failed_repositories(trimmed)

    return trimmed


def trim_repository(repo: RepositoryAnalysisResult) -> dict:
    trimmed = repo.model_dump()
    trimmed["metrics"] = [trim_metric(metric) for metric in repo.metrics]

    _exclude_repo_null_requirement_failed_metrics(trimmed)
    _exclude_repo_null_status_failed_metrics(trimmed)

    return trimmed


def trim_metric(metric: RepositoryMetricResult) -> dict:
    trimmed = metric.model_dump()

    for key in EXCLUDED_METRIC_FIELDS:
        trimmed.pop(key, None)

    _exclude_metric_rating_if_failed(metric, trimmed)

    return trimmed


def _exclude_file_null_requirement_failed_repositories(trimmed: dict) -> None:
    if trimmed.get("requirement_failed_repositories") is None:
        trimmed.pop("requirement_failed_repositories", None)


def _exclude_file_null_status_failed_repositories(trimmed: dict) -> None:
    if trimmed.get("status_failed_repositories") is None:
        trimmed.pop("status_failed_repositories", None)


def _exclude_repo_null_requirement_failed_metrics(trimmed: dict) -> None:
    if trimmed.get("requirement_failed_metrics") is None:
        trimmed.pop("requirement_failed_metrics", None)


def _exclude_repo_null_status_failed_metrics(trimmed: dict) -> None:
    if trimmed.get("status_failed_metrics") is None:
        trimmed.pop("status_failed_metrics", None)


def _exclude_metric_rating_if_failed(metric: RepositoryMetricResult, trimmed: dict) -> None:
    if metric.status != "success" or metric.requirement_failed:
        trimmed.pop("rating", None)