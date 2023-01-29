import React from "react";
import { Box, Typography } from "@mui/material";

export function Resolution() {
  return (
    <Box
      sx={{
        width: "100%",
        height: "100%",
        backgroundColor: "#d6d6d6",
      }}
    >
      <Typography
        variant="h6"
        sx={{
          px: 2,
          pt: 1,
        }}
      >
        Resolution
      </Typography>
    </Box>
  );
}
