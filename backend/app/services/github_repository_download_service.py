from pathlib import Path

from app.core.config import GITHUB_REPOSITORIES_DIRECTORY
from app.services.github_rest_service import (
    fetch_github_rest_resource,
    download_github_tarball,
)

async def ensure_repository_tarball(owner: str, repository_name: str) -> Path:
    GITHUB_REPOSITORIES_DIRECTORY.mkdir(parents=True, exist_ok=True)
    tarball_path = GITHUB_REPOSITORIES_DIRECTORY / f"{owner}-{repository_name}.tar.gz"

    if not tarball_path.exists():
        repository_data = await fetch_github_rest_resource(
            f"/repos/{owner}/{repository_name}"
        )
        default_branch = repository_data.get("default_branch")
        if not default_branch:
            raise RuntimeError("Could not determine the repository default branch.")

        await download_github_tarball(
            f"/repos/{owner}/{repository_name}/tarball/{default_branch}",
            tarball_path,
        )

    return tarball_path
