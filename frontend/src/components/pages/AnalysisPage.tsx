import { useMemo, useState } from "react";
import type { ChangeEvent } from "react";
import "../../App.css";
import FileUploadSection from "../../components/FileUploadSection";
import RepositoryAnalysisSection from "../../components/RepositoryAnalysisSection";
import SelectedFilesList from "../../components/SelectedFilesList";
import type {
  AnalysisSelectionState,
  ItemWeightsState,
  MetricParametersState,
  MetricParameterValue,
  UploadResponse,
} from "../../types";
import {
  createInitialAnalysisSelections,
  createInitialItemWeights,
  createInitialMetricParameters,
} from "../../utils/initialState";
import { ANALYSIS_CATEGORIES } from "../../data/analysisCategories";

const ALLOWED_EXTENSIONS = [".txt", ".docx", ".pdf"];

type AnalysisResponse = {
  files: {
    file_id: number | null;
    file_name: string;
    repositories: {
      repository_url: string;
      metrics: {
        metric_key: string;
        display_name: string;
        value: string | number | null;
        status: string;
        message?: string | null;
      }[];
    }[];
  }[];
  warnings: string[];
};

function App() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [statusMessage, setStatusMessage] = useState<string>("");
  const [analysisSelections, setAnalysisSelections] =
    useState<AnalysisSelectionState>(createInitialAnalysisSelections);
  const [itemWeights, setItemWeights] =
    useState<ItemWeightsState>(createInitialItemWeights);
  const [metricParameters, setMetricParameters] =
    useState<MetricParametersState>(createInitialMetricParameters);

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

  const isPercentageParameter = (
    categoryName: string,
    itemName: string,
    parameterKey: string,
  ): boolean => {
    const category = ANALYSIS_CATEGORIES.find(
      (c) => c.title === categoryName,
    );

    if (!category) return false;

    const item = category.items.find((i) => i.name === itemName);
    if (!item) return false;

    const parameter = item.parameters?.find((p) => p.key === parameterKey);

    return parameter?.type === "percentage-range";
  };

  const convertPercentageValue = (value: string): string => {
    if (!value.trim()) return value;

    const num = Number(value);
    if (Number.isNaN(num)) return value;

    return String(num / 100);
  };

  const buildAnalysisPayload = (
    uploadResult: UploadResponse,
  ): Record<string, unknown> => {
    const payload: Record<string, unknown> = {
      files: uploadResult.files,
    };

    Object.entries(analysisSelections).forEach(([categoryName, items]) => {
      const selectedSubcategories: Record<string, unknown> = {};

      Object.entries(items).forEach(([itemName, isChecked]) => {
        if (!isChecked) {
          return;
        }

        const cleanItemName = itemName
          .replace(/\s*⭐/g, "")
          .replace(/\s*\(not rdy\)/g, "")
          .trim();

        const subcategoryPayload: Record<string, unknown> = {
          weight: itemWeights[categoryName]?.[itemName] ?? 5,
        };

        const parameters = metricParameters[categoryName]?.[itemName];

        if (parameters) {
          Object.entries(parameters).forEach(([parameterKey, parameterValue]) => {
            const cleanedParameterValue = Object.fromEntries(
              Object.entries(parameterValue)
                .filter(([, value]) => value !== "" && value !== undefined)
                .map(([valueKey, rawValue]) => {
                  if (
                    isPercentageParameter(categoryName, itemName, parameterKey) &&
                    typeof rawValue === "string"
                  ) {
                    return [valueKey, convertPercentageValue(rawValue)];
                  }

                  return [valueKey, rawValue];
                }),
            );

            if (Object.keys(cleanedParameterValue).length > 0) {
              subcategoryPayload[parameterKey] = cleanedParameterValue;
            }
          });
        }

        selectedSubcategories[cleanItemName] = subcategoryPayload;
      });

      if (Object.keys(selectedSubcategories).length > 0) {
        payload[categoryName] = {
          subcategories: selectedSubcategories,
        };
      }
    });

    return payload;
  };

  const handleUpload = async (): Promise<UploadResponse> => {
    if (selectedFiles.length === 0) {
      throw new Error("Please select at least one file before uploading.");
    }

    const formData = new FormData();

    selectedFiles.forEach((file) => {
      formData.append("files", file);
    });

    const uploadRequestPreview = selectedFiles.map((file) => ({
      name: file.name,
      size: file.size,
      type: file.type,
    }));

    console.log("FormData payload sent to /uploads:");
    console.log(JSON.stringify({ files: uploadRequestPreview }, null, 2));

    const response = await fetch("http://localhost:8000/uploads", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Upload failed.");
    }

    const result: UploadResponse = await response.json();

    console.log("/uploads backend response:");
    console.log(JSON.stringify(result, null, 2));

    return result;
  };

  const handleAnalysis = async (
    uploadResult: UploadResponse,
  ): Promise<AnalysisResponse> => {
    if (uploadResult.files.length === 0) {
      throw new Error("No uploaded files are available for analysis.");
    }

    const payload = buildAnalysisPayload(uploadResult);

    console.log("JSON payload sent to /analysis:");
    console.log(JSON.stringify(payload, null, 2));

    const response = await fetch("http://localhost:8000/analysis", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error("Analysis failed.");
    }

    const result: AnalysisResponse = await response.json();

    console.log("/analysis backend response:");
    console.log(JSON.stringify(result, null, 2));

    return result;
  };

  const handleAnalyzeRepositories = async () => {
    if (selectedFiles.length === 0) {
      setStatusMessage("Please select at least one file before analyzing.");
      return;
    }

    try {
      setStatusMessage("Uploading files and analyzing repositories...");

      const uploadResult = await handleUpload();
      const analysisResult = await handleAnalysis(uploadResult);

      const warningText =
        analysisResult.warnings.length > 0
          ? ` Warnings: ${analysisResult.warnings.join(" ")}`
          : "";

      const totalRepositoryCount = analysisResult.files.reduce(
        (sum, file) => sum + file.repositories.length,
        0,
      );

      setStatusMessage(
        `Upload successful. Accepted ${uploadResult.accepted_files} of ${uploadResult.total_files} file(s). Analysis completed for ${totalRepositoryCount} repositor${
          totalRepositoryCount === 1 ? "y" : "ies"
        }.${warningText}`,
      );
    } catch (error) {
      console.error(error);

      if (error instanceof Error) {
        setStatusMessage(error.message);
      } else {
        setStatusMessage(
          "Something went wrong while uploading files and analyzing repositories.",
        );
      }
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

  const handleMetricParameterChange = (
    categoryTitle: string,
    itemName: string,
    parameterKey: string,
    valueKey: keyof MetricParameterValue,
    value: string,
  ) => {
    setMetricParameters((previousValues) => ({
      ...previousValues,
      [categoryTitle]: {
        ...previousValues[categoryTitle],
        [itemName]: {
          ...previousValues[categoryTitle][itemName],
          [parameterKey]: {
            ...previousValues[categoryTitle][itemName][parameterKey],
            [valueKey]: value,
          },
        },
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
          <FileUploadSection
            acceptedFileTypes={acceptedFileTypes}
            statusMessage={statusMessage}
            onFileChange={handleFileChange}
          />

          <SelectedFilesList
            selectedFiles={selectedFiles}
            onRemoveFile={handleRemoveFile}
          />
        </section>

        <RepositoryAnalysisSection
          analysisSelections={analysisSelections}
          itemWeights={itemWeights}
          metricParameters={metricParameters}
          onAnalysisItemToggle={handleAnalysisItemToggle}
          onItemWeightChange={handleItemWeightChange}
          onMetricParameterChange={handleMetricParameterChange}
        />

        <div
          className="actions"
          style={{
            marginTop: "30px",
            display: "flex",
            justifyContent: "center",
          }}
        >
          <button
            className="primary-button"
            onClick={handleAnalyzeRepositories}
          >
            Analyze GitHub Repositories
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;