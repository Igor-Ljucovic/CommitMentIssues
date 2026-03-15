import type { ChangeEvent } from "react";

type FileUploadSectionProps = {
  acceptedFileTypes: string;
  statusMessage: string;
  onFileChange: (event: ChangeEvent<HTMLInputElement>) => void;
  onUpload: () => void;
};

function FileUploadSection({
  acceptedFileTypes,
  statusMessage,
  onFileChange,
  onUpload,
}: FileUploadSectionProps) {
  return (
    <>
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
          onChange={onFileChange}
        />
        <span className="upload-box-title">Choose files</span>
        <span className="upload-box-text">
          Select multiple TXT, DOCX, or PDF files
        </span>
      </label>

      <div className="actions">
        <button className="primary-button" onClick={onUpload}>
          Upload files
        </button>
      </div>

      {statusMessage && <p className="status-message">{statusMessage}</p>}
    </>
  );
}

export default FileUploadSection;