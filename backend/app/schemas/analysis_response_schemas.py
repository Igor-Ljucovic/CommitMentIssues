from pydantic import BaseModel, Field


class RepositoryMetricResult(BaseModel):
    metric_key: str = Field(..., min_length=1)
    metric_name: str = Field(..., min_length=1)
    value: str | int | float | bool | None = None
    weight: float | None = None
    rating: float | None = None
    requirement_failed: bool | None = None
    status: str = Field(..., min_length=1)
    message: str | None = None


class RepositoryAnalysisResult(BaseModel):
    repository_url: str = Field(..., min_length=1)
    rating: float | None = None
    requirement_failed_metrics: list[str] | None = None
    status_failed_metrics: list[str] | None = None
    metrics: list[RepositoryMetricResult] = Field(default_factory=list)


class FileAnalysisResult(BaseModel):
    file_id: int | None = None
    file_name: str
    rating: float | None = None
    requirement_failed_repositories: list[str] | None = None
    status_failed_repositories: list[str] | None = None
    repositories: list[RepositoryAnalysisResult] = Field(default_factory=list)


class AnalysisResponse(BaseModel):
    files: list[FileAnalysisResult] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    class Config:
        from_attributes = True