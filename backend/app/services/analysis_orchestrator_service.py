import hashlib

from app.schemas.analysis_request import AnalysisRequest
from app.schemas.analysis_response import AnalysisResponse, FileRepoRating


def _generate_sample_rating(file_name: str) -> float:
    """
    Generates a deterministic pseudo-random rating in the range [5.50, 9.50]
    based on the file name, so the same file always gets the same sample score.
    This is just a placeholder for demonstration purposes and will be replaced later.
    """
    digest = hashlib.sha256(file_name.strip().lower().encode("utf-8")).hexdigest()
    numeric_value = int(digest[:8], 16)

    min_rating = 5.50
    max_rating = 9.50

    normalized = numeric_value / 0xFFFFFFFF
    rating = min_rating + (max_rating - min_rating) * normalized

    return round(rating, 2)


async def analyze_repositories(request: AnalysisRequest) -> AnalysisResponse:
    if not request.files:
        raise ValueError("At least one file must be provided for analysis.")

    file_repo_ratings: list[FileRepoRating] = []

    for file in request.files:
        file_repo_ratings.append(
            FileRepoRating(
                name=file.name,
                average_rating=_generate_sample_rating(file.name),
            )
        )

    return AnalysisResponse(file_repo_ratings=file_repo_ratings)