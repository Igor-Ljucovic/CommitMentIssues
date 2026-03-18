import { Link, NavLink } from "react-router-dom";

function Navbar() {
  const navLinkStyle = ({ isActive }: { isActive: boolean }) => ({
    color: isActive ? "#111827" : "#4b5563",
    textDecoration: "none",
    fontWeight: isActive ? 700 : 500,
    transition: "color 0.2s ease",
  });

  return (
    <header className="navbar">
      <div className="navbar__left">
        <Link to="/" className="navbar__brand">
          CommitMentIssues
        </Link>

        <nav className="navbar__nav">
          <NavLink to="/analysis" style={navLinkStyle}>
            Analysis
          </NavLink>
        </nav>
      </div>

      <div className="navbar__right">
        <Link to="/login" className="navbar__login">
          Log in
        </Link>

        <Link to="/signup" className="navbar__signup">
          Sign up
        </Link>
      </div>
    </header>
  );
}

export default Navbar;