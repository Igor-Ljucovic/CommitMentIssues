import asyncio
from collections.abc import Awaitable, Callable

from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import (
    AnalysisResponse,
    FileAnalysisResult,
    RepositoryAnalysisResult,
    RepositoryMetricResult,
)

# Phase 1 executors — no prior results available yet.
MetricExecutor = Callable[
    [AnalysisRequest, RepositoryInput],
    Awaitable[RepositoryMetricResult | None],
]

# Phase 2+ executors — receive all accumulated results from prior phases.
PostMetricExecutor = Callable[
    [AnalysisRequest, RepositoryInput, list[RepositoryMetricResult]],
    Awaitable[RepositoryMetricResult | None],
]


async def _analyze_repository(
    request: AnalysisRequest,
    repository: RepositoryInput,
    first_phase: list[MetricExecutor],
    # Phase 2, 3, 4... - each phase gets all accumulated results so far.
    # The subsequent_phases helps us avoid unnecessary API calls while
    # still letting us use async. 
    # This can be useful for metrics that depend on other metrics 
    # (e.g. average commits per month depends on total commits, first/last commit date)
    subsequent_phases: list[list[PostMetricExecutor]] | None = None,
) -> RepositoryAnalysisResult:
    phase1_results = await asyncio.gather(
        *(executor(request, repository) for executor in first_phase)
    )
    all_metrics: list[RepositoryMetricResult] = [m for m in phase1_results if m is not None]

    for phase in (subsequent_phases or []):
        phase_results = await asyncio.gather(
            *(executor(request, repository, all_metrics) for executor in phase)
        )
        all_metrics += [m for m in phase_results if m is not None]

    return RepositoryAnalysisResult(
        repository_url=repository.repo_url,
        metrics=all_metrics,
    )


async def analyze_repository(
    request: AnalysisRequest,
    metric_executors: list[MetricExecutor],
    no_repositories_warning: str,
    subsequent_phases: list[list[PostMetricExecutor]] | None = None,
) -> AnalysisResponse:
    warnings: list[str] = []
    repositories = request.get_repository_inputs()

    if not repositories:
        warnings.append(no_repositories_warning)
        return AnalysisResponse(files=[], warnings=warnings)

    repo_results = await asyncio.gather(
        *(
            _analyze_repository(request, repository, metric_executors, subsequent_phases)
            for repository in repositories
        )
    )

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