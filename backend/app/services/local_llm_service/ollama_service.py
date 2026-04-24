from typing import Any

from app.clients.ollama_client import execute_ollama_request


async def rate_metric_with_ollama(
    *,
    base_url: str,
    model: str,
    messages: list[dict[str, str]],
    num_ctx: int = 4096,
) -> dict[str, Any]:
    json_body = {
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
                "rating": {"type": "number", "minimum": 0, "maximum": 10},
                "explanation": {"type": "string", "maxLength": 250},
            },
            "required": ["rating", "explanation"],
            "additionalProperties": False,
        },
    }

    return await execute_ollama_request(
        base_url=base_url,
        json_body=json_body,
    )