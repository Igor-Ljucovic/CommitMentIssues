from app.analyzers.general.total_lines_of_code_analyzer.total_lines_of_code_metric import get_total_lines_of_code_metric
from app.analyzers.general.total_lines_of_code_analyzer.total_lines_of_code_constants import (
    TOTAL_LINES_OF_CODE_CATEGORY_NAME,
    TOTAL_LINES_OF_CODE_SUBCATEGORY_NAME,
)
from app.analyzers.general.total_lines_of_code_filtered_analyzer.total_lines_of_code_filtered_metric import get_total_lines_of_code_filtered_metric
from app.analyzers.general.total_lines_of_code_filtered_analyzer.total_lines_of_code_filtered_constants import (
    TOTAL_LINES_OF_CODE_FILTERED_CATEGORY_NAME,
    TOTAL_LINES_OF_CODE_FILTERED_SUBCATEGORY_NAME,
)
from app.analyzers.code_and_repository_quality.libraries_used_analyzer.libraries_used_metric import get_libraries_used_metric
from app.analyzers.code_and_repository_quality.libraries_used_analyzer.libraries_used_constants import (
    LIBRARIES_USED_CATEGORY_NAME,
    LIBRARIES_USED_SUBCATEGORY_NAME,
)

TARBALL_REQUIRING_METRICS: frozenset = frozenset({
    get_total_lines_of_code_metric,
    get_total_lines_of_code_filtered_metric,
    get_libraries_used_metric,
})

TARBALL_REQUIRING_SUBCATEGORIES: frozenset[tuple[str, str]] = frozenset({
    (TOTAL_LINES_OF_CODE_CATEGORY_NAME, TOTAL_LINES_OF_CODE_SUBCATEGORY_NAME),
    (TOTAL_LINES_OF_CODE_FILTERED_CATEGORY_NAME, TOTAL_LINES_OF_CODE_FILTERED_SUBCATEGORY_NAME),
    (LIBRARIES_USED_CATEGORY_NAME, LIBRARIES_USED_SUBCATEGORY_NAME),
})
