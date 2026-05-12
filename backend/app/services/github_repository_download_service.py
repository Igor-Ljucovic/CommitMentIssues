import asyncio
from pathlib import Path

from app.core.config import GITHUB_REPOSITORIES_DIRECTORY, settings
from app.services.github_rest_service import (
    fetch_github_rest_resource,
    download_github_tarball,
)

_download_semaphore: asyncio.Semaphore | None = None


def _get_download_semaphore() -> asyncio.Semaphore:
    global _download_semaphore
    if _download_semaphore is None:
        _download_semaphore = asyncio.Semaphore(settings.GITHUB_MAX_CONCURRENT_TARBALL_DOWNLOADS)
    return _download_semaphore


async def ensure_repository_tarball(owner: str, repository_name: str) -> Path:
    GITHUB_REPOSITORIES_DIRECTORY.mkdir(parents=True, exist_ok=True)
    tarball_path = GITHUB_REPOSITORIES_DIRECTORY / f"{owner}-{repository_name}.tar.gz"

    if not tarball_path.exists():
        async with _get_download_semaphore():
            if not tarball_path.exists():
                repository_data = await fetch_github_rest_resource(
                    f"/repos/{owner}/{repository_name}"
                )
                repo_size_kb = repository_data.get("size", 0)
                if repo_size_kb > settings.GITHUB_MAX_REPOSITORY_SIZE_KB:
                    raise ValueError(
                        f"Repository size ({repo_size_kb:,} KB) exceeds the "
                        f"{settings.GITHUB_MAX_REPOSITORY_SIZE_KB:,} KB limit."
                    )
                default_branch = repository_data.get("default_branch")
                if not default_branch:
                    raise RuntimeError("Could not determine the repository default branch.")

                await download_github_tarball(
                    f"/repos/{owner}/{repository_name}/tarball/{default_branch}",
                    tarball_path,
                )

    return tarball_path
