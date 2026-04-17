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
from app.schemas.analysis_request_schemas import AnalysisRequest
from app.schemas.analysis_response_schemas import AnalysisResponse
from app.services.api.analysis_orchestrator_service.utils.client_api_helper_service import run_repository_analysis


async def analyze_repositories_github_graphql(
    request: AnalysisRequest,
) -> AnalysisResponse:
    return await run_repository_analysis(
        request=request,
        metric_executors=[
            get_total_commits_metric,
            get_first_commit_date_metric,
            get_pull_request_acceptance_rate_metric,
            get_github_wiki_total_commits_metric,
        ],
        no_repositories_warning=(
            "No repositories were provided in the analysis request, "
            "so GitHub-based metrics could not be calculated."
        ),
    )