from app.analyzers.common.prompt_utils import prompt_character_limit


def build_estimated_github_wiki_quality_prompt(
    wiki_data: str,
    num_ctx: int,
) -> str:
    template = """
You are analyzing the quality of a GitHub repository Wiki.

Score the Wiki using this EXACT rubric (you can also rate partial points, e.g. 6.35/10.0):

1. Grammar & Clarity (0.0–10.0)
2. Formatting & Structure (0.0–15.0)
3. Technologies Listed (0.0–10.0)
4. Technology Explanation (0.0–15.0)
5. Architecture Design Rationale (explanations why they solved something a certain way) (0.0-15.0)
6. Setup Instructions (0.0–10.0)
7. Usage Examples (0.0–10.0)
8. Project Documentation Coverage (0.0–15.0)

Rules:
- Total score MUST be the sum (0.0–100.0)
- Be conservative when scoring
- The Wiki content may be truncated.
- If it is truncated, evaluate only the visible content.
- Do not assume missing sections are absent from the full Wiki 
unless the visible content strongly suggests they are missing.
- Be slightly conservative when scoring truncated content.

Return ONLY valid JSON in this format:

{{
  "rating": float (number, for example 78.5),
  "explanation": string (for example "The formatting is good, 
  but the technologies used are missing...")
}}

Wiki content:
\"\"\"
{github_wiki_content}
\"\"\"
""".strip()

    return template.format(
        github_wiki_content=wiki_data,
    )[:prompt_character_limit(num_ctx=num_ctx)]