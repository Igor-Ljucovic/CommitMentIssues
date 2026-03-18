import { Link } from "react-router-dom";

type HomePageProps = {
  onGetStarted?: () => void;
};

function HomePage({ onGetStarted }: HomePageProps) {
  const handleGetStarted = () => {
    onGetStarted?.();
  };

  return (
    <div className="page">
      <main className="container">
        <section
          className="card"
          style={{
            padding: "48px 32px",
            marginBottom: "28px",
          }}
        >
          <div
            style={{
              maxWidth: "760px",
              margin: "0 auto",
              textAlign: "center",
            }}
          >
            <p className="eyebrow">CommitMentIssues</p>

            <h1
              style={{
                margin: "0 0 16px 0",
                fontSize: "3rem",
                lineHeight: 1.08,
                letterSpacing: "-0.03em",
              }}
            >
              GitHub repository analysis for technical hiring
            </h1>

            <p
              className="subtitle"
              style={{
                maxWidth: "700px",
                margin: "0 auto 24px auto",
                fontSize: "1.1rem",
                lineHeight: 1.7,
              }}
            >
              Evaluate candidate repositories faster with structured metrics,
              configurable scoring, and a workflow designed for technical
              recruiters and hiring teams.
            </p>

            <div
              style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                flexWrap: "wrap",
                gap: "12px",
                marginBottom: "18px",
              }}
            >
              <Link
                to="/analysis"
                className="primary-button"
                onClick={handleGetStarted}
                style={{ textDecoration: "none" }}
              >
                Start analyzing
              </Link>

              <a
                href="#how-it-works"
                className="secondary-button"
                style={{
                  textDecoration: "none",
                  display: "inline-flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                Learn more
              </a>
            </div>

            <p
              style={{
                margin: 0,
                color: "#4b5563",
                fontSize: "0.95rem",
                lineHeight: 1.6,
              }}
            >
              Supports both single-repository analysis for personal use and bulk
              CV/PDF/DOCX/TXT upload workflows for company-side candidate
              screening.
            </p>
          </div>
        </section>

        <section
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
            gap: "16px",
            marginBottom: "28px",
          }}
        >
          <div className="result-card">
            <h3 style={{ marginTop: 0, marginBottom: "10px" }}>
              Single repository analysis
            </h3>
            <p style={{ margin: 0, lineHeight: 1.65 }}>
              Review one GitHub repository at a time for personal use, focused
              candidate evaluation, or self-assessment.
            </p>
          </div>

          <div className="result-card">
            <h3 style={{ marginTop: 0, marginBottom: "10px" }}>
              Bulk candidate workflows
            </h3>
            <p style={{ margin: 0, lineHeight: 1.65 }}>
              Upload multiple CV and document files, extract GitHub links, and
              prepare repositories for large-scale technical screening.
            </p>
          </div>

          <div className="result-card">
            <h3 style={{ marginTop: 0, marginBottom: "10px" }}>
              Configurable scoring
            </h3>
            <p style={{ margin: 0, lineHeight: 1.65 }}>
              Select the metrics that matter, assign weights, and adapt the
              analysis to different hiring goals and engineering roles.
            </p>
          </div>
        </section>

        <section
          id="how-it-works"
          className="card"
          style={{
            marginBottom: "28px",
            padding: "28px",
          }}
        >
          <h2 style={{ marginTop: 0, marginBottom: "18px" }}>How it works</h2>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
              gap: "16px",
            }}
          >
            <div>
              <strong>1. Upload repository links or candidate files</strong>
              <p style={{ margin: "8px 0 0 0", lineHeight: 1.65 }}>
                Use a single repository for focused analysis or upload multiple
                CV, PDF, DOCX, and TXT files for company workflows.
              </p>
            </div>

            <div>
              <strong>2. Configure the evaluation criteria</strong>
              <p style={{ margin: "8px 0 0 0", lineHeight: 1.65 }}>
                Enable the metrics you care about and assign weights based on
                role expectations and hiring priorities.
              </p>
            </div>

            <div>
              <strong>3. Analyze repositories more consistently</strong>
              <p style={{ margin: "8px 0 0 0", lineHeight: 1.65 }}>
                Combine simple repository signals with deeper code-quality
                indicators in a more structured screening process.
              </p>
            </div>
          </div>
        </section>

        <section
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
            gap: "16px",
            marginBottom: "28px",
          }}
        >
          <div className="card" style={{ padding: "24px" }}>
            <h2 style={{ marginTop: 0, marginBottom: "14px" }}>
              Basic repository signals
            </h2>
            <p style={{ margin: 0, lineHeight: 1.7 }}>
              Measure concrete repository metadata such as repository age, total
              commit count, last commit date, contributor count, pull requests,
              forks, stars, total files, lines of code, and technologies used.
            </p>
          </div>

          <div className="card" style={{ padding: "24px" }}>
            <h2 style={{ marginTop: 0, marginBottom: "14px" }}>
              Advanced quality signals
            </h2>
            <p style={{ margin: 0, lineHeight: 1.7 }}>
              Go beyond vanity metrics with indicators such as commit naming
              consistency, commit-message-to-code alignment, code duplication,
              file architecture quality, naming consistency, and estimated test
              coverage.
            </p>
          </div>
        </section>

        <section className="card" style={{ padding: "28px", marginBottom: "28px" }}>
          <h2 style={{ marginTop: 0, marginBottom: "18px" }}>
            Why this helps technical recruiters
          </h2>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
              gap: "16px",
            }}
          >
            <div>
              <strong>Faster screening</strong>
              <p style={{ margin: "8px 0 0 0", lineHeight: 1.65 }}>
                Spend less time manually opening repositories and checking the
                same signals candidate by candidate.
              </p>
            </div>

            <div>
              <strong>More consistency</strong>
              <p style={{ margin: "8px 0 0 0", lineHeight: 1.65 }}>
                Apply a repeatable framework instead of relying only on
                subjective first impressions.
              </p>
            </div>

            <div>
              <strong>Role-specific evaluation</strong>
              <p style={{ margin: "8px 0 0 0", lineHeight: 1.65 }}>
                Adjust metric weights and criteria for backend, frontend,
                full-stack, QA, or other technical roles.
              </p>
            </div>

            <div>
              <strong>Better hiring discussions</strong>
              <p style={{ margin: "8px 0 0 0", lineHeight: 1.65 }}>
                Make repository review easier to explain and compare across
                recruiters, engineers, and hiring managers.
              </p>
            </div>
          </div>
        </section>

        <section
          className="card"
          style={{
            padding: "32px",
            textAlign: "center",
          }}
        >
          <h2 style={{ marginTop: 0, marginBottom: "12px" }}>
            Ready to analyze candidate repositories?
          </h2>

          <p
            style={{
              maxWidth: "640px",
              margin: "0 auto 20px auto",
              color: "#4b5563",
              lineHeight: 1.7,
            }}
          >
            Start with a single repository or upload multiple candidate files
            and build a more structured technical screening workflow.
          </p>

          <Link
            to="/analysis"
            className="primary-button"
            onClick={handleGetStarted}
            style={{ textDecoration: "none" }}
          >
            Go to analysis
          </Link>
        </section>
      </main>
    </div>
  );
}

export default HomePage;