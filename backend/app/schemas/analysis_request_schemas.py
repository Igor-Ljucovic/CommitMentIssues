from typing import Any
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class AnalysisFileInput(BaseModel):
    id: int | None = Field(default=None, ge=1)
    original_file_name: str = Field(..., min_length=1)
    github_links: list[str] = Field(default_factory=list)

    @field_validator("original_file_name")
    @classmethod
    def validate_original_file_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("original_file_name must not be empty.")
        return value

    @field_validator("github_links")
    @classmethod
    def validate_github_links(cls, links: list[str]) -> list[str]:
        cleaned_links: list[str] = []

        for link in links:
            cleaned = link.strip()
            if not cleaned:
                continue

            parsed = urlparse(cleaned)
            if parsed.netloc.lower() not in {"github.com", "www.github.com"}:
                raise ValueError(f'Invalid GitHub URL: "{cleaned}"')

            path_parts = [part for part in parsed.path.strip("/").split("/") if part]
            if len(path_parts) < 2:
                raise ValueError(f'GitHub URL must point to a repository: "{cleaned}"')

            cleaned_links.append(cleaned)

        return cleaned_links


class RepositoryInput(BaseModel):
    repo_url: str = Field(..., min_length=1)
    source_file_id: int | None = Field(default=None, ge=1)
    source_file_name: str | None = None

    @field_validator("repo_url")
    @classmethod
    def validate_repo_url(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("repo_url must not be empty.")

        parsed = urlparse(value)
        if parsed.netloc.lower() not in {"github.com", "www.github.com"}:
            raise ValueError("repo_url must be a valid GitHub repository URL.")

        path_parts = [part for part in parsed.path.strip("/").split("/") if part]
        if len(path_parts) < 2:
            raise ValueError("repo_url must point to a GitHub repository.")

        return value

    def get_owner_and_repository_name(self) -> tuple[str, str]:
        parsed = urlparse(self.repo_url.strip())
        path_parts = [part for part in parsed.path.strip("/").split("/") if part]

        owner = path_parts[0].strip()
        repository_name = path_parts[1].strip()

        if repository_name.endswith(".git"):
            repository_name = repository_name[:-4]

        if not owner or not repository_name:
            raise ValueError("repo_url must contain both repository owner and repository name.")

        return owner, repository_name


class NumericRange(BaseModel):
    min: str | None = None
    max: str | None = None


class DateRange(BaseModel):
    before: str | None = None
    after: str | None = None


class BooleanRequirement(BaseModel):
    selected: str | None = None


class AnalysisSubcategoryConfig(BaseModel):
    weight: int | float | None = None
    hardRequirementRange: NumericRange | DateRange | None = None
    recommendedRange: NumericRange | DateRange | None = None
    idealRange: NumericRange | DateRange | None = None
    hardRequirement: BooleanRequirement | None = None
    recommendedRequirement: BooleanRequirement | None = None
    idealRequirement: BooleanRequirement | None = None

    model_config = ConfigDict(extra="allow")


class AnalysisCategoryConfig(BaseModel):
    weight: int | float | None = None
    subcategories: dict[str, AnalysisSubcategoryConfig] = Field(default_factory=dict)

    model_config = ConfigDict(extra="allow")


class AnalysisRequest(BaseModel):
    files: list[AnalysisFileInput] = Field(default_factory=list)

    model_config = ConfigDict(extra="allow")

    @field_validator("files")
    @classmethod
    def validate_files_not_empty(cls, files: list[AnalysisFileInput]) -> list[AnalysisFileInput]:
        if not files:
            raise ValueError("At least one file must be provided.")
        return files

    @model_validator(mode="after")
    def validate_top_level_categories(self) -> "AnalysisRequest":
        for key, value in self.model_extra.items():
            if not isinstance(value, dict):
                raise ValueError(f'Top-level field "{key}" must be an object when provided.')

            AnalysisCategoryConfig.model_validate(value)

        return self

    def get_category_configs(self) -> dict[str, AnalysisCategoryConfig]:
        categories: dict[str, AnalysisCategoryConfig] = {}

        for key, value in self.model_extra.items():
            if isinstance(value, dict):
                categories[key] = AnalysisCategoryConfig.model_validate(value)

        return categories

    def get_repository_inputs(self) -> list[RepositoryInput]:
        # currently DOESN'T skip files that have exactly the same repository URLs
        # as 1 previous file, I had it implemented like that at first, but it
        # could cause confusion so I scrapped that idea.
        repositories: list[RepositoryInput] = []

        for file in self.files:
            file_seen_urls: set[str] = set()

            for repo_url in file.github_links:
                normalized_url = repo_url.strip().rstrip("/")

                if normalized_url in file_seen_urls:
                    continue

                file_seen_urls.add(normalized_url)

                repositories.append(
                    RepositoryInput(
                        repo_url=normalized_url,
                        source_file_id=file.id,
                        source_file_name=file.original_file_name,
                    )
                )

        return repositories

    def to_analysis_payload(self) -> dict[str, Any]:
        payload = {
            "files": [file.model_dump() for file in self.files],
        }

        for key, value in self.model_extra.items():
            payload[key] = value

        return payload