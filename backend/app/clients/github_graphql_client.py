import httpx

from app.core.config import settings


async def _execute_github_graphql_query(query: str, variables: dict) -> dict:
    if not settings.GITHUB_TOKEN:
        raise PermissionError("GitHub token is not configured on the server.")

    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "query": query,
        "variables": variables,
    }

    timeout = httpx.Timeout(settings.GITHUB_REQUEST_TIMEOUT_SECONDS)

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            settings.GITHUB_GRAPHQL_URL,
            json=payload,
            headers=headers,
        )

    if response.status_code == 401:
        raise PermissionError("GitHub authentication failed. Check the GitHub token.")

    if response.status_code >= 400:
        raise RuntimeError(
            f"GitHub GraphQL request failed with status code {response.status_code}."
        )

    data = response.json()

    if "errors" in data and data["errors"]:
        first_error_message = data["errors"][0].get(
            "message",
            "Unknown GitHub GraphQL error.",
        )
        raise RuntimeError(f"GitHub GraphQL error: {first_error_message}")

    repository = data.get("data", {}).get("repository")
    if repository is None:
        raise ValueError("Repository was not found or is not accessible.")

    return repository