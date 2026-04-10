from copy import deepcopy

from app.schemas.analysis_response_schemas import AnalysisResponse


def rank_files(
    analysis_response: AnalysisResponse,
    descending: bool = True,
) -> AnalysisResponse:
    result = deepcopy(analysis_response)

    def get_safe_rating(value: float | None) -> float:
        # unrated files are treated as having the lowest possible rating
        return value if value is not None else float("-inf")

    for file_result in result.files:
        file_result.repositories.sort(
            key=lambda repo: get_safe_rating(repo.rating),
            reverse=descending,
        )

    result.files.sort(
        key=lambda file: get_safe_rating(file.rating),
        reverse=descending,
    )

    return result