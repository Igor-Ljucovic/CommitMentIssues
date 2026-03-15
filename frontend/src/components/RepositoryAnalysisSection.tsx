import type { ChangeEvent } from "react";
import { ANALYSIS_CATEGORIES, DEFAULT_WEIGHT } from "../data/analysisCategories";
import type {
  AnalysisSelectionState,
  CategoryWeightsState,
  ItemWeightsState,
  MetricParametersState,
  MetricParameterValue,
} from "../types";
import AnalysisCategoryCard from "./AnalysisCategoryCard";

type RepositoryAnalysisSectionProps = {
  analysisSelections: AnalysisSelectionState;
  categoryWeights: CategoryWeightsState;
  itemWeights: ItemWeightsState;
  metricParameters: MetricParametersState;
  onAnalysisItemToggle: (categoryTitle: string, itemName: string) => void;
  onCategoryWeightChange: (
    categoryTitle: string,
    event: ChangeEvent<HTMLInputElement>,
  ) => void;
  onItemWeightChange: (
    categoryTitle: string,
    itemName: string,
    event: ChangeEvent<HTMLInputElement>,
  ) => void;
  onMetricParameterChange: (
    categoryTitle: string,
    itemName: string,
    parameterKey: string,
    valueKey: keyof MetricParameterValue,
    value: string,
  ) => void;
};

function RepositoryAnalysisSection({
  analysisSelections,
  categoryWeights,
  itemWeights,
  metricParameters,
  onAnalysisItemToggle,
  onCategoryWeightChange,
  onItemWeightChange,
  onMetricParameterChange,
}: RepositoryAnalysisSectionProps) {
  return (
    <section className="card">
      <h2>Repository Analysis Sections</h2>
      <p className="card-description">
        Choose which repository metrics should be included in the analysis.
      </p>

      <div className="results-list">
        {ANALYSIS_CATEGORIES.map((category) => (
          <AnalysisCategoryCard
            key={category.title}
            category={category}
            categoryWeight={categoryWeights[category.title] ?? DEFAULT_WEIGHT}
            analysisSelectionsForCategory={
              analysisSelections[category.title] ?? {}
            }
            itemWeightsForCategory={itemWeights[category.title] ?? {}}
            metricParametersForCategory={metricParameters[category.title] ?? {}}
            onAnalysisItemToggle={onAnalysisItemToggle}
            onCategoryWeightChange={onCategoryWeightChange}
            onItemWeightChange={onItemWeightChange}
            onMetricParameterChange={onMetricParameterChange}
          />
        ))}
      </div>
    </section>
  );
}

export default RepositoryAnalysisSection;