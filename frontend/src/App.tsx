import { useMemo, useState } from "react";
import type { ChangeEvent } from "react";
import "./App.css";
import FileUploadSection from "./components/FileUploadSection";
import RepositoryAnalysisSection from "./components/RepositoryAnalysisSection";
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

  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      setStatusMessage("Please select at least one file before uploading.");
      return;
    }

    const payload: Record<string, unknown> = {
      files: selectedFiles.map((file) => ({
        name: file.name,
        size: file.size,
        type: file.type,
      })),
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
              Object.entries(parameterValue).filter(
                ([, value]) => value !== "" && value !== undefined,
              ),
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
          weight: categoryWeights[categoryName] ?? 5,
          subcategories: selectedSubcategories,
        };
      }
    });

    console.log("JSON payload sent to backend:");
    console.log(JSON.stringify(payload, null, 2));

    try {
      setStatusMessage("Uploading files...");

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

      console.log("Backend response:");
      console.log(JSON.stringify(result, null, 2));

      setStatusMessage(
        `Upload successful. Accepted ${result.accepted_files} of ${result.total_files} file(s).`,
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
          />

          <SelectedFilesList
            selectedFiles={selectedFiles}
            onRemoveFile={handleRemoveFile}
          />
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
        <div
          className="actions"
          style={{
            marginTop: "30px",
            display: "flex",
            justifyContent: "center",
          }}
        >
          <button className="primary-button" onClick={handleUpload}>
            Analyze GitHub Repositories
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;