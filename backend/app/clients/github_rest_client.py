from typing import Any
from urllib.parse import parse_qs, urlparse

import httpx

from app.core.config import settings


async def execute_github_rest_request(
    method: str,
    endpoint: str,
    *,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
    extra_headers: dict[str, str] | None = None,
) -> Any:
    response = await execute_github_rest_request_raw(
        method=method,
        endpoint=endpoint,
        params=params,
        json_body=json_body,
        extra_headers=extra_headers,
    )

    if response.status_code == 204:
        return None

    content_type = response.headers.get("Content-Type", "").lower()
    if "application/json" in content_type:
        return response.json()

    return response.text


async def execute_github_rest_request_raw(
    method: str,
    endpoint: str,
    *,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
    extra_headers: dict[str, str] | None = None,
) -> httpx.Response:
    if not settings.GITHUB_TOKEN:
        raise PermissionError("GitHub token is not configured on the server.")

    normalized_endpoint = endpoint.strip()
    if not normalized_endpoint:
        raise ValueError("GitHub REST endpoint must not be empty.")

    if not normalized_endpoint.startswith("/"):
        normalized_endpoint = f"/{normalized_endpoint}"

    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if extra_headers:
        headers.update(extra_headers)

    timeout = httpx.Timeout(settings.GITHUB_REQUEST_TIMEOUT_SECONDS)

    async with httpx.AsyncClient(
        base_url=settings.GITHUB_REST_API_BASE_URL,
        timeout=timeout,
    ) as client:
        response = await client.request(
            method=method.upper(),
            url=normalized_endpoint,
            params=params,
            json=json_body,
            headers=headers,
        )

    _raise_for_github_rest_error(response)
    return response


async def execute_github_rest_get(
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


async def fetch_github_rest_last_page_number(
    endpoint: str,
    *,
    params: dict[str, Any] | None = None,
    extra_headers: dict[str, str] | None = None,
) -> int:
    response = await execute_github_rest_request_raw(
        method="GET",
        endpoint=endpoint,
        params=params,
        extra_headers=extra_headers,
    )

    return extract_last_page_number_from_response(response)


def extract_last_page_number_from_response(response: httpx.Response) -> int:
    last_link = response.links.get("last", {}).get("url")

    if last_link is not None:
        parsed_url = urlparse(last_link)
        parsed_query = parse_qs(parsed_url.query)
        page_values = parsed_query.get("page")

        if page_values:
            try:
                return int(page_values[0])
            except ValueError as exc:
                raise RuntimeError(
                    "GitHub pagination returned an invalid last page number."
                ) from exc

    response_data = response.json()
    if isinstance(response_data, list):
        return len(response_data)

    raise RuntimeError(
        "Could not determine total item count from GitHub REST response."
    )


def _raise_for_github_rest_error(response: httpx.Response) -> None:
    if response.status_code < 400:
        return

    error_message = _extract_github_rest_error_message(response)

    if response.status_code == 401:
        raise PermissionError("GitHub authentication failed. Check the GitHub token.")

    if response.status_code == 403:
        lowered_message = error_message.lower()
        if "rate limit" in lowered_message:
            raise RuntimeError(
                f"GitHub REST rate limit exceeded: {error_message}"
            )

        raise PermissionError(
            f"GitHub REST access forbidden: {error_message}"
        )

    if response.status_code == 404:
        raise ValueError("Resource was not found or is not accessible.")

    if response.status_code == 422:
        raise ValueError(f"GitHub REST validation failed: {error_message}")

    raise RuntimeError(
        f"GitHub REST request failed with status code "
        f"{response.status_code}: {error_message}"
    )


def _extract_github_rest_error_message(response: httpx.Response) -> str:
    try:
        data = response.json()
    except Exception:
        text = response.text.strip()
        return text or "Unknown GitHub REST error."

    if isinstance(data, dict):
        message = data.get("message")
        if isinstance(message, str) and message.strip():
            return message.strip()

    return "Unknown GitHub REST error."