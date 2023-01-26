import { Suspense } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { MainLayout } from "../components/Layout";
import { lazyImport } from "../utils/lazyImport";

// const { Playlists } = lazyImport();

const App = () => {
  return (
    <MainLayout header="Apex Res">
      <Suspense
        fallback={
          <div className="h-full w-full flex items-center justify-center">
            Loading...
          </div>
        }
      >
        <Outlet />
      </Suspense>
    </MainLayout>
  );
};

export const protectedRoutes = [
  {
    path: "/",
    element: <App />,
  },
];
