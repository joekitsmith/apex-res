import React from "react";
import {
  Paper,
  Typography,
  Grid,
  TextField,
  Stack,
  Button,
} from "@mui/material";
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
    <Grid container rowSpacing={2}>
      <Grid item xs={6}>
        <SingleValueEntry
          label={`t\u2080`}
          descriptor="Dwell time (s)"
          value={t0}
          setValue={setT0}
        />
      </Grid>
      <Grid item xs={6}>
        <SingleValueEntry
          label={`t\u1d48`}
          descriptor="Dead time (s)"
          value={td}
          setValue={setTd}
        />
      </Grid>
      <Grid item xs={6}>
        <SingleValueEntry
          label="N"
          descriptor="Plate number"
          value={N}
          setValue={setN}
        />
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
    <Grid container rowSpacing={2}>
      <Grid item xs={6}>
        <SingleValueEntry
          label={`B\u2080`}
          descriptor="Initial % organic"
          value={b0}
          setValue={setB0}
        />
      </Grid>
      <Grid item xs={6}>
        <SingleValueEntry
          label={`B\u1da0`}
          descriptor="Final % organic"
          value={bf}
          setValue={setBf}
        />
      </Grid>
      <Grid item xs={6}>
        <SingleValueEntry
          label={`tG\u2081`}
          descriptor="Run 1 gradient time (s)"
          value={tg1}
          setValue={setTg1}
        />
      </Grid>
      <Grid item xs={6}>
        <SingleValueEntry
          label={`tG\u2082`}
          descriptor="Run 2 gradient time (s)"
          value={tg2}
          setValue={setTg2}
        />
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
    <Paper
      elevation={4}
      sx={{
        backgroundColor: "#ffffff",
        borderRadius: "0.5rem",
        height: "100%",
      }}
    >
      <Stack alignItems="center" spacing={2} sx={{ pb: 3 }}>
        <Stack spacing={2.5}>
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
            Data
          </Typography>
          <Stack spacing={1}>
            <InstrumentParameterDataEntry
              instrumentParameters={instrumentParameters}
              setInstrumentParameters={setInstrumentParameters}
            />
            <MethodParameterDataEntry
              methodParameters={methodParameters}
              setMethodParameters={setMethodParameters}
            />
            <PeakTable peakData={peakData} setPeakData={setPeakData} />
          </Stack>
        </Stack>
        <Button
          variant="outlined"
          onClick={handleUpdateClicked}
          sx={{ width: "fit-content" }}
        >
          Update
        </Button>
      </Stack>
    </Paper>
  );
}
