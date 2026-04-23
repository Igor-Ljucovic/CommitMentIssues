from copy import deepcopy

from app.schemas.analysis_response_schemas import (
    AnalysisResponse,
    FileAnalysisResult,
    RepositoryAnalysisResult,
)


def merge_analysis_responses(
    responses: list[AnalysisResponse],
) -> AnalysisResponse:
    if not responses:
        return AnalysisResponse(files=[], warnings=[])

    result = deepcopy(responses[0])

    file_map: dict[tuple[int | None, str], FileAnalysisResult] = {
        (file_result.file_id, file_result.file_name): file_result
        for file_result in result.files
    }

    for response in responses[1:]:
        for incoming_file in response.files:
            file_key = (incoming_file.file_id, incoming_file.file_name)

            if file_key not in file_map:
                copied_file = deepcopy(incoming_file)
                file_map[file_key] = copied_file
                result.files.append(copied_file)
                continue

            existing_file = file_map[file_key]
            _merge_repositories(existing_file, incoming_file)

        result.warnings.extend(response.warnings)

    return result


def _merge_repositories(
    existing_file: FileAnalysisResult,
    incoming_file: FileAnalysisResult,
) -> None:
    repository_map: dict[str, RepositoryAnalysisResult] = {
        repository.repository_url: repository
        for repository in existing_file.repositories
    }

    for incoming_repository in incoming_file.repositories:
        existing_repository = repository_map.get(incoming_repository.repository_url)

        if existing_repository is None:
            existing_file.repositories.append(deepcopy(incoming_repository))
            continue

        existing_repository.metrics.extend(deepcopy(incoming_repository.metrics))