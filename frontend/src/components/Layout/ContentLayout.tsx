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
      <Head title={currentTitle} />
      <ResponsiveAppBar />
      <Stack spacing={3} sx={{ px: 3, pt: 1 }}>
        <Box>
          <Paper
            elevation={10}
            sx={{
              border: 2,
              pt: 4,
              display: "flex",
              height: "76vh",
              overflowY: "hidden",
              backgroundColor: "#2b2b2b",
            }}
          >
            <Stack spacing={2} sx={{ px: 2 }}>
              <Box sx={{ px: 3 }}>{header}</Box>
              {children}
            </Stack>
          </Paper>
        </Box>
      </Stack>
    </>
  );
};
