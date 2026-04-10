from copy import deepcopy

from app.schemas.analysis_response_schemas import AnalysisResponse


def rank_repositories(
    analysis_response: AnalysisResponse,
    descending: bool = True,
) -> AnalysisResponse:
    result = deepcopy(analysis_response)

    def sort_key(value: float | None) -> tuple[bool, float]:
        # unrated repositories are treated as having the lowest possible rating
        return (value is None, value if value is not None else 0.0)

    for file_result in result.files:
        file_result.repositories.sort(
            key=lambda repository: sort_key(repository.rating),
            reverse=descending,
        )

    return result