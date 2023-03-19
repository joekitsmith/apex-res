import * as React from "react";
import { Grid, Box } from "@mui/material";
import { Layout } from "../components/Layout";
import { DataEntry } from "../components/DataEntry";
import { Chromatogram } from "../components/Chromatogram";
import { Sliders } from "../components/Sliders";
import { Resolution } from "../components/Resolution";
import { useInitialise } from "../api/initialise";
import { usePredict } from "../api/predict";
import { InstrumentParameters, MethodParameters, PeakDataItem } from "../types";

export const TwoGradient = () => {
  const [initialised, setInitialised] = React.useState(false);
  const [updateClicked, setUpdateClicked] = React.useState(false);

  const [instrumentParameters, setInstrumentParameters] =
    React.useState<InstrumentParameters>({
      dwell_time: 2.56,
      dead_time: 3.05,
      N: 19000,
    });
  const [methodParameters, setMethodParameters] =
    React.useState<MethodParameters>({
      gradient_time: {
        first: 15,
        second: 30,
      },
      gradient_solvent: {
        initial: 0.4,
        final: 1,
      },
    });
  const [peakData, setPeakData] = React.useState<PeakDataItem[]>([
    {
      name: "1",
      retention_time_first: 9.06,
      width_first: 0.2,
      area_first: 326.5,
      retention_time_second: 10.53,
      width_second: 0.242,
      area_second: 259.6,
    },
    {
      name: "2",
      retention_time_first: 10.78,
      width_first: 0.143,
      area_first: 1528,
      retention_time_second: 13.2,
      width_second: 0.19,
      area_second: 1528,
    },
    {
      name: "3",
      retention_time_first: 13.73,
      width_first: 0.214,
      area_first: 983.5,
      retention_time_second: 17.5,
      width_second: 0.332,
      area_second: 1028.5,
    },
  ]);

  const [bValue, setBValue] = React.useState<number[]>([0.4, 1]);

  const initialise = useInitialise(setInitialised);
  const predict = usePredict(initialised);

  const handleUpdateClicked = async () => {
    await initialise.mutateAsync({
      instrument_params: instrumentParameters,
      method_params: methodParameters,
      peak_data: peakData,
    });
  };

  React.useEffect(() => {
    if (updateClicked) {
      handleUpdateClicked();
      setUpdateClicked(false);
    }
  }, [updateClicked]);

  return (
    <Layout>
      <Grid
        container
        spacing={0}
        direction="row"
        justifyContent="center"
        alignItems="stretch"
        sx={{ height: "100%", border: 2 }}
      >
        <Grid item xs={3}>
          <Grid container>
            <Grid item xs={12} sx={{ height: "89vh", borderRight: 2 }}>
              <DataEntry
                setUpdateClicked={setUpdateClicked}
                instrumentParameters={instrumentParameters}
                setInstrumentParameters={setInstrumentParameters}
                methodParameters={methodParameters}
                setMethodParameters={setMethodParameters}
                peakData={peakData}
                setPeakData={setPeakData}
              />
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={9}>
          <Grid container spacing={0}>
            <Grid item xs={9} sx={{ borderBottom: 1 }}>
              <Sliders bValue={bValue} setBValue={setBValue} />
            </Grid>
            <Grid item xs={3} sx={{ borderBottom: 1, borderLeft: 2 }}>
              <Resolution bValue={bValue} setBValue={setBValue} />
            </Grid>
            <Grid item xs={12} sx={{ height: "75vh" }}>
              <Chromatogram />
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Layout>
  );
};
