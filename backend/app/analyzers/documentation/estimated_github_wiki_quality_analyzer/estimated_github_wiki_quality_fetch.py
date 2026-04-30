import os
import shutil
import subprocess
import tempfile

from app.analyzers.documentation.estimated_github_wiki_quality_analyzer.estimated_github_wiki_quality_query import (
    GITHUB_WIKI_ENABLED_QUERY,
)
from app.services.github_graphql_service import fetch_github_graphql_resource


async def fetch_estimated_github_wiki_quality_input(
    owner: str,
    repository_name: str,
) -> str:
    repository = await fetch_github_graphql_resource(
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
        return ""
        

    content = _extract_wiki_content(
        owner=owner,
        repository_name=repository_name,
    )

    return content


def _extract_wiki_content(
    owner: str,
    repository_name: str,
) -> str:
    wiki_url = f"https://github.com/{owner}/{repository_name}.wiki.git"

    if not shutil.which("git"):
        raise RuntimeError("Git is not installed on the server.")

    with tempfile.TemporaryDirectory(prefix="github-wiki-") as temp_dir:
        repo_dir = os.path.join(temp_dir, "wiki")

        clone_result = subprocess.run(
            [
                "git",
                "clone",
                "--quiet",
                "--no-checkout",
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
                return ""

            raise RuntimeError(
                f"Could not clone GitHub wiki repository: {clone_result.stderr.strip()}"
            )

        return _read_markdown_files(repo_dir)


def _read_markdown_files(repo_dir: str) -> str:
    collected_content = []
    total_chars = 0
    max_total_chars = 20000

    # Get list of files in repo
    list_result = subprocess.run(
        ["git", "-C", repo_dir, "ls-tree", "-r", "--name-only", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )

    if list_result.returncode != 0:
        return ""

    files = list_result.stdout.splitlines()

    # Prioritize Home.md (main page on the GitHub Wiki)
    files.sort(key=lambda f: f.lower() != "home.md")

    for file in files:
        if not file.lower().endswith((".md", ".markdown")):
            continue

        show_result = subprocess.run(
            ["git", "-C", repo_dir, "show", f"HEAD:{file}"],
            capture_output=True,
            text=True,
            check=False,
        )

        if show_result.returncode != 0:
            continue

        content = show_result.stdout

        # Makes the AI prompt be in this format:
        # # File: Home.md
        # Welcome to the wiki...
        # # File: Setup.md
        # Installation steps...
        if content.strip():
            chunk = f"\n\n# File: {file}\n{content}"
            collected_content.append(chunk)
            total_chars += len(chunk)

            if total_chars > max_total_chars:
                return "".join(collected_content)

    return "".join(collected_content)