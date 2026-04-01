from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# This file only validates the general structure , but it does NOT 
# strictly enforce an exact format (i.e. if min > max, or 
# if the subcategory is called "general" or "General", 
# or if a field that shouln't have a DateRange has a NumberRange instead, but
# it will enforce that if a field is provided, it must be in one of the correct formats
# This file will only be changed when the JSON data becomes final)

class AnalysisFileInput(BaseModel):
    name: str = Field(..., min_length=1)
    size: int = Field(..., ge=0)
    type: str = Field(..., min_length=1)

    @field_validator("name", "type")
    @classmethod
    def validate_non_empty_strings(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("File fields must not be empty.")
        return value


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
                raise ValueError(
                    f'Top-level field "{key}" must be an object when provided.'
                )

            AnalysisCategoryConfig.model_validate(value)

        return self

    def get_category_configs(self) -> dict[str, AnalysisCategoryConfig]:
        categories: dict[str, AnalysisCategoryConfig] = {}

        for key, value in self.model_extra.items():
            if isinstance(value, dict):
                categories[key] = AnalysisCategoryConfig.model_validate(value)

        return categories

    def to_analysis_payload(self) -> dict[str, Any]:
        payload = {
            "files": [file.model_dump() for file in self.files],
        }

        for key, value in self.model_extra.items():
            payload[key] = value

        return payload