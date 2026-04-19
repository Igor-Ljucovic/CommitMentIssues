import { ANALYSIS_CATEGORIES, DEFAULT_WEIGHT } from "../data/analysisCategories";
import type {
  AnalysisItem,
  AnalysisSelectionState,
  CategoryWeightsState,
  ItemWeightsState,
  MetricParametersState,
  MetricParameterValue,
} from "../types/types";

const getAllItems = (items: AnalysisItem[]): AnalysisItem[] => {
  return items.flatMap((item) => [
    item,
    ...(item.subItems ? getAllItems(item.subItems) : []),
  ]);
};

export const createInitialAnalysisSelections = (): AnalysisSelectionState => {
  return ANALYSIS_CATEGORIES.reduce<AnalysisSelectionState>(
    (categoryAcc, category) => {
      categoryAcc[category.title] = getAllItems(category.items).reduce<
        Record<string, boolean>
      >((itemAcc, item) => {
        itemAcc[item.name] = false;
        return itemAcc;
      }, {});

      return categoryAcc;
    },
    {},
  );
};

export const createInitialCategoryWeights = (): CategoryWeightsState => {
  return ANALYSIS_CATEGORIES.reduce<CategoryWeightsState>((acc, category) => {
    acc[category.title] = DEFAULT_WEIGHT;
    return acc;
  }, {});
};

export const createInitialItemWeights = (): ItemWeightsState => {
  return ANALYSIS_CATEGORIES.reduce<ItemWeightsState>((categoryAcc, category) => {
    categoryAcc[category.title] = getAllItems(category.items).reduce<
      Record<string, number>
    >((itemAcc, item) => {
      itemAcc[item.name] = DEFAULT_WEIGHT;
      return itemAcc;
    }, {});

    return categoryAcc;
  }, {});
};

export const createInitialMetricParameters = (): MetricParametersState => {
  return ANALYSIS_CATEGORIES.reduce<MetricParametersState>(
    (categoryAcc, category) => {
      categoryAcc[category.title] = getAllItems(category.items).reduce<
        Record<string, Record<string, MetricParameterValue>>
      >((itemAcc, item) => {
        itemAcc[item.name] = {};

        item.parameters?.forEach((parameter) => {
          if (parameter.type === "date-range") {
            itemAcc[item.name][parameter.key] = { before: "", after: "" };
            return;
          }

          itemAcc[item.name][parameter.key] = { min: "", max: "" };
        });

        return itemAcc;
      }, {});

      return categoryAcc;
    },
    {},
  );
};