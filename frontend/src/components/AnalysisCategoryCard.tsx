import { useState, type ChangeEvent } from "react";
import type {
  AnalysisCategory,
  AnalysisItem,
  MetricParameterValue,
} from "../types";
import { DEFAULT_WEIGHT } from "../data/analysisCategories";
import MetricParameterInputs from "./MetricParameterInputs";

type AnalysisCategoryCardProps = {
  category: AnalysisCategory;
  categoryWeight: number;
  analysisSelectionsForCategory: Record<string, boolean>;
  itemWeightsForCategory: Record<string, number>;
  metricParametersForCategory: Record<
    string,
    Record<string, MetricParameterValue>
  >;
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

function AnalysisCategoryCard({
  category,
  categoryWeight,
  analysisSelectionsForCategory,
  itemWeightsForCategory,
  metricParametersForCategory,
  onAnalysisItemToggle,
  onCategoryWeightChange,
  onItemWeightChange,
  onMetricParameterChange,
}: AnalysisCategoryCardProps) {
  const [isCategoryExpanded, setIsCategoryExpanded] = useState(false);

  const [expandedItems, setExpandedItems] = useState<Record<string, boolean>>(
    () => {
      const initialState: Record<string, boolean> = {};

      const collectExpandableItems = (items: AnalysisItem[]) => {
        items.forEach((item) => {
          const hasSubItems = Boolean(item.subItems && item.subItems.length > 0);
          const hasParameters = Boolean(
            item.parameters && item.parameters.length > 0,
          );

          if (hasSubItems || hasParameters) {
            initialState[item.name] = false;
          }

          if (item.subItems) {
            collectExpandableItems(item.subItems);
          }
        });
      };

      collectExpandableItems(category.items);
      return initialState;
    },
  );

  const toggleItemExpanded = (itemName: string) => {
    setExpandedItems((previous) => ({
      ...previous,
      [itemName]: !previous[itemName],
    }));
  };

  const renderItem = (item: AnalysisItem, depth = 0) => {
    const isChecked = analysisSelectionsForCategory?.[item.name] ?? false;
    const currentItemWeight =
      itemWeightsForCategory?.[item.name] ?? DEFAULT_WEIGHT;
    const parameterValues = metricParametersForCategory?.[item.name] ?? {};
    const hasSubItems = Boolean(item.subItems && item.subItems.length > 0);
    const hasParameters = Boolean(item.parameters && item.parameters.length > 0);
    const isExpandable = hasSubItems || hasParameters;
    const isExpanded = expandedItems[item.name] ?? false;

    return (
      <li
        key={item.name}
        style={{
          marginLeft: depth > 1 ? `${(depth - 1) * 1.35}rem` : 0,
          listStyle: "none",
          marginTop: depth > 0 ? "0.65rem" : "0",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "0.75rem",
            justifyContent: "space-between",
            paddingBottom: "0.4rem",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "0.55rem",
              flex: 1,
              minWidth: 0,
            }}
          >
            {isExpandable ? (
              <button
                type="button"
                onClick={() => toggleItemExpanded(item.name)}
                style={{
                  border: "none",
                  background: "transparent",
                  cursor: "pointer",
                  fontSize: "0.9rem",
                  padding: 0,
                  width: "1rem",
                  flexShrink: 0,
                }}
              >
                {isExpanded ? "▼" : "▶"}
              </button>
            ) : (
              <span
                style={{
                  width: "1rem",
                  display: "inline-block",
                  flexShrink: 0,
                }}
              />
            )}

            <label
              style={{
                display: "flex",
                alignItems: "center",
                gap: "0.65rem",
                cursor: "pointer",
                flex: 1,
                minWidth: 0,
              }}
            >
              <input
                type="checkbox"
                checked={isChecked}
                onChange={() => onAnalysisItemToggle(category.title, item.name)}
              />

              <span
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "0.45rem",
                  minWidth: 0,
                }}
              >
                <span>{item.name}</span>

                {item.tooltipText ? (
                  <span
                    title={item.tooltipText}
                    aria-label={item.tooltipText}
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      justifyContent: "center",
                      width: "1rem",
                      height: "1rem",
                      borderRadius: "50%",
                      border: "1px solid #999",
                      fontSize: "0.72rem",
                      color: "#666",
                      backgroundColor: "#f5f5f5",
                      cursor: "help",
                      flexShrink: 0,
                      lineHeight: 1,
                      userSelect: "none",
                    }}
                  >
                    i
                  </span>
                ) : null}
              </span>
            </label>
          </div>

          <input
            id={`item-weight-${category.title}-${item.name}`}
            type="range"
            min="0"
            max="10"
            step="1"
            value={currentItemWeight}
            onChange={(event) =>
              onItemWeightChange(category.title, item.name, event)
            }
            style={{
              width: depth > 0 ? "90px" : "110px",
              flexShrink: 0,
            }}
          />
        </div>

        {isExpanded && hasParameters ? (
          <MetricParameterInputs
            categoryTitle={category.title}
            item={item}
            parameterValues={parameterValues}
            onMetricParameterChange={onMetricParameterChange}
          />
        ) : null}

        {isExpanded && hasSubItems ? (
          <ul style={{ margin: 0, padding: 0 }}>
            {item.subItems!.map((subItem) => renderItem(subItem, depth + 1))}
          </ul>
        ) : null}
      </li>
    );
  };

  return (
    <div className="result-card">
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: "1rem",
          marginBottom: "1rem",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "0.6rem" }}>
          <button
            type="button"
            onClick={() => setIsCategoryExpanded((previous) => !previous)}
            style={{
              border: "none",
              background: "transparent",
              cursor: "pointer",
              fontSize: "1rem",
              padding: 0,
              width: "1rem",
              flexShrink: 0,
            }}
          >
            {isCategoryExpanded ? "▼" : "▶"}
          </button>

          <h3 style={{ margin: 0 }}>{category.title}</h3>
        </div>

        <input
          id={`category-weight-${category.title}`}
          type="range"
          min="0"
          max="10"
          step="1"
          value={categoryWeight}
          onChange={(event) => onCategoryWeightChange(category.title, event)}
          style={{
            width: "200px",
            flexShrink: 0,
          }}
        />
      </div>

      {isCategoryExpanded ? (
        <ul className="link-list" style={{ paddingLeft: 0, margin: 0 }}>
          {category.items.map((item) => renderItem(item))}
        </ul>
      ) : null}
    </div>
  );
}

export default AnalysisCategoryCard;