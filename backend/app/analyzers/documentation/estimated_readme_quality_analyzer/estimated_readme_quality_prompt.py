from app.analyzers.documentation.estimated_readme_quality_analyzer.estimated_readme_quality_constants import (
    README_CONTENT,
)
from app.analyzers.common.prompt_utils import prompt_character_limit


def build_estimated_readme_quality_prompt(
    readme_data: dict,
    num_ctx: int,
) -> str:
    template = """
You are analyzing the quality of a GitHub repository README.

Score the README using this EXACT rubric (you can also rate partial points, e.g. 6.35/10.0):

1. Grammar & Clarity (0.0–10.0)
2. Formatting & Structure (0.0–15.0)
3. Tech Stack (0.0–25.0)
4. Setup Instructions (0.0–10.0)
5. Project purpose (who would use it and how) (0.0–20.0)
6. Project Description (0.0–20.0)

Rules:
- Total score MUST be the sum (0.0–100.0)
- Be conservative when scoring
- The README content may be truncated.
- If it is truncated, evaluate only the visible content.
- Do not assume missing sections are absent from the full README 
unless the visible content strongly suggests they are missing.
- Be slightly conservative when scoring truncated content.

Return ONLY valid JSON in this format:

{{
  "rating": float (number, for example 78.5),
  "explanation": string (for example "The formatting is good, 
  but the usage examples are missing...")
}}

README content:
\"\"\"
{readme_content}
\"\"\"
""".strip()

    return template.format(
        readme_content=readme_data.get(README_CONTENT, ""),
    )[:prompt_character_limit(num_ctx=num_ctx)]