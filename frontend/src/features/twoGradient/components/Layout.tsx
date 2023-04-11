import * as React from "react";
import { Paper } from "@mui/material";

type LayoutProps = {
  children: React.ReactNode;
};

export const Layout = ({ children }: LayoutProps) => {
  return (
    <Paper
      elevation={6}
      sx={{
        height: "87vh",
        border: 4,
      }}
    >
      {children}
    </Paper>
  );
};
