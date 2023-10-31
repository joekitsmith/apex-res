import * as React from "react";
import { Stack, Box } from "@mui/material";
import { Head } from "../Head";
import ResponsiveAppBar, { pages } from "../AppBar/AppBar";
import { useLocation, useNavigate } from "react-router";

type Title = {
  name: string;
  navigateTo: string;
};

type MainLayoutProps = {
  children: React.ReactNode;
  header: any;
};

export const MainLayout = ({ children, header }: MainLayoutProps) => {
  const location = useLocation();
  const currentTitle = pages.find(
    (page) => page.navigateTo === location.pathname.split("/")[1]
  )?.name;

  const navigate = useNavigate();

  return (
    <>
      <Head title={currentTitle} />
      <ResponsiveAppBar />
      <Box sx={{ px: 3, mt: 10 }}>{children}</Box>
    </>
  );
};
