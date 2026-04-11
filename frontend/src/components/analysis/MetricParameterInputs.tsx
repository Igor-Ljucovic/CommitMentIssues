import type { AnalysisItem, MetricParameterValue } from "@/types/types";

type MetricParameterInputsProps = {
  categoryTitle: string;
  item: AnalysisItem;
  parameterValues: Record<string, MetricParameterValue>;
  onMetricParameterChange: (
    categoryTitle: string,
    itemName: string,
    parameterKey: string,
    valueKey: keyof MetricParameterValue,
    value: string,
  ) => void;
};

function MetricParameterInputs({
  categoryTitle,
  item,
  parameterValues,
  onMetricParameterChange,
}: MetricParameterInputsProps) {
  if (!item.parameters || item.parameters.length === 0) {
    return null;
  }

  return (
    <div
      style={{
        marginLeft: "1.9rem",
        marginTop: "0.2rem",
        display: "flex",
        flexDirection: "column",
        gap: "0.75rem",
      }}
    >
      {item.parameters.map((parameter) => {
        const currentValue = parameterValues?.[parameter.key] ?? {};

        return (
          <div
            key={`${item.name}-${parameter.key}`}
            style={{
              border: "1px solid #d6d6d6",
              borderRadius: "8px",
              padding: "0.75rem",
              backgroundColor: "#fafafa",
            }}
          >
            <div
              style={{
                fontSize: "0.92rem",
                fontWeight: 600,
                marginBottom: "0.55rem",
              }}
            >
              {parameter.label}
            </div>

            {parameter.type === "int-range" ? (
              <div
                style={{
                  display: "flex",
                  gap: "0.75rem",
                  flexWrap: "wrap",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "0.3rem",
                  }}
                >
                  <label style={{ fontSize: "0.85rem" }}>Min</label>
                  <input
                    type="number"
                    value={currentValue.min ?? ""}
                    onChange={(event) =>
                      onMetricParameterChange(
                        categoryTitle,
                        item.name,
                        parameter.key,
                        "min",
                        event.target.value,
                      )
                    }
                    style={{
                      padding: "0.45rem 0.55rem",
                      borderRadius: "6px",
                      border: "1px solid #b8b8b8",
                      minWidth: "120px",
                    }}
                  />
                </div>

                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "0.3rem",
                  }}
                >
                  <label style={{ fontSize: "0.85rem" }}>Max</label>
                  <input
                    type="number"
                    value={currentValue.max ?? ""}
                    onChange={(event) =>
                      onMetricParameterChange(
                        categoryTitle,
                        item.name,
                        parameter.key,
                        "max",
                        event.target.value,
                      )
                    }
                    style={{
                      padding: "0.45rem 0.55rem",
                      borderRadius: "6px",
                      border: "1px solid #b8b8b8",
                      minWidth: "120px",
                    }}
                  />
                </div>
              </div>
            ) : parameter.type === "percentage-range" ? (
              <div
                style={{
                  display: "flex",
                  gap: "0.75rem",
                  flexWrap: "wrap",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "0.3rem",
                  }}
                >
                  <label style={{ fontSize: "0.85rem" }}>Min</label>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    placeholder="0"
                    value={currentValue.min ?? ""}
                    onChange={(event) =>
                      onMetricParameterChange(
                        categoryTitle,
                        item.name,
                        parameter.key,
                        "min",
                        event.target.value,
                      )
                    }
                    style={{
                      padding: "0.45rem 0.55rem",
                      borderRadius: "6px",
                      border: "1px solid #b8b8b8",
                      minWidth: "120px",
                    }}
                  />
                </div>

                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "0.3rem",
                  }}
                >
                  <label style={{ fontSize: "0.85rem" }}>Max</label>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    placeholder="100"
                    value={currentValue.max ?? ""}
                    onChange={(event) =>
                      onMetricParameterChange(
                        categoryTitle,
                        item.name,
                        parameter.key,
                        "max",
                        event.target.value,
                      )
                    }
                    style={{
                      padding: "0.45rem 0.55rem",
                      borderRadius: "6px",
                      border: "1px solid #b8b8b8",
                      minWidth: "120px",
                    }}
                  />
                </div>
              </div>
            ) : (
              <div
                style={{
                  display: "flex",
                  gap: "0.75rem",
                  flexWrap: "wrap",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "0.3rem",
                  }}
                >
                  <label style={{ fontSize: "0.85rem" }}>After</label>
                  <input
                    type="date"
                    value={currentValue.after ?? ""}
                    onChange={(event) =>
                      onMetricParameterChange(
                        categoryTitle,
                        item.name,
                        parameter.key,
                        "after",
                        event.target.value,
                      )
                    }
                    style={{
                      padding: "0.45rem 0.55rem",
                      borderRadius: "6px",
                      border: "1px solid #b8b8b8",
                      minWidth: "170px",
                    }}
                  />
                </div>

                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "0.3rem",
                  }}
                >
                  <label style={{ fontSize: "0.85rem" }}>Before</label>
                  <input
                    type="date"
                    value={currentValue.before ?? ""}
                    onChange={(event) =>
                      onMetricParameterChange(
                        categoryTitle,
                        item.name,
                        parameter.key,
                        "before",
                        event.target.value,
                      )
                    }
                    style={{
                      padding: "0.45rem 0.55rem",
                      borderRadius: "6px",
                      border: "1px solid #b8b8b8",
                      minWidth: "170px",
                    }}
                  />
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

export default MetricParameterInputs;