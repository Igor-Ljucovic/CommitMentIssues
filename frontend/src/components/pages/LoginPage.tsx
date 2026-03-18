import { useState } from "react";
import { useNavigate } from "react-router-dom";

function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [statusMessage, setStatusMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit: React.SubmitEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault();

    if (!email.trim() || !password) {
        setStatusMessage("Please enter both email and password.");
        return;
    }

    try {
        setIsLoading(true);
        setStatusMessage("");

        const payload = {
        email: email.trim(),
        password,
        };

        const logPayload = {
        ...payload,
        password: "thePasswordIsHiddenForSecurityReasons",
        };

        console.log("Login request payload:");
        console.log(JSON.stringify(logPayload, null, 2));

        const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
        });

        if (!response.ok) {
        throw new Error("Login failed.");
        }

        const data = await response.json();
        console.log("Login success:", data);

        setStatusMessage("Login successful!");

        navigate("/analysis");
    } catch (error) {
        console.error(error);
        setStatusMessage("Login failed. Please try again.");
    } finally {
        setIsLoading(false);
    }
  };

  return (
    <main
      style={{
        minHeight: "calc(100vh - 150px)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "32px 20px",
        boxSizing: "border-box",
      }}
    >
      <section
        className="card"
        style={{
          width: "100%",
          maxWidth: "460px",
          padding: "32px",
        }}
      >
        <div style={{ marginBottom: "24px", textAlign: "center" }}>
          <p className="eyebrow" style={{ marginBottom: "10px" }}>
            CommitMentIssues
          </p>

          <h1
            style={{
              margin: "0 0 10px 0",
              fontSize: "2rem",
              lineHeight: 1.15,
            }}
          >
            Log in
          </h1>

          <p className="card-description" style={{ margin: 0 }}>
            Sign in to continue to your CV and GitHub repository analysis
            dashboard.
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "18px",
            }}
          >
            <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
              <label
                htmlFor="email"
                style={{ fontWeight: 600, fontSize: "0.95rem" }}
              >
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                autoComplete="email"
                style={{
                  padding: "12px 14px",
                  borderRadius: "10px",
                  border: "1px solid #cbd5e1",
                  fontSize: "0.95rem",
                  outline: "none",
                  width: "100%",
                  boxSizing: "border-box",
                }}
              />
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
              <label
                htmlFor="password"
                style={{ fontWeight: 600, fontSize: "0.95rem" }}
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                autoComplete="current-password"
                style={{
                  padding: "12px 14px",
                  borderRadius: "10px",
                  border: "1px solid #cbd5e1",
                  fontSize: "0.95rem",
                  outline: "none",
                  width: "100%",
                  boxSizing: "border-box",
                }}
              />
            </div>

            <div
              style={{
                display: "flex",
                justifyContent: "flex-end",
                marginTop: "-4px",
              }}
            >
              <button
                type="button"
                style={{
                  border: "none",
                  background: "transparent",
                  color: "#4f46e5",
                  cursor: "pointer",
                  fontSize: "0.9rem",
                  padding: 0,
                }}
                onClick={() => {
                  console.log("Forgot password clicked");
                }}
              >
                Forgot password?
              </button>
            </div>

            <div className="actions" style={{ marginTop: "4px" }}>
              <button
                className="primary-button"
                type="submit"
                disabled={isLoading}
                style={{ width: "100%" }}
              >
                {isLoading ? "Logging in..." : "Log in"}
              </button>
            </div>

            {statusMessage ? (
              <p
                className="status-message"
                style={{
                  margin: 0,
                  textAlign: "center",
                }}
              >
                {statusMessage}
              </p>
            ) : null}

            <div
              style={{
                textAlign: "center",
                fontSize: "0.95rem",
                color: "#4b5563",
                marginTop: "8px",
              }}
            >
              Don&apos;t have an account?{" "}
              <button
                type="button"
                onClick={() => navigate("/signup")}
                style={{
                  border: "none",
                  background: "transparent",
                  color: "#4f46e5",
                  cursor: "pointer",
                  fontWeight: 600,
                  padding: 0,
                }}
              >
                Sign up
              </button>
            </div>
          </div>
        </form>
      </section>
    </main>
  );
}

export default LoginPage;