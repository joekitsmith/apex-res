import { Navigate } from "react-router-dom";
import { lazyImport } from "../utils/lazyImport";

const { AuthRoutes } = lazyImport(
  () => import("../features/login"),
  "AuthRoutes"
);

export const publicRoutes = [
  {
    path: "/",
    element: <Navigate replace to="/login" />,
  },
  {
    path: "/login",
    element: <AuthRoutes />,
  }
];
