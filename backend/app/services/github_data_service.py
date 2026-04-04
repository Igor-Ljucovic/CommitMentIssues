import os
import shutil
import subprocess
import tempfile

from app.clients.github_graphql_client import (
    fetch_first_commit_date,
    fetch_github_wiki_enabled,
    fetch_pull_request_acceptance_rate,
    fetch_total_commit_count,
)
from app.core.config import settings
from app.schemas.analysis_request_schemas import RepositoryInput


async def get_total_commit_count_for_repository(
    repository: RepositoryInput,
) -> dict:
    owner, repository_name = repository.get_owner_and_repository_name()

    return await fetch_total_commit_count(
        owner=owner,
        repository_name=repository_name,
    )


async def get_first_commit_date_for_repository(
    repository: RepositoryInput,
) -> dict:
    owner, repository_name = repository.get_owner_and_repository_name()

    return await fetch_first_commit_date(
        owner=owner,
        repository_name=repository_name,
    )


async def get_pull_request_acceptance_rate_for_repository(
    repository: RepositoryInput,
) -> dict:
    owner, repository_name = repository.get_owner_and_repository_name()

    return await fetch_pull_request_acceptance_rate(
        owner=owner,
        repository_name=repository_name,
    )


async def get_github_wiki_commit_count_for_repository(
    repository: RepositoryInput,
) -> dict:
    owner, repository_name = repository.get_owner_and_repository_name()

    wiki_enabled_result = await fetch_github_wiki_enabled(
        owner=owner,
        repository_name=repository_name,
    )

    if not wiki_enabled_result["has_wiki_enabled"]:
        return {
            "wiki_commit_count": 0,
        }

    wiki_commit_count = _get_wiki_commit_count_with_git(
        owner=owner,
        repository_name=repository_name,
    )

    return {
        "wiki_commit_count": wiki_commit_count,
    }


def _get_wiki_commit_count_with_git(
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