from typing import Any

from app.clients.openai.openai_rest_client import execute_openai_request


async def analyze_metric_with_openai(
    prompt: str,
) -> dict[str, Any]:
    response = await execute_openai_request(
        endpoint="/chat/completions",
        json_body={
            "model": "gpt-4.1-mini",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a repository analysis assistant. "
                        "Always return ONLY valid JSON matching the requested schema."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "repository_metric_analysis",
                    "schema": {
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
                        "required": [
                            "rating",
                            "explanation",
                        ],
                        "additionalProperties": False,
                    },
                },
            },
        },
    )

    content = response["choices"][0]["message"]["content"]

    import json
    return json.loads(content)