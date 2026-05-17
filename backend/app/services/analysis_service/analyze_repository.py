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
from app.services.repository_metrics_redis_cache_service import cache_metrics, get_cached_metrics

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


def _split_metric_executors_by_cache(
    executors: list,
    cached_dict: dict[str, RepositoryMetricResult],
    request: AnalysisRequest,
) -> tuple[list, list[RepositoryMetricResult]]:
    """
    Split executors into (to_run, from_cache), skipping disabled ones entirely.
        1. If a metric isn't checked in the request ("disabled"), skip it entirely.
        2. If a metric is checked and is in the cache, use the cached value,
        but update its weight to the current request value.
        3. If a metric is checked and not in the cache, queue it to to_run.
    """
    to_run, from_cache = [], []
    for e in executors:
        get_config = getattr(e, "get_config", None)
        if get_config is not None:
            config = get_config(request)
            if config is None:
                # The metric isn't checked ("Disabled") - skip entirely
                continue  
        else:
            config = None

        key = getattr(e, "metric_key", None)
        if key is not None and key in cached_dict:
            cached_metric = cached_dict[key]
            if config is not None:
                cached_metric = cached_metric.model_copy(update={"weight": config.weight})
            from_cache.append(cached_metric)
        else:
            to_run.append(e)
    return to_run, from_cache


def _executor_will_run(
    e,
    cached_dict: dict[str, RepositoryMetricResult],
    request: AnalysisRequest,
) -> bool:
    """
    Returns false if the metric is not checked in the request ("Disabled"), 
    or if it is cached already
    """
    get_config = getattr(e, "get_config", None)
    if get_config is not None and get_config(request) is None:
        return False  
    return getattr(e, "metric_key", None) not in cached_dict


async def _analyze_repository(
    request: AnalysisRequest,
    repository: RepositoryInput,
    first_phase: list[MetricExecutor],
    subsequent_phases: list[list[PostMetricExecutor]] | None = None,
    tarball_requiring_subcategories: frozenset[tuple[str, str]] | None = None,
) -> RepositoryAnalysisResult:
    cached = await get_cached_metrics(repository.repo_url)
    cached_dict: dict[str, RepositoryMetricResult] = (
        {m.metric_key: m for m in cached} if cached is not None else {}
    )

    to_run_p1, from_cache_p1 = _split_metric_executors_by_cache(first_phase, cached_dict, request)

    # Only start the tarball download if there is at least one enabled+uncached
    # subsequent-phase executor that may need it.
    any_subsequent_to_run = any(
        _executor_will_run(e, cached_dict, request)
        for phase in (subsequent_phases or [])
        for e in phase
    )
    tarball_task: asyncio.Task | None = None
    if any_subsequent_to_run and tarball_requiring_subcategories and any(
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
        *(executor(request, repository) for executor in to_run_p1)
    )
    all_metrics: list[RepositoryMetricResult] = from_cache_p1 + [
        m for m in phase1_results if m is not None
    ]

    # Resolve the tarball download before subsequent phases need it.
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
        to_run_phase, from_cache_phase = _split_metric_executors_by_cache(phase, cached_dict, request)
        phase_results = await asyncio.gather(
            *(executor(request, repository, context + all_metrics) for executor in to_run_phase)
        )
        all_metrics += from_cache_phase + [m for m in phase_results if m is not None]

    # Update cache only when new metrics were computed. Preserve all previously
    # cached metrics (even ones not in the current request) so future requests
    # can still benefit from them.
    newly_computed = [m for m in all_metrics if m.metric_key not in cached_dict]
    if newly_computed or not cached_dict:
        merged = {**cached_dict, **{m.metric_key: m for m in newly_computed}}
        await cache_metrics(repository.repo_url, list(merged.values()))

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