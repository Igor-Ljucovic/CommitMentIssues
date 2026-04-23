from app.analyzers.code_and_repository_quality.estimated_commit_naming_quality_analyzer.estimated_commit_naming_quality_constants import (
    ESTIMATED_COMMIT_NAMING_QUALITY_SAMPLE_SEED,
    ESTIMATED_COMMIT_NAMING_QUALITY_SAMPLE_SIZE,
)
from app.analyzers.common.list_utils import random_list_sample


def build_estimated_commit_naming_quality_prompt(
    commit_messages: list,
) -> str:
    commit_messages_sample = random_list_sample(
            samples=commit_messages,
            sample_size=ESTIMATED_COMMIT_NAMING_QUALITY_SAMPLE_SIZE,
            seed=ESTIMATED_COMMIT_NAMING_QUALITY_SAMPLE_SEED,
        )

    if not isinstance(commit_messages_sample, list):
        raise RuntimeError("Commit messages were not in the expected format.")

    formatted_commit_messages_sample = "\n".join(
        f"{index + 1}. {message}"
        for index, message in enumerate(commit_messages_sample)
    )[:5000]

    template = """
You are analyzing the naming quality of Git commit messages in a GitHub repository.

Score the commit naming quality using this EXACT rubric
(you may also use partial points, e.g. 1.55 / 2.0):

1. Consistency of naming convention (0.0–2.0)
- Reward repositories where commit names consistently start with conventional action words
  such as "add", "fix", "refactor", "update", "remove", etc.
- Reward consistent formatting/casing style across commits.
- Penalize inconsistent styles, mixed casing, or mixed variants if they feel chaotic.

2. Commit message length quality (0.0–2.0)
- Reward commit names that are usually descriptive but not excessively long.
- Very short vague commit names should score lower.
- Very long commit names should also score lower.
- Prefer concise but still informative messages.

3. Use of meaningful technical / conventional terms (0–2.0)
- Reward commit messages that use concrete technical terms
  such as API, backend, frontend, auth, schema, migration, model, controller, test, etc.
- Reward messages that clearly refer to specific technical concepts.

4. Avoidance of vague / bad-practice wording (0–2.0)
- Penalize vague words like "stuff", "thing", "misc", "tmp", "wip", "random", etc.
- Penalize low-information commit naming habits.

5. Readability and clarity / does the message make logical sense (0–2.0)
- Reward messages that are easy to read and provide clear context, such as
  "Fix typo in user authentication logic" or
  "Update README with correct installation instructions".
- Penalize low-information commit naming habits.

Rules:
- Total score MUST be the sum of all 5 categories (0.0–10.0).
- Be conservative when scoring.
- Evaluate ONLY the visible commit messages.
- Do not assume the unseen commit history is better or worse.
- Focus only on naming quality, not on whether the code change itself is good.
- Short commit messages are not automatically bad if they are still clear.
- Long commit messages are not automatically bad if they are still readable and specific.

Return ONLY valid JSON in this format:

{{
  "rating": number (0.0-10.0, for example, 7.78),
  "explanation": string (0-250 characters, for example, "The commit messages are generally 
  well-formatted and provide good context, but the wording is slightly inconsistent.")
}}

Commit messages:
\"\"\"
{formatted_commit_messages_sample}
\"\"\"
""".strip()

    return template.format(
        formatted_commit_messages_sample=formatted_commit_messages_sample,
    )