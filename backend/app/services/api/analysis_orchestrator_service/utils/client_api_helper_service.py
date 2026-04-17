import asyncio
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

async def _analyze_repository(
    request: AnalysisRequest,
    repository: RepositoryInput,
    metric_executors: list[MetricExecutor],
) -> RepositoryAnalysisResult:
    # All metrics for 1 repository run concurrently.
    metric_results = await asyncio.gather(
        *(executor(request, repository) for executor in metric_executors)
    )

    metrics = [m for m in metric_results if m is not None]

    return RepositoryAnalysisResult(
        repository_url=repository.repo_url,
        metrics=metrics,
    )


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

    # All repositories run concurrently
    repo_results = await asyncio.gather(
        *(
            _analyze_repository(request, repository, metric_executors)
            for repository in repositories
        )
    )

    # Preserve file order
    file_map: dict[int | None, FileAnalysisResult] = {}

    for repository, repo_result in zip(repositories, repo_results):
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