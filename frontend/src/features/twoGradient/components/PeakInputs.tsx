import React from "react";
import { Paper, Typography, Stack } from "@mui/material";
import { PeakTable } from "./PeakTable";
import { PeakDataItem } from "../types";

interface PeakInputsProps {
  peakData: PeakDataItem[];
  setPeakData: React.Dispatch<React.SetStateAction<PeakDataItem[]>>;
}

export function PeakInputs({ peakData, setPeakData }: PeakInputsProps) {
  return (
    <Paper
      elevation={4}
      sx={{
        backgroundColor: "#ffffff",
        borderRadius: "0.5rem",
      }}
    >
      <Stack>
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
          Peaks
        </Typography>
        <PeakTable peakData={peakData} setPeakData={setPeakData} />
      </Stack>
    </Paper>
  );
}
