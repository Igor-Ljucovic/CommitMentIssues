import { useMemo, useState } from "react";
import type { ChangeEvent } from "react";
import "./App.css";

const ALLOWED_EXTENSIONS = [".txt", ".docx", ".pdf"];

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

function App() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [statusMessage, setStatusMessage] = useState<string>("");
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null);

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
      </main>
    </div>
  );
}

export default App;