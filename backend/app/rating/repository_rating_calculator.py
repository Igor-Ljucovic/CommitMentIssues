from copy import deepcopy

from app.schemas.analysis_response_schemas import AnalysisResponse


def calculate_repository_ratings(
    analysis_response: AnalysisResponse,
) -> AnalysisResponse:
    result = deepcopy(analysis_response)

    for file_result in result.files:
        for repository in file_result.repositories:
            weighted_sum = 0.0
            total_weight = 0.0

            requirement_failed_metrics: list[str] = []
            status_failed_metrics: list[str] = []

            for metric in repository.metrics:
                metric_weight = (float(metric.weight) if metric.weight is not None else 0.0)

                metric_rating = (float(metric.rating) if metric.rating is not None else None)

                if metric_rating is not None and metric_weight > 0:
                    weighted_sum += metric_weight * metric_rating
                    total_weight += metric_weight

                if metric.requirement_failed is True:
                    requirement_failed_metrics.append(metric.metric_name)

                if metric.status != "success":
                    status_failed_metrics.append(metric.metric_name)

            repository.rating = round(weighted_sum / total_weight, 2) if total_weight > 0 else 0.0

            if requirement_failed_metrics:
                repository.requirement_failed_metrics = requirement_failed_metrics

            if status_failed_metrics:
                repository.status_failed_metrics = status_failed_metrics

    return result