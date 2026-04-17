from copy import deepcopy

from app.schemas.analysis_response_schemas import (
    FileAnalysisResult,
    RepositoryAnalysisResult,
    AnalysisResponse
)


def merge_analysis_responses(
    github_response: AnalysisResponse,
    openai_response: AnalysisResponse,
) -> AnalysisResponse:
    result = deepcopy(github_response)

    file_map: dict[tuple[int | None, str], FileAnalysisResult] = {
        (file_result.file_id, file_result.file_name): file_result
        for file_result in result.files
    }

    for openai_file in openai_response.files:
        file_key = (openai_file.file_id, openai_file.file_name)

        if file_key not in file_map:
            file_map[file_key] = deepcopy(openai_file)
            result.files.append(file_map[file_key])
            continue

        existing_file = file_map[file_key]
        _merge_repositories(existing_file, openai_file)

    result.warnings.extend(openai_response.warnings)

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