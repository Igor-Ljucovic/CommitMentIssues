import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import HomePage from "./components/pages/HomePage";
import AnalysisPage from "./components/pages/AnalysisPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/analysis" element={<AnalysisPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;