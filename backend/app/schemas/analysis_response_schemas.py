from pydantic import BaseModel, Field


class RepositoryMetricResult(BaseModel):
    metric_key: str = Field(..., min_length=1)
    display_name: str = Field(..., min_length=1)
    value: str | int | float | bool | None = None
    status: str = Field(..., min_length=1)
    message: str | None = None


class RepositoryAnalysisResult(BaseModel):
    repository_url: str = Field(..., min_length=1)
    metrics: list[RepositoryMetricResult] = Field(default_factory=list)

class FileAnalysisResult(BaseModel):
    file_id: int | None = None
    file_name: str
    repositories: list[RepositoryAnalysisResult] = Field(default_factory=list)


class AnalysisResponse(BaseModel):
    files: list[FileAnalysisResult] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    # tells Pydantic that you can create this model from objects, not just dicts
    class Config:
        from_attributes = True