import { useMemo, useState } from "react";
import type { ChangeEvent } from "react";
import "./App.css";
import FileUploadSection from "./components/FileUploadSection";
import RepositoryAnalysisSection from "./components/RepositoryAnalysisSection";
import ScanResultsSection from "./components/ScanResultsSection";
import SelectedFilesList from "./components/SelectedFilesList";
import type {
  AnalysisSelectionState,
  CategoryWeightsState,
  ItemWeightsState,
  MetricParametersState,
  MetricParameterValue,
  UploadResponse,
} from "./types";
import {
  createInitialAnalysisSelections,
  createInitialCategoryWeights,
  createInitialItemWeights,
  createInitialMetricParameters,
} from "./utils/initialState";

const ALLOWED_EXTENSIONS = [".txt", ".docx", ".pdf"];

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

  const getSelectedAnalysisMetrics = () => {
    const selected: string[] = [];

    Object.entries(analysisSelections).forEach(([category, items]) => {
      Object.entries(items).forEach(([metric, isChecked]) => {
        if (isChecked) {
          const categoryWeight = categoryWeights[category];
          const metricWeight = itemWeights[category]?.[metric];
          const metricConfig = metricParameters[category]?.[metric];

          selected.push(
            `${category} (category weight: ${categoryWeight}) -> ${metric} (metric weight: ${metricWeight})`,
          );

          if (metricConfig) {
            Object.entries(metricConfig).forEach(
              ([parameterKey, parameterValue]) => {
                selected.push(
                  `   ${parameterKey}: ${JSON.stringify(parameterValue)}`,
                );
              },
            );
          }
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

    console.log("All metric parameter values:");
    Object.entries(metricParameters).forEach(([category, items]) => {
      Object.entries(items).forEach(([item, parameters]) => {
        Object.entries(parameters).forEach(([parameterKey, parameterValue]) => {
          console.log(
            `${category} -> ${item} -> ${parameterKey}:`,
            parameterValue,
          );
        });
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
            onUpload={handleUpload}
          />

          <SelectedFilesList
            selectedFiles={selectedFiles}
            onRemoveFile={handleRemoveFile}
          />

          <ScanResultsSection uploadResult={uploadResult} />
        </section>

        <RepositoryAnalysisSection
          analysisSelections={analysisSelections}
          categoryWeights={categoryWeights}
          itemWeights={itemWeights}
          metricParameters={metricParameters}
          onAnalysisItemToggle={handleAnalysisItemToggle}
          onCategoryWeightChange={handleCategoryWeightChange}
          onItemWeightChange={handleItemWeightChange}
          onMetricParameterChange={handleMetricParameterChange}
        />
      </main>
    </div>
  );
}

export default App;