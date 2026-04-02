import httpx

from app.core.config import settings


GITHUB_TOTAL_COMMIT_COUNT_QUERY = """
query GetRepositoryCommitCount($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    name
    owner {
      login
    }
    defaultBranchRef {
      name
      target {
        ... on Commit {
          history(first: 1) {
            totalCount
          }
        }
      }
    }
  }
}
""".strip()


async def fetch_total_commit_count(
    owner: str,
    repository_name: str,
) -> dict:
    if not settings.GITHUB_TOKEN:
        raise PermissionError("GitHub token is not configured on the server.")

    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "query": GITHUB_TOTAL_COMMIT_COUNT_QUERY,
        "variables": {
            "owner": owner,
            "name": repository_name,
        },
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
        first_error_message = data["errors"][0].get("message", "Unknown GitHub GraphQL error.")
        raise RuntimeError(f"GitHub GraphQL error: {first_error_message}")

    repository = data.get("data", {}).get("repository")
    if repository is None:
        raise ValueError("Repository was not found or is not accessible.")

    default_branch_ref = repository.get("defaultBranchRef")
    if default_branch_ref is None:
        raise ValueError("Repository does not have a default branch.")

    history = default_branch_ref.get("target", {}).get("history", {})
    total_commit_count = history.get("totalCount")

    if total_commit_count is None:
        raise RuntimeError("Could not read commit history for the default branch.")

    # owner, repository_name and branch_name are not needed for the end user,
    # but they are required for the GitHub GraphQL API 
    # (we remove them later in analysis_response_schemas and analysis_orchestrator_service)
    return {
        "owner": repository["owner"]["login"],
        "repository_name": repository["name"],
        "branch_name": default_branch_ref["name"],
        "total_commit_count": total_commit_count,
    }