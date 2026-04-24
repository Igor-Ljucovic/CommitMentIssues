import json
from typing import Any, Callable, Awaitable

from app.core.config import settings


async def local_llm_analyze(
    local_llm: Callable[..., Awaitable[dict[str, Any]]],
    prompt: str,
    llm_model: str,
    num_ctx: int = 4096,
) -> dict[str, Any]:
    response = await local_llm(
        base_url=settings.LOCAL_LLM_BASE_URL,
        model=llm_model,
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
                "content": prompt,
            },
        ],
        num_ctx=num_ctx,
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