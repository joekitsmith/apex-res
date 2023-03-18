import * as React from "react";
import { Box, Typography, Stack } from "@mui/material";
import { usePredict } from "../api/predict";

const getResolution = (results: any, conditions: any) => {
  let result = results.filter(
    (item: any) =>
      Math.round(item.conditions.initial * 100) / 100 === conditions.initial &&
      Math.round(item.conditions.final * 100) / 100 === conditions.final
  );
  if (result === undefined) {
    return { total: 0, critical: 0 };
  }
  result = result[0];
  return {
    total: Math.round(result.resolution.total * 100) / 100,
    critical: Math.round(result.resolution.critical * 100) / 100,
  };
};

type ResolutionProps = {
  currentConditions: any;
};

export function Resolution({ currentConditions }: ResolutionProps) {
  const predict = usePredict();
  const resolution =
    predict.data !== undefined
      ? getResolution(predict.data.results, currentConditions)
      : { total: 0, critical: 0 };

  return (
    <Box
      sx={{
        width: "100%",
        height: "100%",
        backgroundColor: "#d6d6d6",
      }}
    >
      <Stack
        spacing={3}
        sx={{
          px: 2,
          pt: 1,
        }}
      >
        <Typography variant="h6">Resolution</Typography>
        <Stack direction="row" spacing={1}>
          <Typography>Critical resolution:</Typography>
          <Typography sx={{ fontWeight: "bold" }}>
            {resolution.critical}
          </Typography>
        </Stack>
        <Stack direction="row" spacing={1}>
          <Typography>Total resolution:</Typography>
          <Typography sx={{ fontWeight: "bold" }}>
            {resolution.total}
          </Typography>
        </Stack>
      </Stack>
    </Box>
  );
}
