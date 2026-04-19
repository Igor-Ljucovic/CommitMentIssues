from app.analyzers.documentation.estimated_readme_quality_analyzer.estimated_readme_quality_constants import (
    README_CONTENT,
    README_HEAD_SIZE,
    README_TAIL_SIZE,
)


def build_estimated_readme_quality_prompt(
    readme_data: dict,
) -> str:
    readme_content = readme_data.get(README_CONTENT, "")

    truncated_readme_content = _truncate_text(
        text=readme_content,
        head_size=README_HEAD_SIZE,
        tail_size=README_TAIL_SIZE,
    )

    template = """
You are analyzing the quality of a GitHub repository README.

Score the README using this EXACT rubric (you can also rate partial points, e.g. 0.35/1.0):

1. Grammar & Clarity (0–15)
2. Formatting & Structure (0–15)
3. Technologies Listed (0–20)
4. Technology Explanation (0–10)
5. Setup Instructions (0–10)
6. Usage Examples (0–10)
7. Project Description (0–10)
8. Content Depth/Length (0–10)

Rules:
- Total score MUST be the sum (0–100)
- Be conservative when scoring
- The README content may be truncated.
- If it is truncated, evaluate only the visible content.
- Do not assume missing sections are absent from the full README unless the visible content strongly suggests they are missing.
- Be slightly conservative when scoring truncated content.

README content:
\"\"\"
{truncated_readme_content}
\"\"\"

Return ONLY valid JSON in this format:

{{
  "rating": 67.0,
  "explanation": "The formatting is good but the usage examples are missing..."
}}
""".strip()

    return template.format(
        truncated_readme_content=truncated_readme_content,
    )


def _truncate_text(text: str, head_size: int, tail_size: int) -> str:
    if len(text) <= head_size + tail_size:
        return text

    head = text[:head_size]
    tail = text[-tail_size:]

    return head.rstrip() + "\n\n...[TRUNCATED]...\n\n" + tail.lstrip()