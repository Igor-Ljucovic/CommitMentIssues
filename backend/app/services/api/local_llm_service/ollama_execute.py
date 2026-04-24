from typing import Any
import httpx


async def ollama_execute(
    *,
    base_url: str,
    model: str,
    messages: list[dict[str, str]],
    num_ctx: int = 4096,
) -> dict[str, Any]:
    json_body: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0,
            "num_ctx": num_ctx,
        },
        "format": {
            "type": "object",
            "properties": {
                "rating": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 10,
                },
                "explanation": {
                    "type": "string",
                    "maxLength": 250,
                },
            },
            "required": ["rating", "explanation"],
            "additionalProperties": False,
        }
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{base_url}/api/chat",
            json=json_body,
        )

        response.raise_for_status()
        return response.json()