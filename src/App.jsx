import { Route, Routes } from "react-router-dom";
import "./App.css";
import Main from "./pages/Main";
import Skanning from "./pages/Skanning";
import Completion from "./pages/Completion";

import data from "./products.json";
import { CardsContext } from "./contexts/CardsContext";
import { useEffect, useState } from "react";
import { CompletedContext } from "./contexts/CompletedContext";

function App() {
  const [completedCards, setCompletedCards] = useState([]);
  const [isCompleted, setCompleted] = useState(false);

  useEffect(() => {
    const jsonData = data.skus.map((sku) => sku.id);

    const isAllIdsMatched = jsonData.every((id) => completedCards.includes(id));

    if (isAllIdsMatched) {
      setCompleted(true);
    }
  }, [completedCards]);

  return (
    <div className="app">
      <CardsContext.Provider value={{ completedCards, setCompletedCards }}>
        <CompletedContext.Provider value={{ isCompleted }}>
          <Routes>
            <Route path="/" element={<Main data={data} />} />
            <Route
              path="/scan"
              element={<Skanning typeBox={data.recommended_cartontype} />}
            />
            <Route path="/completetion" element={<Completion />} />
          </Routes>
        </CompletedContext.Provider>
      </CardsContext.Provider>
    </div>
  );
}

export default App;
