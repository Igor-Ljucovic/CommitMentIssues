import { useMemo, useState } from "react";
import type { ChangeEvent } from "react";
import "./App.css";

const ALLOWED_EXTENSIONS = [".txt", ".docx", ".pdf"];
const DEFAULT_WEIGHT = 5;

type FileScanResult = {
  file_name: string;
  github_links: string[];
};

type UploadResponse = {
  total_files: number;
  accepted_files: number;
  rejected_files: number;
  rejected_file_names: string[];
  scanned_files: FileScanResult[];
  unique_github_links: string[];
};

type AnalysisCategory = {
  title: string;
  items: string[];
};

type AnalysisSelectionState = Record<string, Record<string, boolean>>;
type CategoryWeightsState = Record<string, number>;
type ItemWeightsState = Record<string, Record<string, number>>;

const ANALYSIS_CATEGORIES: AnalysisCategory[] = [
  {
    title: "General",
    items: [
      "Repository Creation Date",
      "Total Commit Count",
      "Last Commit Date",
      "Commit Activity Timeline",
      "Repository Owner Type (Organization or Personal)",
      "Lines of Code and Unique Lines of Code",
    ],
  },
  {
    title: "Collaboration",
    items: [
      "Contributor Count",
      "Branch Overview",
      "Pull Request Acceptance Rate",
    ],
  },
  {
    title: "Documentation",
    items: [
      "README and Wiki Presence & Quality",
      "Project Summary and CV Match",
    ],
  },
  {
    title: "Consistency",
    items: [
      "Commit Naming Consistency",
      "Commit Message and Code Change Alignment",
      "Consistency of Class, Function, Variable, and File Naming",
    ],
  },
  {
    title: "Architecture",
    items: [
      "Software Architecture Overview",
      "Project Summary and Functional Match",
      "Code Duplication",
      "Tests and Test Coverage",
    ],
  },
  {
    title: "AI Code Analysis",
    items: [
      "Technology Stack Match with CV",
      "Commit Message and Code Change Alignment (AI)",
      "Naming and Project Structure Consistency (AI)",
      "Project Summary and CV Match (AI)",
      "Estimated AI-Generated Code Percentage",
    ],
  },
];

const createInitialAnalysisSelections = (): AnalysisSelectionState => {
  return ANALYSIS_CATEGORIES.reduce<AnalysisSelectionState>((categoryAcc, category) => {
    categoryAcc[category.title] = category.items.reduce<Record<string, boolean>>(
      (itemAcc, item) => {
        itemAcc[item] = true;
        return itemAcc;
      },
      {},
    );

    return categoryAcc;
  }, {});
};

const createInitialCategoryWeights = (): CategoryWeightsState => {
  return ANALYSIS_CATEGORIES.reduce<CategoryWeightsState>((acc, category) => {
    acc[category.title] = DEFAULT_WEIGHT;
    return acc;
  }, {});
};

const createInitialItemWeights = (): ItemWeightsState => {
  return ANALYSIS_CATEGORIES.reduce<ItemWeightsState>((categoryAcc, category) => {
    categoryAcc[category.title] = category.items.reduce<Record<string, number>>(
      (itemAcc, item) => {
        itemAcc[item] = DEFAULT_WEIGHT;
        return itemAcc;
      },
      {},
    );

    return categoryAcc;
  }, {});
};

function App() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [statusMessage, setStatusMessage] = useState<string>("");
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null);
  const [analysisSelections, setAnalysisSelections] =
    useState<AnalysisSelectionState>(createInitialAnalysisSelections);
  const [categoryWeights, setCategoryWeights] =
    useState<CategoryWeightsState>(createInitialCategoryWeights);
  const [itemWeights, setItemWeights] =
    useState<ItemWeightsState>(createInitialItemWeights);

  const acceptedFileTypes = useMemo(() => ALLOWED_EXTENSIONS.join(","), []);

  const isAllowedFile = (file: File): boolean => {
    const fileName = file.name.toLowerCase();
    return ALLOWED_EXTENSIONS.some((extension) => fileName.endsWith(extension));
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const fileList = event.target.files;

    if (!fileList) {
      return;
    }

    const filesArray = Array.from(fileList);

    const validFiles = filesArray.filter(isAllowedFile);
    const invalidFiles = filesArray.filter((file) => !isAllowedFile(file));

    setSelectedFiles((previousFiles) => {
      const combinedFiles = [...previousFiles, ...validFiles];

      return combinedFiles.filter(
        (file, index, array) =>
          index ===
          array.findIndex(
            (otherFile) =>
              otherFile.name === file.name &&
              otherFile.size === file.size &&
              otherFile.lastModified === file.lastModified,
          ),
      );
    });

    if (invalidFiles.length > 0) {
      setStatusMessage(
        `Some files were ignored because only TXT, DOCX, and PDF are allowed: ${invalidFiles
          .map((file) => file.name)
          .join(", ")}`,
      );
    } else {
      setStatusMessage("");
    }

    event.target.value = "";
  };

  const handleRemoveFile = (fileToRemove: File) => {
    setSelectedFiles((previousFiles) =>
      previousFiles.filter(
        (file) =>
          !(
            file.name === fileToRemove.name &&
            file.size === fileToRemove.size &&
            file.lastModified === fileToRemove.lastModified
          ),
      ),
    );
  };

  const getSelectedAnalysisMetrics = () => {
    const selected: string[] = [];

    Object.entries(analysisSelections).forEach(([category, items]) => {
      Object.entries(items).forEach(([metric, isChecked]) => {
        if (isChecked) {
          const categoryWeight = categoryWeights[category];
          const metricWeight = itemWeights[category]?.[metric];

          selected.push(
            `${category} (category weight: ${categoryWeight}) -> ${metric} (metric weight: ${metricWeight})`,
          );
        }
      });
    });

    return selected;
  };

  const handleUpload = async () => {
    const selectedMetrics = getSelectedAnalysisMetrics();

    console.log("Selected analysis metrics:");
    selectedMetrics.forEach((metric) => console.log(metric));

    console.log("All category weights:");
    Object.entries(categoryWeights).forEach(([category, weight]) => {
      console.log(`${category}: ${weight}`);
    });

    console.log("All subcategory weights:");
    Object.entries(itemWeights).forEach(([category, items]) => {
      Object.entries(items).forEach(([item, weight]) => {
        console.log(`${category} -> ${item}: ${weight}`);
      });
    });

    if (selectedFiles.length === 0) {
      setStatusMessage("Please select at least one file before uploading.");
      return;
    }

    try {
      setStatusMessage("Uploading files...");
      setUploadResult(null);

      const formData = new FormData();

      selectedFiles.forEach((file) => {
        formData.append("files", file);
      });

      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed.");
      }

      const result: UploadResponse = await response.json();
      setUploadResult(result);

      setStatusMessage(
        `Upload successful. Accepted ${result.accepted_files} of ${result.total_files} file(s). Found ${result.unique_github_links.length} unique GitHub link(s).`,
      );
    } catch (error) {
      console.error(error);
      setStatusMessage("Something went wrong while uploading the files.");
    }
  };

  const handleAnalysisItemToggle = (categoryTitle: string, itemName: string) => {
    setAnalysisSelections((previousSelections) => ({
      ...previousSelections,
      [categoryTitle]: {
        ...previousSelections[categoryTitle],
        [itemName]: !previousSelections[categoryTitle][itemName],
      },
    }));
  };

  const handleCategoryWeightChange = (
    categoryTitle: string,
    event: ChangeEvent<HTMLInputElement>,
  ) => {
    const weight = Number(event.target.value);

    setCategoryWeights((previousWeights) => ({
      ...previousWeights,
      [categoryTitle]: weight,
    }));
  };

  const handleItemWeightChange = (
    categoryTitle: string,
    itemName: string,
    event: ChangeEvent<HTMLInputElement>,
  ) => {
    const weight = Number(event.target.value);

    setItemWeights((previousWeights) => ({
      ...previousWeights,
      [categoryTitle]: {
        ...previousWeights[categoryTitle],
        [itemName]: weight,
      },
    }));
  };

  return (
    <div className="page">
      <main className="container">
        <section className="hero">
          <p className="eyebrow">CommitMentIssues</p>
          <h1>CV and GitHub Repository Analyzer</h1>
          <p className="subtitle">
            Upload one or more CV files to extract useful information and later
            analyze linked GitHub repositories.
          </p>
        </section>

        <section className="card">
          <h2>Upload files</h2>
          <p className="card-description">
            Allowed file types: <strong>.txt</strong>, <strong>.docx</strong>,{" "}
            <strong>.pdf</strong>
          </p>

          <label className="upload-box" htmlFor="file-upload">
            <input
              id="file-upload"
              type="file"
              accept={acceptedFileTypes}
              multiple
              onChange={handleFileChange}
            />
            <span className="upload-box-title">Choose files</span>
            <span className="upload-box-text">
              Select multiple TXT, DOCX, or PDF files
            </span>
          </label>

          <div className="actions">
            <button className="primary-button" onClick={handleUpload}>
              Upload files
            </button>
          </div>

          {statusMessage && <p className="status-message">{statusMessage}</p>}

          <div className="files-section">
            <h3>Selected files</h3>

            {selectedFiles.length === 0 ? (
              <p className="empty-state">No files selected yet.</p>
            ) : (
              <ul className="file-list">
                {selectedFiles.map((file) => (
                  <li
                    key={`${file.name}-${file.size}-${file.lastModified}`}
                    className="file-item"
                  >
                    <div className="file-info">
                      <span className="file-name">{file.name}</span>
                      <span className="file-meta">
                        {(file.size / 1024).toFixed(2)} KB
                      </span>
                    </div>

                    <button
                      className="remove-button"
                      onClick={() => handleRemoveFile(file)}
                      type="button"
                    >
                      Remove
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>

          {uploadResult && (
            <div className="results-section">
              <h3>Scan results</h3>

              {uploadResult.scanned_files.length === 0 ? (
                <p className="empty-state">No GitHub links found.</p>
              ) : (
                <div className="results-list">
                  {uploadResult.scanned_files.map((fileResult) => (
                    <div key={fileResult.file_name} className="result-card">
                      <h4>{fileResult.file_name}</h4>

                      {fileResult.github_links.length === 0 ? (
                        <p className="empty-state">No GitHub links found.</p>
                      ) : (
                        <ul className="link-list">
                          {fileResult.github_links.map((link) => (
                            <li key={link}>
                              <a href={link} target="_blank" rel="noreferrer">
                                {link}
                              </a>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  ))}
                </div>
              )}

              <div className="unique-links-section">
                <h3>Unique GitHub links</h3>

                {uploadResult.unique_github_links.length === 0 ? (
                  <p className="empty-state">No GitHub links found.</p>
                ) : (
                  <ul className="link-list">
                    {uploadResult.unique_github_links.map((link) => (
                      <li key={link}>
                        <a href={link} target="_blank" rel="noreferrer">
                          {link}
                        </a>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          )}
        </section>

        <section className="card">
          <h2>Repository Analysis Sections</h2>
          <p className="card-description">
            Choose which repository metrics should be included in the analysis.
          </p>

          <div className="results-list">
            {ANALYSIS_CATEGORIES.map((category) => {
              const currentCategoryWeight = categoryWeights[category.title] ?? DEFAULT_WEIGHT;

              return (
                <div key={category.title} className="result-card">
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      gap: "1rem",
                      marginBottom: "1rem",
                    }}
                  >
                    <h3 style={{ margin: 0 }}>{category.title}</h3>

                    <input
                      id={`category-weight-${category.title}`}
                      type="range"
                      min="0"
                      max="10"
                      step="1"
                      value={currentCategoryWeight}
                      onChange={(event) =>
                        handleCategoryWeightChange(category.title, event)
                      }
                      style={{
                        width: "200px",
                        flexShrink: 0,
                      }}
                    />
                  </div>

                  <ul className="link-list">
                    {category.items.map((item) => {
                      const isChecked =
                        analysisSelections[category.title]?.[item] ?? false;
                      const currentItemWeight =
                        itemWeights[category.title]?.[item] ?? DEFAULT_WEIGHT;

                      return (
                        <li key={item}>
                          <div
                            style={{
                              display: "flex",
                              alignItems: "center",
                              gap: "0.75rem",
                              justifyContent: "space-between",
                              paddingBottom: "0.65rem",
                            }}
                          >
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
                                onChange={() =>
                                  handleAnalysisItemToggle(category.title, item)
                                }
                              />
                              <span>
                                {item} (not rdy)
                              </span>
                            </label>

                            <input
                              id={`item-weight-${category.title}-${item}`}
                              type="range"
                              min="0"
                              max="10"
                              step="1"
                              value={currentItemWeight}
                              onChange={(event) =>
                                handleItemWeightChange(
                                  category.title,
                                  item,
                                  event,
                                )
                              }
                              style={{
                                width: "110px",
                                flexShrink: 0,
                              }}
                            />
                          </div>
                        </li>
                      );
                    })}
                  </ul>
                </div>
              );
            })}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;