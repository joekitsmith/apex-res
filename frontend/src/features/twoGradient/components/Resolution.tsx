import * as React from "react";
import { Paper, Typography, Stack, Grid, Button } from "@mui/material";
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
    <Paper
      elevation={4}
      sx={{
        backgroundColor: "#ffffff",
        borderRadius: "0.5rem",
        height: "100%",
      }}
    >
      <Stack spacing={3}>
        <Typography
          sx={{
            backgroundColor: "#30115c",
            borderRadius: "0.5rem 0.5rem 0px 0px",
            py: 0.5,
            px: 1.5,
            fontWeight: "bold",
            color: "#ffffff",
            fontSize: 14,
          }}
        >
          Resolution
        </Typography>
        <Grid container>
          <Grid item xs={6}>
            <Stack spacing={0.5} sx={{ textAlign: "center" }}>
              <Typography sx={{ fontSize: 13 }}>Total</Typography>
              <Typography sx={{ fontWeight: "bold", fontSize: 18 }}>
                {resolution.total}
              </Typography>
            </Stack>
          </Grid>
          <Grid item xs={6}>
            <Stack spacing={0.5} sx={{ textAlign: "center" }}>
              <Typography sx={{ fontSize: 13 }}>Critical</Typography>
              <Typography sx={{ fontWeight: "bold", fontSize: 18 }}>
                {resolution.critical}
              </Typography>
            </Stack>
          </Grid>
          <Grid item xs={12} sx={{ textAlign: "center", mt: 3 }}>
            <Button
              onClick={handleOptimiseClicked}
              variant="outlined"
              sx={{ fontSize: 12 }}
            >
              Optimise
            </Button>
          </Grid>
        </Grid>
      </Stack>
    </Paper>
  );
}
