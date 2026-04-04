from app.analyzers.collaboration.pull_request_acceptance_rate_analyzer import (
    analyze_pull_request_acceptance_rate,
)
from app.analyzers.documentation.github_wiki_total_commits_analyzer import (
    analyze_github_wiki_commit_count,
)
from app.analyzers.general.first_commit_date_analyzer import (
    analyze_first_commit_date,
)
from app.analyzers.general.total_commits_analyzer import (
    analyze_total_commits,
)
from app.schemas.analysis_request_schemas import AnalysisRequest
from app.schemas.analysis_response_schemas import (
    AnalysisResponse,
    FileAnalysisResult,
    RepositoryAnalysisResult,
    RepositoryMetricResult,
)


async def analyze_repositories(request: AnalysisRequest) -> AnalysisResponse:
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

        total_commits_config = request.get_subcategory_config("General", "Total Commits")
        if total_commits_config is not None:
            try:
                total_commits_metric = await analyze_total_commits(
                    repository=repository,
                    subcategory_config=total_commits_config,
                )
                metrics.append(total_commits_metric)
            except Exception as exc:
                metrics.append(
                    RepositoryMetricResult(
                        metric_key="total_commits",
                        display_name="Total Commits",
                        value=None,
                        rating=None,
                        requirement_failed=None,
                        status="failed",
                        message=str(exc),
                    )
                )

        first_commit_date_config = request.get_subcategory_config(
            "General",
            "First Commit Date",
        )
        if first_commit_date_config is not None:
            try:
                first_commit_date_metric = await analyze_first_commit_date(
                    repository=repository,
                    subcategory_config=first_commit_date_config,
                )
                metrics.append(first_commit_date_metric)
            except Exception as exc:
                metrics.append(
                    RepositoryMetricResult(
                        metric_key="first_commit_date",
                        display_name="First Commit Date",
                        value=None,
                        rating=None,
                        requirement_failed=None,
                        status="failed",
                        message=str(exc),
                    )
                )

        pull_request_acceptance_rate_config = request.get_subcategory_config(
            "Collaboration",
            "Pull Request Acceptance Rate",
        )
        if pull_request_acceptance_rate_config is not None:
            try:
                pull_request_acceptance_rate_metric = await analyze_pull_request_acceptance_rate(
                    repository=repository,
                    subcategory_config=pull_request_acceptance_rate_config,
                )
                metrics.append(pull_request_acceptance_rate_metric)
            except Exception as exc:
                metrics.append(
                    RepositoryMetricResult(
                        metric_key="pull_request_acceptance_rate",
                        display_name="Pull Request Acceptance Rate",
                        value=None,
                        rating=None,
                        requirement_failed=None,
                        status="failed",
                        message=str(exc),
                    )
                )

        github_wiki_total_commits_config = request.get_subcategory_config(
            "Documentation",
            "GitHub Wiki Total Commits",
        )
        if github_wiki_total_commits_config is not None:
            try:
                github_wiki_total_commits_metric = await analyze_github_wiki_commit_count(
                    repository=repository,
                    subcategory_config=github_wiki_total_commits_config,
                )
                metrics.append(github_wiki_total_commits_metric)
            except Exception as exc:
                metrics.append(
                    RepositoryMetricResult(
                        metric_key="github_wiki_total_commits",
                        display_name="GitHub Wiki Total Commits",
                        value=None,
                        rating=None,
                        requirement_failed=None,
                        status="failed",
                        message=str(exc),
                    )
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