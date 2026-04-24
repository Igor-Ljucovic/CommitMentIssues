from typing import Any

from app.core.config import settings

from app.clients.github_rest_client import (
    execute_github_rest_request,
    github_rest_get_bytes,
)


async def fetch_github_rest_resource(
    endpoint: str,
    *,
    params: dict[str, Any] | None = None,
    extra_headers: dict[str, str] | None = None,
) -> Any:
    return await execute_github_rest_request(
        method="GET",
        endpoint=endpoint,
        params=params,
        extra_headers=extra_headers,
    )


async def fetch_github_rest_bytes(path: str) -> bytes:
    url = f"https://api.github.com{path}" if path.startswith("/") else path
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2026-03-10",
    }
    return await github_rest_get_bytes(url, headers)