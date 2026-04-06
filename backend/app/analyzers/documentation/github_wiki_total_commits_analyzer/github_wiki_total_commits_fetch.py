import os
import shutil
import subprocess
import tempfile

from app.analyzers.documentation.github_wiki_total_commits_analyzer.github_wiki_total_commits_constants import (
    GITHUB_WIKI_TOTAL_COMMITS_METRIC_KEY,
)
from app.analyzers.documentation.github_wiki_total_commits_analyzer.github_wiki_total_commits_query import (
    GITHUB_WIKI_ENABLED_QUERY,
)
from app.clients.github_graphql_client import execute_github_graphql_query
from app.core.config import settings

# Unlike other fetch methods, GitHub GraphQL does not provide wiki commit counts.
# (GitHub wiki's are considered a seperate repository)
# Because of that, we:
# 1. Check if the wiki is enabled via GraphQL
# 2. Clone the wiki repository using git
# 3. Count commits locally using `git rev-list`
#
# This is why this fetch method is more complex and contains helper functions.

async def fetch_github_wiki_total_commits(
    owner: str,
    repository_name: str,
) -> dict:
    repository = await execute_github_graphql_query(
        query=GITHUB_WIKI_ENABLED_QUERY,
        variables={
            "owner": owner,
            "name": repository_name,
        },
    )

    has_wiki_enabled = repository.get("hasWikiEnabled")
    if has_wiki_enabled is None:
        raise RuntimeError("Could not read GitHub wiki enabled status.")

    if not has_wiki_enabled:
        github_wiki_total_commits = 0
    else:
        github_wiki_total_commits = _count_github_wiki_commits(
            owner=owner,
            repository_name=repository_name,
        )

    return {
        "owner": repository["owner"]["login"],
        "repository_name": repository["name"],
        GITHUB_WIKI_TOTAL_COMMITS_METRIC_KEY: github_wiki_total_commits,
    }


def _count_github_wiki_commits(
    owner: str,
    repository_name: str,
) -> int:
    wiki_url = f"https://{settings.GITHUB_TOKEN}@github.com/{owner}/{repository_name}.wiki.git"

    if not shutil.which("git"):
        raise RuntimeError("Git is not installed on the server.")

    with tempfile.TemporaryDirectory(prefix="github-wiki-") as temp_dir:
        repo_dir = os.path.join(temp_dir, "wiki.git")

        clone_result = subprocess.run(
            [
                "git",
                "clone",
                "--quiet",
                "--bare",
                wiki_url,
                repo_dir,
            ],
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

        count_result = subprocess.run(
            [
                "git",
                f"--git-dir={repo_dir}",
                "rev-list",
                "--count",
                "HEAD",
            ],
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