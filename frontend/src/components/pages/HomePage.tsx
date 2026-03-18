type HomePageProps = {
  onGetStarted?: () => void;
};

function HomePage({ onGetStarted }: HomePageProps) {
  return (
    <section className="card" style={{ marginBottom: "28px" }}>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "1.5rem",
        }}
      >
        <div>
          <p className="eyebrow">CommitMentIssues</p>

          <h1
            style={{
              margin: "0 0 12px 0",
              fontSize: "2.5rem",
              lineHeight: 1.1,
            }}
          >
            GitHub repository analysis built to make technical recruiters&apos;
            lives easier
          </h1>

          <p
            className="subtitle"
            style={{
              maxWidth: "820px",
              marginBottom: "0.9rem",
            }}
          >
            CommitMentIssues helps recruiters and hiring teams evaluate GitHub
            repositories faster, more consistently, and with way less manual
            effort. Instead of opening candidate repositories one by one and
            trying to judge them from memory, you can define what matters,
            assign weights to the metrics, and analyze repositories using a more
            structured approach.
          </p>

          <p
            className="subtitle"
            style={{
              maxWidth: "820px",
              margin: 0,
            }}
          >
            It works both for individual repository analysis and for
            higher-volume company workflows where recruiters upload multiple CV,
            PDF, DOCX, or TXT files, extract GitHub links from them, and use
            those links as the starting point for candidate repository analysis.
          </p>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
            gap: "1rem",
          }}
        >
          <div className="result-card">
            <h3 style={{ marginTop: 0, marginBottom: "0.65rem" }}>
              For personal use
            </h3>
            <p style={{ margin: 0, lineHeight: 1.6 }}>
              Analyze a single repository when you want a focused review of one
              candidate, one project, or even your own GitHub repo.
            </p>
          </div>

          <div className="result-card">
            <h3 style={{ marginTop: 0, marginBottom: "0.65rem" }}>
              For company use
            </h3>
            <p style={{ margin: 0, lineHeight: 1.6 }}>
              Upload candidate CVs and other documents in bulk, extract GitHub
              links automatically, and prepare a more scalable screening process
              for technical recruitment.
            </p>
          </div>

          <div className="result-card">
            <h3 style={{ marginTop: 0, marginBottom: "0.65rem" }}>
              Configurable scoring
            </h3>
            <p style={{ margin: 0, lineHeight: 1.6 }}>
              Choose which metrics matter, set weights for categories and
              subcategories, and tailor the analysis to different roles,
              expectations, and hiring standards.
            </p>
          </div>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
            gap: "1rem",
          }}
        >
          <div
            style={{
              border: "1px solid #d6d6d6",
              borderRadius: "12px",
              padding: "1rem 1.1rem",
              backgroundColor: "#fafafa",
            }}
          >
            <h3 style={{ marginTop: 0, marginBottom: "0.8rem" }}>
              Basic repository signals
            </h3>

            <p style={{ marginTop: 0, lineHeight: 1.65 }}>
              CommitMentIssues supports straightforward numeric and metadata
              checks such as repository creation date, last commit date, total
              commit count, average commits per month, total lines of code,
              total files, contributors, pull requests, forks, stars, and
              technology stack size.
            </p>

            <p style={{ marginBottom: 0, lineHeight: 1.65 }}>
              These are useful for getting a fast first impression and filtering
              repositories based on activity, size, recency, popularity, and
              collaboration patterns.
            </p>
          </div>

          <div
            style={{
              border: "1px solid #d6d6d6",
              borderRadius: "12px",
              padding: "1rem 1.1rem",
              backgroundColor: "#fafafa",
            }}
          >
            <h3 style={{ marginTop: 0, marginBottom: "0.8rem" }}>
              More sophisticated quality signals
            </h3>

            <p style={{ marginTop: 0, lineHeight: 1.65 }}>
              Beyond raw counts, the platform is designed to support more
              advanced quality-oriented metrics such as commit naming
              consistency, commit message and code change alignment, code
              duplication estimation, naming consistency across files and code
              elements, file architecture quality, estimated test coverage, and
              AI-generated code estimation.
            </p>

            <p style={{ marginBottom: 0, lineHeight: 1.65 }}>
              This is the part that makes the project especially useful for
              technical recruiters, because it moves the analysis closer to
              actual engineering quality instead of stopping at vanity metrics.
            </p>
          </div>
        </div>

        <div className="result-card">
          <h3 style={{ marginTop: 0, marginBottom: "0.8rem" }}>
            Why this helps recruiters
          </h3>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
              gap: "0.85rem",
            }}
          >
            <div>
              <strong>Faster screening</strong>
              <p style={{ margin: "0.35rem 0 0 0", lineHeight: 1.6 }}>
                Reduce the time spent manually opening repositories and checking
                the same things over and over again.
              </p>
            </div>

            <div>
              <strong>More consistency</strong>
              <p style={{ margin: "0.35rem 0 0 0", lineHeight: 1.6 }}>
                Apply the same analysis logic across candidates instead of
                relying only on subjective first impressions.
              </p>
            </div>

            <div>
              <strong>Role-specific evaluation</strong>
              <p style={{ margin: "0.35rem 0 0 0", lineHeight: 1.6 }}>
                Change weights and acceptable ranges depending on whether the
                role is backend, frontend, full-stack, QA, or something else.
              </p>
            </div>

            <div>
              <strong>Better recruiter-engineer alignment</strong>
              <p style={{ margin: "0.35rem 0 0 0", lineHeight: 1.6 }}>
                Turn vague repository review into a more transparent framework
                that technical and non-technical stakeholders can both discuss.
              </p>
            </div>
          </div>
        </div>

        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: "0.9rem",
            alignItems: "center",
          }}
        >
          <button
            type="button"
            className="primary-button"
            onClick={onGetStarted}
          >
            Start analyzing
          </button>

          <span
            style={{
              color: "#4b5563",
              fontSize: "0.95rem",
            }}
          >
            Built for recruiter-friendly GitHub analysis, from single-repo
            reviews to multi-candidate document workflows.
          </span>
        </div>
      </div>
    </section>
  );
}

export default HomePage;