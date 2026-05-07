import asyncio
from collections.abc import Awaitable, Callable

from app.schemas.analysis_request_schemas import AnalysisRequest, RepositoryInput
from app.schemas.analysis_response_schemas import (
    AnalysisResponse,
    FileAnalysisResult,
    RepositoryAnalysisResult,
    RepositoryMetricResult,
)
from app.analyzers.common.constants import REPOSITORY_TARBALL_METRIC_KEY
from app.services.github_repository_download_service import ensure_repository_tarball

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
    subsequent_phases: list[list[PostMetricExecutor]] | None = None,
    tarball_requiring_subcategories: frozenset[tuple[str, str]] | None = None,
) -> RepositoryAnalysisResult:
    # Start the tarball repository download as a background task (if any enabled metric needs it)
    # so it runs concurrently with phase 1 rather than blocking it.
    tarball_task: asyncio.Task | None = None
    if tarball_requiring_subcategories and any(
        request.get_subcategory_config(cat, subcat) is not None
        for cat, subcat in tarball_requiring_subcategories
    ):
        try:
            owner, repository_name = repository.get_owner_and_repository_name()
            tarball_task = asyncio.create_task(
                ensure_repository_tarball(owner, repository_name)
            )
        except Exception:
            pass

    phase1_results = await asyncio.gather(
        *(executor(request, repository) for executor in first_phase)
    )
    all_metrics: list[RepositoryMetricResult] = [m for m in phase1_results if m is not None]

    # Resolve the tarball repository download task before subsequent phases need it.
    context: list[RepositoryMetricResult] = []
    if tarball_task is not None:
        try:
            tarball_path = await tarball_task
            tarball_result = RepositoryMetricResult(
                metric_key=REPOSITORY_TARBALL_METRIC_KEY,
                metric_name="Repository Tarball",
                status="success",
                value=None,
            )
            tarball_result._transient["tarball_path"] = tarball_path
            context.append(tarball_result)
        except Exception:
            pass

    for phase in (subsequent_phases or []):
        phase_results = await asyncio.gather(
            *(executor(request, repository, context + all_metrics) for executor in phase)
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
    tarball_requiring_subcategories: frozenset[tuple[str, str]] | None = None,
) -> AnalysisResponse:
    warnings: list[str] = []
    repositories = request.get_repository_inputs()

    if not repositories:
        warnings.append(no_repositories_warning)
        return AnalysisResponse(files=[], warnings=warnings)

    repo_results = await asyncio.gather(
        *(
            _analyze_repository(
                request, repository, metric_executors, subsequent_phases,
                tarball_requiring_subcategories,
            )
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
