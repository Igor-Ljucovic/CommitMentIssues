from typing import Any
import httpx

from app.core.config import settings


async def execute_openai_request(
    endpoint: str,
    *,
    json_body: dict[str, Any],
) -> dict:
    response = await execute_openai_request_raw(
        endpoint=endpoint,
        json_body=json_body,
    )

    return response.json()


async def execute_openai_request_raw(
    endpoint: str,
    *,
    json_body: dict[str, Any],
) -> httpx.Response:
    if not settings.OPENAI_API_KEY:
        raise PermissionError("OpenAI API key is not configured on the server.")

    normalized_endpoint = endpoint.strip()
    if not normalized_endpoint:
        raise ValueError("OpenAI endpoint must not be empty.")

    if not normalized_endpoint.startswith("/"):
        normalized_endpoint = f"/{normalized_endpoint}"

    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    timeout = httpx.Timeout(settings.OPENAI_REQUEST_TIMEOUT_SECONDS)

    async with httpx.AsyncClient(
        base_url=settings.OPENAI_API_BASE_URL,
        timeout=timeout,
    ) as client:
        response = await client.post(
            url=normalized_endpoint,
            json=json_body,
            headers=headers,
        )

    _raise_for_openai_error(response)

    return response


def _raise_for_openai_error(response: httpx.Response) -> None:
    if response.status_code < 400:
        return

    error_message = _extract_openai_error_message(response)

    if response.status_code == 401:
        raise PermissionError(
            "OpenAI authentication failed. Check the API key."
        )

    if response.status_code == 429:
        raise RuntimeError(
            f"OpenAI rate limit exceeded: {error_message}"
        )

    raise RuntimeError(
        f"OpenAI request failed with status code "
        f"{response.status_code}: {error_message}"
    )


def _extract_openai_error_message(response: httpx.Response) -> str:
    try:
        data = response.json()
    except Exception:
        text = response.text.strip()
        return text or "Unknown OpenAI API error."

    error = data.get("error")
    if isinstance(error, dict):
        message = error.get("message")
        if isinstance(message, str) and message.strip():
            return message.strip()

    return "Unknown OpenAI API error."