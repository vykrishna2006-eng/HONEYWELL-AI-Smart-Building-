import { Routes, Route } from "react-router-dom";

import Dashboard       from "./pages/Dashboard";
import Predictions     from "./pages/Predictions";
import Analytics       from "./pages/Analytics";
import Recommendations from "./pages/Recommendations";
import Simulation      from "./pages/Simulation";
import Settings        from "./pages/Settings";

function App() {
  return (
    <Routes>
      <Route path="/"               element={<Dashboard />}       />
      <Route path="/predictions"    element={<Predictions />}     />
      <Route path="/analytics"      element={<Analytics />}       />
      <Route path="/recommendations" element={<Recommendations />} />
      <Route path="/simulation"     element={<Simulation />}      />
      <Route path="/settings"       element={<Settings />}        />
    </Routes>
  );
}

export default App;
