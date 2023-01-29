import { Navigate, Route, Routes } from "react-router-dom";
import { TwoGradient } from "./TwoGradient";

export const TwoGradientRoutes = () => {
  return (
    <Routes>
      <Route path="" element={<TwoGradient />} />
      <Route path="*" element={<Navigate to="." />} />
    </Routes>
  );
};
