import type { ChangeEvent } from "react";
import { ANALYSIS_CATEGORIES } from "../data/analysisCategories";
import type {
  AnalysisSelectionState,
  ItemWeightsState,
  MetricParametersState,
  MetricParameterValue,
} from "../types";
import AnalysisCategoryCard from "./AnalysisCategoryCard";

type RepositoryAnalysisSectionProps = {
  analysisSelections: AnalysisSelectionState;
  itemWeights: ItemWeightsState;
  metricParameters: MetricParametersState;
  onAnalysisItemToggle: (categoryTitle: string, itemName: string) => void;
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
  itemWeights,
  metricParameters,
  onAnalysisItemToggle,
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
            analysisSelectionsForCategory={
              analysisSelections[category.title] ?? {}
            }
            itemWeightsForCategory={itemWeights[category.title] ?? {}}
            metricParametersForCategory={metricParameters[category.title] ?? {}}
            onAnalysisItemToggle={onAnalysisItemToggle}
            onItemWeightChange={onItemWeightChange}
            onMetricParameterChange={onMetricParameterChange}
          />
        ))}
      </div>
    </section>
  );
}

export default RepositoryAnalysisSection;