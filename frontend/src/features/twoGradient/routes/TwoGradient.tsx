import * as React from "react";
import { Grid, Box } from "@mui/material";
import { Layout } from "../components/Layout";
import { PeakInputs } from "../components/PeakInputs";
import { Chromatogram } from "../components/Chromatogram";
import { Sliders } from "../components/Sliders";
import { Resolution } from "../components/Resolution";
import { useInitialise } from "../api/initialise";
import { usePredict } from "../api/predict";
import { InstrumentParameters, MethodParameters, PeakDataItem } from "../types";
import { ParameterInputs } from "../components/ParameterInputs";
import { Update } from "../components/Update";

const isValidPeak = (obj: any) => {
  return (
    obj.name !== "" &&
    obj.retention_time_first !== "" &&
    obj.width_first !== "" &&
    obj.area_first !== "" &&
    obj.retention_time_second !== "" &&
    obj.width_second !== "" &&
    obj.area_second !== ""
  );
};

const filterPeakData = (peakData: PeakDataItem[]) => {
  return peakData.filter((peakDataItem) => isValidPeak(peakDataItem));
};

export const TwoGradient = () => {
  const [initialised, setInitialised] = React.useState(false);
  const [updateClicked, setUpdateClicked] = React.useState(false);
  const [clearClicked, setClearClicked] = React.useState(false);

  const [instrumentParameters, setInstrumentParameters] =
    React.useState<InstrumentParameters>({
      dwell_time: "2.56",
      dead_time: "3.05",
      N: "19000",
    });
  const [methodParameters, setMethodParameters] =
    React.useState<MethodParameters>({
      gradient_time_first: "15",
      gradient_time_second: "30",
      gradient_solvent_initial: "0.4",
      gradient_solvent_final: "1",
    });
  const [peakData, setPeakData] = React.useState<PeakDataItem[]>([
    {
      name: "1",
      retention_time_first: "9.06",
      width_first: "0.2",
      area_first: "326.5",
      retention_time_second: "10.53",
      width_second: "0.242",
      area_second: "259.6",
    },
    {
      name: "2",
      retention_time_first: "10.78",
      width_first: "0.143",
      area_first: "1528",
      retention_time_second: "13.2",
      width_second: "0.19",
      area_second: "1528",
    },
    {
      name: "3",
      retention_time_first: "13.73",
      width_first: "0.214",
      area_first: "983.5",
      retention_time_second: "17.5",
      width_second: "0.332",
      area_second: "1028.5",
    },
    {
      name: "4",
      retention_time_first: "",
      width_first: "",
      area_first: "",
      retention_time_second: "",
      width_second: "",
      area_second: "",
    },
    {
      name: "5",
      retention_time_first: "",
      width_first: "",
      area_first: "",
      retention_time_second: "",
      width_second: "",
      area_second: "",
    },
    {
      name: "6",
      retention_time_first: "",
      width_first: "",
      area_first: "",
      retention_time_second: "",
      width_second: "",
      area_second: "",
    },
    {
      name: "7",
      retention_time_first: "",
      width_first: "",
      area_first: "",
      retention_time_second: "",
      width_second: "",
      area_second: "",
    },
    {
      name: "8",
      retention_time_first: "",
      width_first: "",
      area_first: "",
      retention_time_second: "",
      width_second: "",
      area_second: "",
    },
    {
      name: "9",
      retention_time_first: "",
      width_first: "",
      area_first: "",
      retention_time_second: "",
      width_second: "",
      area_second: "",
    },
  ]);

  const [bValue, setBValue] = React.useState<number[]>([0.4, 1]);

  const initialise = useInitialise(setInitialised);
  const predict = usePredict(initialised);

  const handleUpdateClicked = async () => {
    await initialise.mutateAsync({
      instrument_params: instrumentParameters,
      method_params: methodParameters,
      peak_data: filterPeakData(peakData),
    });
  };

  const handleClearClicked = () => {
    setInstrumentParameters({ dwell_time: "", dead_time: "", N: "" });
    setMethodParameters({
      gradient_time_first: "",
      gradient_time_second: "",
      gradient_solvent_initial: "",
      gradient_solvent_final: "",
    });
    setPeakData([
      {
        name: "1",
        retention_time_first: "",
        width_first: "",
        area_first: "",
        retention_time_second: "",
        width_second: "",
        area_second: "",
      },
      {
        name: "2",
        retention_time_first: "",
        width_first: "",
        area_first: "",
        retention_time_second: "",
        width_second: "",
        area_second: "",
      },
      {
        name: "3",
        retention_time_first: "",
        width_first: "",
        area_first: "",
        retention_time_second: "",
        width_second: "",
        area_second: "",
      },
      {
        name: "4",
        retention_time_first: "",
        width_first: "",
        area_first: "",
        retention_time_second: "",
        width_second: "",
        area_second: "",
      },
      {
        name: "5",
        retention_time_first: "",
        width_first: "",
        area_first: "",
        retention_time_second: "",
        width_second: "",
        area_second: "",
      },
      {
        name: "6",
        retention_time_first: "",
        width_first: "",
        area_first: "",
        retention_time_second: "",
        width_second: "",
        area_second: "",
      },
      {
        name: "7",
        retention_time_first: "",
        width_first: "",
        area_first: "",
        retention_time_second: "",
        width_second: "",
        area_second: "",
      },
      {
        name: "8",
        retention_time_first: "",
        width_first: "",
        area_first: "",
        retention_time_second: "",
        width_second: "",
        area_second: "",
      },
      {
        name: "9",
        retention_time_first: "",
        width_first: "",
        area_first: "",
        retention_time_second: "",
        width_second: "",
        area_second: "",
      },
    ] as PeakDataItem[]);
  };

  React.useEffect(() => {
    if (updateClicked) {
      handleUpdateClicked();
      setUpdateClicked(false);
    }
  }, [updateClicked]);

  React.useEffect(() => {
    if (clearClicked) {
      handleClearClicked();
      setClearClicked(false);
    }
  }, [clearClicked]);

  return (
    <Layout>
      <Grid container columns={24} columnSpacing={3} sx={{ height: "100%" }}>
        <Grid item xs={7} sx={{ minWidth: 430 }}>
          <Grid container>
            <Grid item xs={12}>
              <ParameterInputs
                setUpdateClicked={setUpdateClicked}
                instrumentParameters={instrumentParameters}
                setInstrumentParameters={setInstrumentParameters}
                methodParameters={methodParameters}
                setMethodParameters={setMethodParameters}
              />
            </Grid>
            <Grid item xs={12} sx={{ mt: 3 }}>
              <PeakInputs peakData={peakData} setPeakData={setPeakData} />
            </Grid>
            <Grid
              item
              xs={12}
              sx={{ mt: 3, mb: 3, height: "100%", textAlign: "right" }}
            >
              <Update
                setUpdateClicked={setUpdateClicked}
                setClearClicked={setClearClicked}
              />
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={17} sx={{ height: "100%", minWidth: 430 }}>
          <Grid container direction="column" sx={{ height: "100%" }}>
            <Grid item>
              <Grid container columnSpacing={3}>
                <Grid item xs={9}>
                  <Sliders bValue={bValue} setBValue={setBValue} />
                </Grid>
                <Grid item xs={3}>
                  <Resolution bValue={bValue} setBValue={setBValue} />
                </Grid>
              </Grid>
            </Grid>
            <Grid item sx={{ flexGrow: 1, mt: 3 }}>
              <Chromatogram bValue={bValue} />
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Layout>
  );
};
