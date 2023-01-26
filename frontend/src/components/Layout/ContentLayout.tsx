import * as React from "react";
import { Box, Typography, Stack, Paper, ButtonBase } from "@mui/material";
import { Head } from "../Head";
import ResponsiveAppBar, { pages } from "../AppBar/AppBar";
import { useLocation, useNavigate } from "react-router";

type Title = {
  name: string;
  navigateTo: string;
};

type ContentLayoutProps = {
  children: React.ReactNode;
  header: any;
};

export const ContentLayout = ({ children, header }: ContentLayoutProps) => {
  const location = useLocation();
  const currentTitle = pages.find(
    (page) => page.navigateTo === location.pathname.split("/")[1]
  )?.name;

  const navigate = useNavigate();

  return (
    <>
      <div>Test</div>
    </>
  );
};
