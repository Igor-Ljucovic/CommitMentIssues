import base64
from typing import Any

from app.analyzers.documentation.estimated_readme_quality_analyzer.estimated_readme_quality_constants import (
    ESTIMATED_README_QUALITY_METRIC_KEY,
    README_CONTENT,
)
from app.clients.github.github_rest_client import execute_github_rest_get


async def fetch_estimated_readme_quality_input(
    owner: str,
    repository_name: str,
) -> dict[str, Any]:
    readme_data = await execute_github_rest_get(
        f"/repos/{owner}/{repository_name}/readme"
    )

    if not isinstance(readme_data, dict):
        raise RuntimeError("GitHub README response was not in the expected format.")

    encoded_content = readme_data.get("content")
    encoding = readme_data.get("encoding")

    if not isinstance(encoded_content, str) or not encoded_content.strip():
        raise RuntimeError("GitHub README content is missing.")

    if encoding != "base64":
        raise RuntimeError(
            f'Unsupported GitHub README encoding: "{encoding}".'
        )

    try:
        decoded_bytes = base64.b64decode(encoded_content, validate=False)
        readme_content = decoded_bytes.decode("utf-8", errors="replace")
    except Exception as exc:
        raise RuntimeError("Could not decode GitHub README content.") from exc

    return {
        "owner": owner,
        "repository_name": repository_name,
        README_CONTENT: readme_content,
        ESTIMATED_README_QUALITY_METRIC_KEY: None,
    }