from pydantic import BaseModel, Field


class FileRepoRating(BaseModel):
    name: str = Field(..., min_length=1)
    average_rating: float = Field(..., ge=0.0, le=10.0)

    class Config:
        from_attributes = True


class AnalysisResponse(BaseModel):
    file_repo_ratings: list[FileRepoRating] = Field(default_factory=list)

    class Config:
        from_attributes = True