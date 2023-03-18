import * as React from "react";
import { Box, Stack, Slider, Typography } from "@mui/material";

export function Sliders() {
  const minBRange = 15;

  const [b0Value, setB0Value] = React.useState<number[]>([40, 100]);
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
        setB0Value([clamped, clamped + minBRange]);
      } else {
        const clamped = Math.max(newValue[1], minBRange);
        setB0Value([clamped - minBRange, clamped]);
      }
    } else {
      setB0Value(newValue as number[]);
    }
  };

  const handleTGChange = (event: Event, newValue: number | number[]) => {
    setTGValue(newValue as number);
  };

  return (
    <Box
      sx={{
        backgroundColor: "#d6d6d6",
      }}
    >
      <Stack spacing={5} sx={{ py: 5, px: 8 }}>
        <Stack
          direction="row"
          justifyContent="center"
          alignItems="center"
          spacing={5}
        >
          <Typography
            component="span"
            sx={{ fontWeight: "bold", fontSize: 16 }}
          >
            B:
          </Typography>
          <Slider
            value={b0Value}
            onChange={handleB0Change}
            valueLabelDisplay="auto"
            disableSwap
          />
        </Stack>
        <Stack
          direction="row"
          justifyContent="center"
          alignItems="center"
          spacing={5}
        >
          <Typography
            component="span"
            sx={{ fontWeight: "bold", fontSize: 16 }}
          >
            tG:
          </Typography>
          <Slider
            value={tGValue}
            onChange={handleTGChange}
            valueLabelDisplay="auto"
          />
        </Stack>
      </Stack>
    </Box>
  );
}
