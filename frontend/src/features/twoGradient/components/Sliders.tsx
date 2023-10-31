import * as React from "react";
import { Paper, Stack, Slider, Typography } from "@mui/material";

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
    <Paper
      elevation={4}
      sx={{
        backgroundColor: "#ffffff",
        borderRadius: "0.5rem",
        height: "100%",
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
          Conditions
        </Typography>
        <Stack spacing={3} sx={{ p: 3, pr: 6 }}>
          <Stack
            direction="row"
            justifyContent="center"
            alignItems="center"
            spacing={4}
          >
            <Stack sx={{ textAlign: "right" }}>
              <Typography sx={{ fontWeight: "bold", fontSize: 16 }}>
                %B
              </Typography>
              <Typography
                sx={{ fontSize: 11, color: "grey", minWidth: "70px" }}
              >
                % organic
              </Typography>
            </Stack>
            <Slider
              value={bValue}
              onChange={handleB0Change}
              valueLabelDisplay="auto"
              color="secondary"
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
            <Stack sx={{ textAlign: "right" }}>
              <Typography sx={{ fontWeight: "bold", fontSize: 16 }}>
                tG
              </Typography>
              <Typography
                sx={{ fontSize: 11, color: "grey", minWidth: "70px" }}
              >
                Gradient time
              </Typography>
            </Stack>
            <Slider
              value={tGValue}
              onChange={handleTGChange}
              valueLabelDisplay="auto"
              color="secondary"
            />
          </Stack>
        </Stack>
      </Stack>
    </Paper>
  );
}
