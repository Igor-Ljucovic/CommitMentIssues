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


GITHUB_FIRST_COMMIT_DATE_QUERY = """
query GetFirstCommitDatePage($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    name
    owner {
      login
    }
    defaultBranchRef {
      name
      target {
        ... on Commit {
          history(first: 100, after: $cursor) {
            nodes {
              committedDate
            }
            pageInfo {
              hasNextPage
              endCursor
            }
          }
        }
      }
    }
  }
}
""".strip()


GITHUB_PULL_REQUEST_ACCEPTANCE_RATE_QUERY = """
query GetPullRequestAcceptanceRate($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    name
    owner {
      login
    }
    mergedPullRequests: pullRequests(states: [MERGED], first: 1) {
      totalCount
    }
    closedPullRequests: pullRequests(states: [CLOSED], first: 1) {
      totalCount
    }
  }
}
""".strip()


GITHUB_WIKI_ENABLED_QUERY = """
query GetGitHubWikiEnabled($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    name
    owner {
      login
    }
    hasWikiEnabled
  }
}
""".strip()


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


async def fetch_total_commit_count(
    owner: str,
    repository_name: str,
) -> dict:
    repository = await _execute_github_graphql_query(
        query=GITHUB_TOTAL_COMMIT_COUNT_QUERY,
        variables={
            "owner": owner,
            "name": repository_name,
        },
    )

    default_branch_ref = repository.get("defaultBranchRef")
    if default_branch_ref is None:
        raise ValueError("Repository does not have a default branch.")

    history = default_branch_ref.get("target", {}).get("history", {})
    total_commit_count = history.get("totalCount")

    if total_commit_count is None:
        raise RuntimeError("Could not read commit history for the default branch.")

    return {
        "owner": repository["owner"]["login"],
        "repository_name": repository["name"],
        "branch_name": default_branch_ref["name"],
        "total_commit_count": total_commit_count,
    }


async def fetch_first_commit_date(
    owner: str,
    repository_name: str,
) -> dict:
    cursor = None
    last_commit_date = None
    branch_name = None
    repository_owner = None
    resolved_repository_name = None

    while True:
        repository = await _execute_github_graphql_query(
            query=GITHUB_FIRST_COMMIT_DATE_QUERY,
            variables={
                "owner": owner,
                "name": repository_name,
                "cursor": cursor,
            },
        )

        default_branch_ref = repository.get("defaultBranchRef")
        if default_branch_ref is None:
            raise ValueError("Repository does not have a default branch.")

        branch_name = default_branch_ref["name"]
        repository_owner = repository["owner"]["login"]
        resolved_repository_name = repository["name"]

        history = default_branch_ref.get("target", {}).get("history", {})
        nodes = history.get("nodes", [])

        if not nodes:
            raise RuntimeError("Could not read commit history for the default branch.")

        last_commit_date = nodes[-1].get("committedDate")
        if last_commit_date is None:
            raise RuntimeError("Could not read committedDate for the first commit.")

        page_info = history.get("pageInfo", {})
        has_next_page = page_info.get("hasNextPage")
        end_cursor = page_info.get("endCursor")

        if not has_next_page:
            break

        cursor = end_cursor

        if cursor is None:
            raise RuntimeError("GitHub pagination did not return an end cursor.")

    return {
        "owner": repository_owner,
        "repository_name": resolved_repository_name,
        "branch_name": branch_name,
        "first_commit_date": last_commit_date[:10],
    }


async def fetch_pull_request_acceptance_rate(
    owner: str,
    repository_name: str,
) -> dict:
    repository = await _execute_github_graphql_query(
        query=GITHUB_PULL_REQUEST_ACCEPTANCE_RATE_QUERY,
        variables={
            "owner": owner,
            "name": repository_name,
        },
    )

    merged_pull_request_count = (
        repository.get("mergedPullRequests", {}).get("totalCount")
    )
    closed_unmerged_pull_request_count = (
        repository.get("closedPullRequests", {}).get("totalCount")
    )

    if merged_pull_request_count is None or closed_unmerged_pull_request_count is None:
        raise RuntimeError("Could not read pull request counts from GitHub.")

    resolved_pull_request_count = (
        merged_pull_request_count + closed_unmerged_pull_request_count
    )

    if resolved_pull_request_count == 0:
        pull_request_acceptance_rate = 0.0
    else:
        pull_request_acceptance_rate = round(
            (merged_pull_request_count / resolved_pull_request_count) * 100,
            2,
        )

    return {
        "owner": repository["owner"]["login"],
        "repository_name": repository["name"],
        "merged_pull_request_count": merged_pull_request_count,
        "closed_unmerged_pull_request_count": closed_unmerged_pull_request_count,
        "resolved_pull_request_count": resolved_pull_request_count,
        "pull_request_acceptance_rate": pull_request_acceptance_rate,
    }


async def fetch_github_wiki_enabled(
    owner: str,
    repository_name: str,
) -> dict:
    repository = await _execute_github_graphql_query(
        query=GITHUB_WIKI_ENABLED_QUERY,
        variables={
            "owner": owner,
            "name": repository_name,
        },
    )

    has_wiki_enabled = repository.get("hasWikiEnabled")

    if has_wiki_enabled is None:
        raise RuntimeError("Could not read GitHub wiki enabled status.")

    return {
        "has_wiki_enabled": has_wiki_enabled,
    }