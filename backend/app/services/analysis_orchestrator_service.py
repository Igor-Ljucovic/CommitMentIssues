from app.schemas.analysis_request_schemas import AnalysisRequest, AnalysisCategoryConfig, RepositoryInput
from app.schemas.analysis_response_schemas import (
    AnalysisResponse,
    FileAnalysisResult,
    RepositoryAnalysisResult,
    RepositoryMetricResult,
)
from app.services.github_data_service import get_total_commit_count_for_repository


def _is_metric_requested(
    category_configs: dict[str, AnalysisCategoryConfig],
    category_name: str,
    subcategory_name: str,
) -> bool:
    category = category_configs.get(category_name)
    if category is None:
        return False

    return subcategory_name in category.subcategories


async def _build_total_commits_metric(repository: RepositoryInput) -> RepositoryMetricResult:
    result = await get_total_commit_count_for_repository(repository)

    return RepositoryMetricResult(
        metric_key="total_commits",
        display_name="Total Commits",
        value=result["total_commit_count"],
        status="success",
        message=f'Commit count fetched from branch "{result["branch_name"]}".',
    )


async def analyze_repositories(request: AnalysisRequest) -> AnalysisResponse:
    category_configs = request.get_category_configs()
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

        if _is_metric_requested(category_configs, "General", "Total Commits"):
            try:
                total_commits_metric = await _build_total_commits_metric(repository)
                metrics.append(total_commits_metric)
            except Exception as exc:
                metrics.append(
                    RepositoryMetricResult(
                        metric_key="total_commits",
                        display_name="Total Commits",
                        value=None,
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