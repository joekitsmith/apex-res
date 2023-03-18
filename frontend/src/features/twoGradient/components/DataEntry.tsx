import React from "react";
import { Box, Typography, Grid, TextField, Stack, Button } from "@mui/material";
import { SingleValueEntry } from "./SingleValueEntry";
import { PeakTable } from "./PeakTable";
import { InstrumentParameters, MethodParameters, PeakDataItem } from "../types";

interface DataEntryProps {
  setUpdateClicked: React.Dispatch<React.SetStateAction<boolean>>;
  instrumentParameters: InstrumentParameters;
  setInstrumentParameters: React.Dispatch<
    React.SetStateAction<InstrumentParameters>
  >;
  methodParameters: MethodParameters;
  setMethodParameters: React.Dispatch<React.SetStateAction<MethodParameters>>;
  peakData: PeakDataItem[];
  setPeakData: React.Dispatch<React.SetStateAction<PeakDataItem[]>>;
}

interface InstrumentParameterDataEntryProps {
  instrumentParameters: InstrumentParameters;
  setInstrumentParameters: React.Dispatch<
    React.SetStateAction<InstrumentParameters>
  >;
}

interface MethodParameterDataEntryProps {
  methodParameters: MethodParameters;
  setMethodParameters: React.Dispatch<React.SetStateAction<MethodParameters>>;
}

interface PeakDataEntryProps {
  peakData: PeakDataItem[];
  setPeakData: React.Dispatch<React.SetStateAction<PeakDataItem[]>>;
}

const InstrumentParameterDataEntry = ({
  instrumentParameters,
  setInstrumentParameters,
}: InstrumentParameterDataEntryProps) => {
  const [t0, setT0] = React.useState<number | null>(
    instrumentParameters.dwell_time
  );
  const [td, setTd] = React.useState<number | null>(
    instrumentParameters.dead_time
  );
  const [N, setN] = React.useState<number | null>(instrumentParameters.N);

  React.useEffect(() => {
    setInstrumentParameters({
      dwell_time: t0,
      dead_time: td,
      N: N,
    });
  }, [t0, td, N]);

  return (
    <Grid container rowSpacing={4}>
      <Grid item xs={12}>
        <Grid container rowSpacing={2}>
          <Grid item xs={6}>
            <SingleValueEntry label="t0" value={t0} setValue={setT0} />
          </Grid>
          <Grid item xs={6}>
            <SingleValueEntry label="td" value={td} setValue={setTd} />
          </Grid>
          <Grid item xs={6}>
            <SingleValueEntry label="N" value={N} setValue={setN} />
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
};

const MethodParameterDataEntry = ({
  methodParameters,
  setMethodParameters,
}: MethodParameterDataEntryProps) => {
  const [tg1, setTg1] = React.useState<number | null>(
    methodParameters.gradient_time.first
  );
  const [tg2, setTg2] = React.useState<number | null>(
    methodParameters.gradient_time.second
  );
  const [b0, setB0] = React.useState<number | null>(
    methodParameters.gradient_solvent.initial
  );
  const [bf, setBf] = React.useState<number | null>(
    methodParameters.gradient_solvent.final
  );

  return (
    <Grid item xs={12}>
      <Grid container rowSpacing={2}>
        <Grid item xs={6}>
          <SingleValueEntry label="B0" value={b0} setValue={setB0} />
        </Grid>
        <Grid item xs={6}>
          <SingleValueEntry label="Bf" value={bf} setValue={setBf} />
        </Grid>
        <Grid item xs={6}>
          <SingleValueEntry label="tG1" value={tg1} setValue={setTg1} />
        </Grid>
        <Grid item xs={6}>
          <SingleValueEntry label="tG2" value={tg2} setValue={setTg2} />
        </Grid>
      </Grid>
    </Grid>
  );
};

export function DataEntry({
  setUpdateClicked,
  instrumentParameters,
  setInstrumentParameters,
  methodParameters,
  setMethodParameters,
  peakData,
  setPeakData,
}: DataEntryProps) {
  const handleUpdateClicked = () => {
    setUpdateClicked(true);
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
        justifyContent="space-between"
        alignItems="center"
        sx={{ height: "100%" }}
      >
        <Stack spacing={6}>
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
              <InstrumentParameterDataEntry
                instrumentParameters={instrumentParameters}
                setInstrumentParameters={setInstrumentParameters}
              />
              <MethodParameterDataEntry
                methodParameters={methodParameters}
                setMethodParameters={setMethodParameters}
              />
            </Grid>
            <PeakTable peakData={peakData} setPeakData={setPeakData} />
          </Stack>
        </Stack>
        <Button
          variant="outlined"
          onClick={handleUpdateClicked}
          sx={{ mb: 2, width: "fit-content" }}
        >
          Update
        </Button>
      </Stack>
    </Box>
  );
}
