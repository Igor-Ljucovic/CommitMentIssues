import os
import shutil
import subprocess
import tempfile

from app.core.config import settings
from app.analyzers.documentation.github_wiki_total_commits_analyzer.github_wiki_total_commits_fetch import fetch_github_wiki_enabled
from app.rating.metric_rating_calculator import calculate_metric_rating
from app.schemas.analysis_request_schemas import AnalysisSubcategoryConfig, RepositoryInput
from app.schemas.analysis_response_schemas import RepositoryMetricResult
from app.analyzers.documentation.github_wiki_total_commits_analyzer.github_wiki_total_commits_constants import (
    GITHUB_WIKI_TOTAL_COMMITS_METRIC_KEY,
    GITHUB_WIKI_TOTAL_COMMITS_DISPLAY_NAME,
)

async def analyze_github_wiki_total_commits(
    repository: RepositoryInput,
    subcategory_config: AnalysisSubcategoryConfig | None,
) -> RepositoryMetricResult:
    owner, repository_name = repository.get_owner_and_repository_name()

    wiki_enabled_result = await fetch_github_wiki_enabled(
        owner=owner,
        repository_name=repository_name,
    )

    if not wiki_enabled_result["has_wiki_enabled"]:
        github_wiki_total_commits = 0
    else:
        github_wiki_total_commits = _get_github_wiki_total_commits(
            owner=owner,
            repository_name=repository_name,
        )

    rating, requirement_failed = calculate_metric_rating(
        value=github_wiki_total_commits,
        subcategory_config=subcategory_config,
    )

    return RepositoryMetricResult(
        metric_key=GITHUB_WIKI_TOTAL_COMMITS_METRIC_KEY,
        display_name=GITHUB_WIKI_TOTAL_COMMITS_DISPLAY_NAME,
        value=github_wiki_total_commits,
        rating=rating,
        requirement_failed=requirement_failed,
        status="success",
        message="GitHub wiki total commits fetched successfully.",
    )


def _get_github_wiki_total_commits(
    owner: str,
    repository_name: str,
) -> int:
    wiki_url = f"https://{settings.GITHUB_TOKEN}@github.com/{owner}/{repository_name}.wiki.git"

    if not shutil.which("git"):
        raise RuntimeError("Git is not installed on the server.")

    with tempfile.TemporaryDirectory(prefix="github-wiki-") as temp_dir:
        repo_dir = os.path.join(temp_dir, "wiki.git")

        clone_command = [
            "git",
            "clone",
            "--quiet",
            "--bare",
            wiki_url,
            repo_dir,
        ]

        clone_result = subprocess.run(
            clone_command,
            capture_output=True,
            text=True,
            env={
                **os.environ,
                "GIT_TERMINAL_PROMPT": "0",
            },
            check=False,
        )

        if clone_result.returncode != 0:
            stderr_text = (clone_result.stderr or "").strip().lower()

            if (
                "repository not found" in stderr_text
                or "not found" in stderr_text
                or "authentication failed" in stderr_text
                or "could not read username" in stderr_text
            ):
                return 0

            raise RuntimeError(
                f"Could not clone GitHub wiki repository: {clone_result.stderr.strip()}"
            )

        count_command = [
            "git",
            f"--git-dir={repo_dir}",
            "rev-list",
            "--count",
            "HEAD",
        ]

        count_result = subprocess.run(
            count_command,
            capture_output=True,
            text=True,
            check=False,
        )

        if count_result.returncode != 0:
            stderr_text = (count_result.stderr or "").strip().lower()

            if "unknown revision" in stderr_text or "bad revision" in stderr_text:
                return 0

            raise RuntimeError(
                f"Could not count GitHub wiki commits: {count_result.stderr.strip()}"
            )

        output = (count_result.stdout or "").strip()

        try:
            return int(output)
        except ValueError as exc:
            raise RuntimeError("Git returned an invalid wiki commit count.") from exc