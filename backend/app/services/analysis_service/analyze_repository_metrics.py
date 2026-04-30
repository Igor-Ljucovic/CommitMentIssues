from app.services.analysis_service.analyze_repository import analyze_repository

from app.schemas.analysis_request_schemas import AnalysisRequest
from app.schemas.analysis_response_schemas import AnalysisResponse

from app.analyzers.collaboration.pull_request_acceptance_rate_analyzer.pull_request_acceptance_rate_metric import get_pull_request_acceptance_rate_metric
from app.analyzers.general.average_commits_per_month_analyzer.average_commits_per_month_metric import get_average_commits_per_month_metric
from app.analyzers.general.first_commit_date_analyzer.first_commit_date_metric import get_first_commit_date_metric
from app.analyzers.general.last_commit_date_analyzer.last_commit_date_metric import get_last_commit_date_metric
from app.analyzers.general.total_commits_analyzer.total_commits_metric import get_total_commits_metric
from app.analyzers.general.total_forks_analyzer.total_forks_metric import get_total_forks_metric
from app.analyzers.general.total_files_analyzer.total_files_metric import get_total_files_metric
from app.analyzers.general.total_lines_of_code_analyzer.total_lines_of_code_metric import get_total_lines_of_code_metric
from app.analyzers.general.total_files_filtered_analyzer.total_files_filtered_metric import get_total_files_filtered_metric
from app.analyzers.documentation.estimated_readme_quality_analyzer.estimated_readme_quality_metric import get_github_readme_quality_metric
from app.analyzers.documentation.estimated_github_wiki_quality_analyzer.estimated_github_wiki_quality_metric import get_github_wiki_quality_metric
from app.analyzers.code_and_repository_quality.estimated_commit_naming_quality_analyzer.ollama_estimated_commit_naming_quality_metric import get_ollama_estimated_commit_naming_quality_metric
from app.analyzers.general.stars_analyzer.stars_metric import get_stars_metric
from app.analyzers.general.languages_used_analyzer.languages_used_metric import get_languages_used_metric
from app.analyzers.general.languages_used_filtered_analyzer.languages_used_filtered_metric import get_languages_used_filtered_metric
from app.analyzers.general.total_branches_analyzer.total_branches_metric import get_total_branches_metric
from app.analyzers.general.average_commit_size_analyzer.average_commit_size_metric import get_average_commit_size_metric
from app.analyzers.general.median_commit_size_analyzer.median_commit_size_metric import get_median_commit_size_metric
from app.analyzers.general.average_commit_size_filtered_analyzer.average_commit_size_filtered_metric import get_average_commit_size_filtered_metric
from app.analyzers.general.median_commit_size_filtered_analyzer.median_commit_size_filtered_metric import get_median_commit_size_filtered_metric


async def analyze_repository_metrics(
    request: AnalysisRequest,
) -> AnalysisResponse:
    return await analyze_repository(
        request=request,
        metric_executors=[
            get_total_branches_metric,
            get_total_commits_metric,
            get_average_commit_size_metric,
            get_first_commit_date_metric,
            get_last_commit_date_metric,
            get_pull_request_acceptance_rate_metric,
            get_total_forks_metric,
            get_stars_metric,
            get_languages_used_filtered_metric,
            get_total_lines_of_code_metric,
            get_total_files_filtered_metric,
            get_github_readme_quality_metric,
            get_github_wiki_quality_metric,
            get_ollama_estimated_commit_naming_quality_metric,
        ],
        subsequent_phases=[
            [
                get_average_commit_size_filtered_metric,
                get_average_commits_per_month_metric,
                get_total_files_metric,
                get_languages_used_metric,
            ],
            [
                get_median_commit_size_metric,
            ],
            [
                get_median_commit_size_filtered_metric
            ],
        ],
        no_repositories_warning=(
            "No repositories were provided in the analysis request, "
            "so metrics could not be calculated."
        ),
    )