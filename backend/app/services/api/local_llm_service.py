import json
from typing import Any

from app.clients.ollama.ollama_client import execute_ollama_chat
from app.core.config import settings


OLLAMA_METRIC_ANALYSIS_SCHEMA: dict[str, Any] = {
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


async def analyze_metric_with_local_llm(
    prompt: str,
) -> dict[str, Any]:
    response = await execute_ollama_chat(
        base_url=settings.LOCAL_LLM_BASE_URL,
        model=settings.LOCAL_LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a repository analysis assistant. "
                    "Return only JSON matching the provided schema."
                ),
            },
            {
                "role": "user",
                "content": prompt[:5000],
            },
        ],
        format_schema=OLLAMA_METRIC_ANALYSIS_SCHEMA,
    )

    content = response.get("message", {}).get("content", "").strip()

    if not content:
        raise RuntimeError("Local LLM returned an empty response.")

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Local LLM returned invalid JSON: {content}") from exc

    rating = parsed.get("rating")
    explanation = parsed.get("explanation")

    if not isinstance(rating, float):
        raise RuntimeError("Local LLM did not return a valid numeric rating.")

    if not isinstance(explanation, str) or not explanation.strip():
        raise RuntimeError("Local LLM did not return a valid explanation.")

    return parsed