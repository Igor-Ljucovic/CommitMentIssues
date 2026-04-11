type SelectedFilesListProps = {
  selectedFiles: File[];
  onRemoveFile: (fileToRemove: File) => void;
};

function SelectedFilesList({
  selectedFiles,
  onRemoveFile,
}: SelectedFilesListProps) {
  return (
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
                onClick={() => onRemoveFile(file)}
                type="button"
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default SelectedFilesList;