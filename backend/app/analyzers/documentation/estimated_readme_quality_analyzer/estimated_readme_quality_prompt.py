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

Score the README using this EXACT rubric (you can also rate partial points, e.g. 0.35/1.0):

1. Grammar & Clarity (0.0–15.0)
2. Formatting & Structure (0.0–15.0)
3. Technologies Listed (0.0–20.0)
4. Technology Explanation (0.0–10.0)
5. Setup Instructions (0.0–10.0)
6. Usage Examples (0.0–10.0)
7. Project Description (0.0–10.0)
8. Content Depth/Length (0.0–10.0)

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