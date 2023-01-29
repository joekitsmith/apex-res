import { useNavigate } from "react-router-dom";
import { Grid } from "@mui/material";
import { Layout } from "../components/Layout";
import { DataEntry } from "../components/DataEntry";
import { Chromatogram } from "../components/Chromatogram";
import { Sliders } from "../components/Sliders";

export const TwoGradient = () => {
  const navigate = useNavigate();

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
              <DataEntry />
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={9}>
          <Grid container spacing={0}>
            <Grid item xs={12} sx={{ height: "22vh", borderBottom: 1 }}>
              <Sliders />
            </Grid>
            <Grid item xs={12} sx={{ height: "67vh" }}>
              <Chromatogram />
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Layout>
  );
};
