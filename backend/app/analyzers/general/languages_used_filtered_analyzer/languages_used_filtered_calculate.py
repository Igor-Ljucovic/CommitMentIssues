from app.analyzers.general.languages_used_analyzer.languages_used_fetch import (
    fetch_languages_used,
)
from app.analyzers.general.languages_used_analyzer.languages_used_constants import (
    LANGUAGES_USED_METRIC_KEY,
)
from app.analyzers.general.languages_used_filtered_analyzer.languages_used_filtered_constants import (
    LANGUAGES_USED_FILTERED_METRIC_KEY,
    LANGUAGES_USED_FILTERED_PROGRAMMING_LANGUAGES
)


async def languages_used_filtered_calculate(
    owner: str,
    repository_name: str,
) -> dict:
    result = await fetch_languages_used(
        owner=owner,
        repository_name=repository_name,
    )

    languages_used  = result[LANGUAGES_USED_METRIC_KEY]

    languages_used_filtered = list(set(languages_used) & set(LANGUAGES_USED_FILTERED_PROGRAMMING_LANGUAGES))
    
    return {
        LANGUAGES_USED_METRIC_KEY: languages_used,
        LANGUAGES_USED_FILTERED_METRIC_KEY: languages_used_filtered
    }