import type { UploadResponse } from "../types";

type ScanResultsSectionProps = {
  uploadResult: UploadResponse | null;
};

function ScanResultsSection({ uploadResult }: ScanResultsSectionProps) {
  if (!uploadResult) {
    return null;
  }

  return (
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
  );
}

export default ScanResultsSection;