import React from "react";
import { Paper, Typography, Grid, Stack } from "@mui/material";
import { SingleValueEntry } from "./SingleValueEntry";
import { InstrumentParameters, MethodParameters } from "../types";

interface ParameterInputsProps {
  setUpdateClicked: React.Dispatch<React.SetStateAction<boolean>>;
  instrumentParameters: InstrumentParameters;
  setInstrumentParameters: React.Dispatch<
    React.SetStateAction<InstrumentParameters>
  >;
  methodParameters: MethodParameters;
  setMethodParameters: React.Dispatch<React.SetStateAction<MethodParameters>>;
}

interface InstrumentParameterInputsProps {
  instrumentParameters: InstrumentParameters;
  setInstrumentParameters: React.Dispatch<
    React.SetStateAction<InstrumentParameters>
  >;
}

interface MethodParameterInputsProps {
  methodParameters: MethodParameters;
  setMethodParameters: React.Dispatch<React.SetStateAction<MethodParameters>>;
}

const InstrumentParameterInputs = ({
  instrumentParameters,
  setInstrumentParameters,
}: InstrumentParameterInputsProps) => {
  const updateInstrumentParameter = (
    key: keyof InstrumentParameters,
    newValue: string
  ) => {
    setInstrumentParameters((prevState) => ({
      ...prevState,
      [key]: newValue,
    }));
  };

  return (
    <Grid container rowSpacing={2}>
      <Grid item xs={6}>
        <SingleValueEntry
          label={`t\u2080`}
          descriptor="Dwell time (s)"
          value={instrumentParameters.dwell_time}
          updateValue={(newValue) =>
            updateInstrumentParameter("dwell_time", newValue)
          }
        />
      </Grid>
      <Grid item xs={6}>
        <SingleValueEntry
          label={`t\u1d48`}
          descriptor="Dead time (s)"
          value={instrumentParameters.dead_time}
          updateValue={(newValue) =>
            updateInstrumentParameter("dead_time", newValue)
          }
        />
      </Grid>
      <Grid item xs={6}>
        <SingleValueEntry
          label="N"
          descriptor="Plate number"
          value={instrumentParameters.N}
          updateValue={(newValue) => updateInstrumentParameter("N", newValue)}
        />
      </Grid>
    </Grid>
  );
};

const MethodParameterInputs = ({
  methodParameters,
  setMethodParameters,
}: MethodParameterInputsProps) => {
  const updateMethodParameter = (
    key: keyof MethodParameters,
    newValue: string
  ) => {
    setMethodParameters((prevState) => ({
      ...prevState,
      [key]: newValue,
    }));
  };

  return (
    <Grid container rowSpacing={2}>
      <Grid item xs={6}>
        <SingleValueEntry
          label={`B\u2080`}
          descriptor="Initial % organic"
          value={methodParameters.gradient_solvent_initial}
          updateValue={(newValue) =>
            updateMethodParameter("gradient_solvent_initial", newValue)
          }
        />
      </Grid>
      <Grid item xs={6}>
        <SingleValueEntry
          label={`B\u1da0`}
          descriptor="Final % organic"
          value={methodParameters.gradient_solvent_final}
          updateValue={(newValue) =>
            updateMethodParameter("gradient_solvent_final", newValue)
          }
        />
      </Grid>
      <Grid item xs={6}>
        <SingleValueEntry
          label={`tG\u2081`}
          descriptor="Run 1 gradient time (min)"
          value={methodParameters.gradient_time_first}
          updateValue={(newValue) =>
            updateMethodParameter("gradient_time_first", newValue)
          }
        />
      </Grid>
      <Grid item xs={6}>
        <SingleValueEntry
          label={`tG\u2082`}
          descriptor="Run 2 gradient time (min)"
          value={methodParameters.gradient_time_second}
          updateValue={(newValue) =>
            updateMethodParameter("gradient_time_second", newValue)
          }
        />
      </Grid>
    </Grid>
  );
};

export function ParameterInputs({
  setUpdateClicked,
  instrumentParameters,
  setInstrumentParameters,
  methodParameters,
  setMethodParameters,
}: ParameterInputsProps) {
  const handleUpdateClicked = () => {
    setUpdateClicked(true);
  };

  return (
    <Paper
      elevation={4}
      sx={{
        backgroundColor: "#ffffff",
        borderRadius: "0.5rem",
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
            Parameters
          </Typography>
          <Stack spacing={1}>
            <InstrumentParameterInputs
              instrumentParameters={instrumentParameters}
              setInstrumentParameters={setInstrumentParameters}
            />
            <MethodParameterInputs
              methodParameters={methodParameters}
              setMethodParameters={setMethodParameters}
            />
          </Stack>
        </Stack>
      </Stack>
    </Paper>
  );
}
