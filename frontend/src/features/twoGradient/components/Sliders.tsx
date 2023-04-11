import * as React from "react";
import { Box, Stack, Slider, Typography } from "@mui/material";

type SlidersProps = {
  bValue: number[];
  setBValue: React.Dispatch<React.SetStateAction<number[]>>;
};

export function Sliders({ bValue, setBValue }: SlidersProps) {
  const minBRange = 0.15;

  const [tGValue, setTGValue] = React.useState<number>(15);

  const handleB0Change = (
    event: Event,
    newValue: number | number[],
    activeThumb: number
  ) => {
    if (!Array.isArray(newValue)) {
      return;
    }

    if (newValue[1] - newValue[0] < minBRange) {
      if (activeThumb === 0) {
        const clamped = Math.min(newValue[0], 100 - minBRange);
        setBValue([clamped, clamped + minBRange]);
      } else {
        const clamped = Math.max(newValue[1], minBRange);
        setBValue([clamped - minBRange, clamped]);
      }
    } else {
      setBValue(newValue as number[]);
    }
  };

  const handleTGChange = (event: Event, newValue: number | number[]) => {
    setTGValue(newValue as number);
  };

  return (
    <Stack spacing={5} sx={{ py: 5, px: 5 }}>
      <Stack
        direction="row"
        justifyContent="center"
        alignItems="center"
        spacing={5}
      >
        <Typography component="span" sx={{ fontWeight: "bold", fontSize: 16 }}>
          B:
        </Typography>
        <Slider
          value={bValue}
          onChange={handleB0Change}
          valueLabelDisplay="auto"
          min={0}
          max={1}
          step={0.01}
          disableSwap
        />
      </Stack>
      <Stack
        direction="row"
        justifyContent="center"
        alignItems="center"
        spacing={5}
      >
        <Typography component="span" sx={{ fontWeight: "bold", fontSize: 16 }}>
          tG:
        </Typography>
        <Slider
          value={tGValue}
          onChange={handleTGChange}
          valueLabelDisplay="auto"
        />
      </Stack>
    </Stack>
  );
}
