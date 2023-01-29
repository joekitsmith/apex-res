import React from "react";
import { Box, Typography, Grid, TextField, Stack, Button } from "@mui/material";
import { SingleValueEntry } from "./SingleValueEntry";
import { PeakTable } from "./PeakTable";

export function DataEntry() {
  return (
    <Box
      sx={{
        width: "100%",
        height: "100%",
        backgroundColor: "#d6d6d6",
      }}
    >
      <Stack
        justifyContent="space-between"
        alignItems="center"
        sx={{ height: "100%" }}
      >
        <Stack spacing={3}>
          <Typography
            variant="h6"
            sx={{
              px: 2,
              pt: 1,
            }}
          >
            Data
          </Typography>
          <Stack spacing={3}>
            <Grid container rowSpacing={4}>
              <Grid item xs={12}>
                <Grid container rowSpacing={2}>
                  <Grid item xs={6}>
                    <SingleValueEntry label="t0" />
                  </Grid>
                  <Grid item xs={6}>
                    <SingleValueEntry label="td" />
                  </Grid>
                  <Grid item xs={6}>
                    <SingleValueEntry label="N" />
                  </Grid>
                </Grid>
              </Grid>
              <Grid item xs={12}>
                <Grid container rowSpacing={2}>
                  <Grid item xs={6}>
                    <SingleValueEntry label="B0" />
                  </Grid>
                  <Grid item xs={6}>
                    <SingleValueEntry label="Bf" />
                  </Grid>
                  <Grid item xs={6}>
                    <SingleValueEntry label="tG1" />
                  </Grid>
                  <Grid item xs={6}>
                    <SingleValueEntry label="tG2" />
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
            <PeakTable />
          </Stack>
        </Stack>
        <Button variant="outlined" sx={{ mb: 2, width: "fit-content" }}>
          Update
        </Button>
      </Stack>
    </Box>
  );
}
