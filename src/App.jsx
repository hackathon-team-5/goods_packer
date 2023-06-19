import { Route, Routes } from "react-router-dom";
import "./App.css";
import Main from "./pages/Main";
import Skanning from "./pages/Skanning";
import Completion from "./pages/Completion";

import data from "./products.json";

function App() {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={<Main data={data} />} />
        <Route
          path="/scan"
          element={<Skanning typeBox={data.recommended_cartontype} />}
        />
        <Route path="/completetion" element={<Completion />} />
      </Routes>
    </div>
  );
}

export default App;
