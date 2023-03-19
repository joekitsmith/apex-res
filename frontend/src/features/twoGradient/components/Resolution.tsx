import * as React from "react";
import { Box, Typography, Stack, Grid, Button } from "@mui/material";
import { usePredict } from "../api/predict";

const getResolution = (results: any, conditions: any) => {
  let result = results.filter(
    (item: any) =>
      Math.round(item.conditions.initial * 100) / 100 === conditions[0] &&
      Math.round(item.conditions.final * 100) / 100 === conditions[1]
  );
  if (result[0] === undefined) {
    return { total: 0, critical: 0 };
  }
  result = result[0];
  return {
    total: Math.round(result.resolution.total * 100) / 100,
    critical: Math.round(result.resolution.critical * 100) / 100,
  };
};

type ResolutionProps = {
  bValue: any;
  setBValue: React.Dispatch<React.SetStateAction<any>>;
};

export function Resolution({ bValue, setBValue }: ResolutionProps) {
  const predict = usePredict();
  const resolution =
    predict.data !== undefined
      ? getResolution(predict.data.results, bValue)
      : { total: 0, critical: 0 };

  const handleOptimiseClicked = () => {
    if (predict.data !== undefined) {
      setBValue([
        predict.data.optimum.conditions.initial,
        predict.data.optimum.conditions.final,
      ]);
    }
  };

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
          pt: 1,
        }}
      >
        <Typography variant="h6" sx={{ px: 2 }}>
          Resolution
        </Typography>
        <Grid container columnSpacing={2}>
          <Grid item xs={5}>
            <Grid container rowSpacing={2}>
              <Grid item xs={12}>
                <Stack direction="row" spacing={1}>
                  <Typography sx={{ fontSize: 14 }}>
                    Critical resolution:
                  </Typography>
                  <Typography sx={{ fontWeight: "bold", fontSize: 15 }}>
                    {resolution.critical}
                  </Typography>
                </Stack>
              </Grid>
              <Grid item xs={12}>
                <Stack direction="row" spacing={1}>
                  <Typography sx={{ fontSize: 14 }}>
                    Total resolution:
                  </Typography>
                  <Typography sx={{ fontWeight: "bold" }}>
                    {resolution.total}
                  </Typography>
                </Stack>
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs={5}>
            <Button
              onClick={handleOptimiseClicked}
              variant="outlined"
              sx={{ fontSize: 12 }}
            >
              Optimise critical resolution
            </Button>
          </Grid>
        </Grid>
      </Stack>
    </Box>
  );
}
