import * as React from "react";
import { Box } from "@mui/material";

type LayoutProps = {
  children: React.ReactNode;
};

export const Layout = ({ children }: LayoutProps) => {
  return (
    <Box
      sx={{
        height: "87vh",
      }}
    >
      {children}
    </Box>
  );
};
