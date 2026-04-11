import { useState } from "react";
import { useNavigate } from "react-router-dom";

function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [statusMessage, setStatusMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  const extractBackendErrorMessage = (data: unknown): string => {
    if (
      typeof data === "object" &&
      data !== null &&
      "detail" in data &&
      Array.isArray((data as { detail: unknown[] }).detail) &&
      (data as { detail: unknown[] }).detail.length > 0
    ) {
      const firstError = (data as { detail: unknown[] }).detail[0];

      if (
        typeof firstError === "object" &&
        firstError !== null &&
        "msg" in firstError &&
        typeof (firstError as { msg: unknown }).msg === "string"
      ) {
        const fullMessage = (firstError as { msg: string }).msg;
        const commaIndex = fullMessage.indexOf(",");

        if (commaIndex !== -1) {
          return fullMessage.slice(commaIndex + 1).trim();
        }

        return fullMessage.trim();
      }
    }

    return "Signup failed.";
  };

  const handleSubmit: React.SubmitEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault();

    if (!email.trim() || !password || !confirmPassword) {
      setStatusMessage("Please fill in all fields.");
      return;
    }

    if (password !== confirmPassword) {
      setStatusMessage("Passwords do not match.");
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

      console.log("Signup request payload:");
      console.log(JSON.stringify(logPayload, null, 2));

       const response = await fetch("http://localhost:8000/auth/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      console.log("Signup response status:", response.status);
      console.log("Signup response data:", data);

      if (!response.ok) {
        throw new Error(extractBackendErrorMessage(data));
      }

      console.log("Signup success:", data);

      setStatusMessage("Account created successfully!");

      navigate("/");
    } catch (error) {
      console.error(error);

      if (error instanceof Error) {
        setStatusMessage(error.message);
      } else {
        setStatusMessage("Signup failed. Please try again.");
      }
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
            Sign up
          </h1>

          <p className="card-description" style={{ margin: 0 }}>
            Create an account to access your CV and GitHub repository analysis
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
                placeholder="Create a password"
                autoComplete="new-password"
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
                htmlFor="confirmPassword"
                style={{ fontWeight: 600, fontSize: "0.95rem" }}
              >
                Confirm password
              </label>
              <input
                id="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm your password"
                autoComplete="new-password"
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

            <div className="actions" style={{ marginTop: "4px" }}>
              <button
                className="primary-button"
                type="submit"
                disabled={isLoading}
                style={{ width: "100%" }}
              >
                {isLoading ? "Signing up..." : "Sign up"}
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
              Already have an account?{" "}
              <button
                type="button"
                onClick={() => navigate("/login")}
                style={{
                  border: "none",
                  background: "transparent",
                  color: "#4f46e5",
                  cursor: "pointer",
                  fontWeight: 600,
                  padding: 0,
                }}
              >
                Log in
              </button>
            </div>
          </div>
        </form>
      </section>
    </main>
  );
}

export default SignupPage;