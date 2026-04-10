from collections.abc import Awaitable, Callable

from app.analyzers.collaboration.pull_request_acceptance_rate_analyzer.pull_request_acceptance_rate_metric import (
    get_pull_request_acceptance_rate_metric,
)
from app.analyzers.documentation.github_wiki_total_commits_analyzer.github_wiki_total_commits_metric import (
    get_github_wiki_total_commits_metric,
)
from app.analyzers.general.first_commit_date_analyzer.first_commit_date_metric import (
    get_first_commit_date_metric,
)
from app.analyzers.general.total_commits_analyzer.total_commits_metric import (
    get_total_commits_metric,
)
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


async def analyze_repositories_github_graphql(request: AnalysisRequest) -> AnalysisResponse:
    warnings: list[str] = []

    repositories = request.get_repository_inputs()

    if not repositories:
        warnings.append(
            "No repositories were provided in the analysis request, so GitHub-based metrics could not be calculated."
        )
        return AnalysisResponse(files=[], warnings=warnings)

    file_map: dict[int | None, FileAnalysisResult] = {}

    for repository in repositories:
        metrics: list[RepositoryMetricResult] = []

        await _append_metric_if_present(metrics, get_total_commits_metric, request, repository)
        await _append_metric_if_present(metrics, get_first_commit_date_metric, request, repository)
        await _append_metric_if_present(metrics, get_pull_request_acceptance_rate_metric, request, repository)
        await _append_metric_if_present(metrics, get_github_wiki_total_commits_metric, request, repository)

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