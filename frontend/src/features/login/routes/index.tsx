import { Route, Routes } from "react-router-dom";

import { Login } from "./Login";

export const AuthRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
    </Routes>
  );
};

export { Login } from "./Login";
