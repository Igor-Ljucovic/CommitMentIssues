from copy import deepcopy

from app.schemas.analysis_response_schemas import AnalysisResponse


def rank_metrics(
    analysis_response: AnalysisResponse,
    descending: bool = True,
) -> AnalysisResponse:
    result = deepcopy(analysis_response)

    def sort_key(value: float | None) -> tuple[bool, float]:
        return (value is None, value if value is not None else 0.0)

    for file_result in result.files:
        for repository in file_result.repositories:
            repository.metrics.sort(
                key=lambda metric: sort_key(metric.rating),
                reverse=descending,
            )

    return result