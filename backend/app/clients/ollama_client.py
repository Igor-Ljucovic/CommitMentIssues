from typing import Any
import httpx


async def execute_ollama_request(
    *,
    base_url: str,
    json_body: dict[str, Any],
    timeout_seconds: float = 120.0,
) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=timeout_seconds) as client:
        response = await client.post(
            f"{base_url}/api/chat",
            json=json_body,
        )

        response.raise_for_status()
        return response.json()