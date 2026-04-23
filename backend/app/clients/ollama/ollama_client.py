from typing import Any
import httpx


async def execute_ollama_chat(
    *,
    base_url: str,
    model: str,
    messages: list[dict[str, str]],
    format_schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    json_body: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0,
            "num_ctx": 4096,
        },
    }

    if format_schema is not None:
        json_body["format"] = format_schema

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{base_url}/api/chat",
            json=json_body,
        )

        response.raise_for_status()
        return response.json()