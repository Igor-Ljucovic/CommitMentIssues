from collections.abc import Awaitable, Callable

from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import (
    AnalysisResponse,
    FileAnalysisResult,
    RepositoryAnalysisResult,
    RepositoryMetricResult,
)


MetricExecutor = Callable[
    [AnalysisRequest, RepositoryInput],
    Awaitable[RepositoryMetricResult | None],
]


async def _append_metric_if_present(
    metrics: list[RepositoryMetricResult],
    executor: MetricExecutor,
    request: AnalysisRequest,
    repository: RepositoryInput,
) -> None:
    metric = await executor(request, repository)

    if metric is not None:
        metrics.append(metric)


async def run_repository_analysis(
    request: AnalysisRequest,
    metric_executors: list[MetricExecutor],
    no_repositories_warning: str,
) -> AnalysisResponse:
    warnings: list[str] = []

    repositories = request.get_repository_inputs()

    if not repositories:
        warnings.append(no_repositories_warning)
        return AnalysisResponse(files=[], warnings=warnings)

    file_map: dict[int | None, FileAnalysisResult] = {}

    for repository in repositories:
        metrics: list[RepositoryMetricResult] = []

        for executor in metric_executors:
            await _append_metric_if_present(
                metrics=metrics,
                executor=executor,
                request=request,
                repository=repository,
            )

        repo_result = RepositoryAnalysisResult(
            repository_url=repository.repo_url,
            metrics=metrics,
        )

        file_id = repository.source_file_id
        file_name = repository.source_file_name or "Unknown"

        if file_id not in file_map:
            file_map[file_id] = FileAnalysisResult(
                file_id=file_id,
                file_name=file_name,
                repositories=[],
            )

        file_map[file_id].repositories.append(repo_result)

    return AnalysisResponse(
        files=list(file_map.values()),
        warnings=warnings,
    )