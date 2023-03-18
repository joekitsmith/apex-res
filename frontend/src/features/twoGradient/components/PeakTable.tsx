import React from "react";
import { Stack, Typography, IconButton, Box } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";
import {
  DataGrid,
  GridColumns,
  GridColumnHeaderParams,
  GridRenderCellParams,
} from "@mui/x-data-grid";
import { PeakDataItem } from "../types";

const columns: GridColumns = [
  {
    field: "name",
    flex: 1,
    headerAlign: "center",
    align: "center",
    sortable: false,
    type: "string",
    renderHeader: (params: GridColumnHeaderParams) => (
      <Typography sx={{ fontSize: 14, fontWeight: "bold" }}>Peak</Typography>
    ),
    renderCell: (params: GridRenderCellParams) => (
      <Typography
        sx={{ fontSize: 14, fontStyle: "italic", fontWeight: "bold" }}
      >
        {params.value}
      </Typography>
    ),
  },
  {
    field: "retention_time_first",
    flex: 1,
    headerAlign: "center",
    align: "center",
    type: "number",
    editable: true,
    sortable: false,
    renderHeader: (params: GridColumnHeaderParams) => (
      <Typography sx={{ fontSize: 14, fontWeight: "bold" }}>tR 1</Typography>
    ),
  },
  {
    field: "width_first",
    flex: 1,
    headerAlign: "center",
    align: "center",
    type: "number",
    editable: true,
    sortable: false,
    renderHeader: (params: GridColumnHeaderParams) => (
      <Typography sx={{ fontSize: 14, fontWeight: "bold" }}>w 1</Typography>
    ),
  },
  {
    field: "area_first",
    flex: 1,
    headerAlign: "center",
    align: "center",
    type: "number",
    editable: true,
    sortable: false,
    renderHeader: (params: GridColumnHeaderParams) => (
      <Typography sx={{ fontSize: 14, fontWeight: "bold" }}>Area 1</Typography>
    ),
  },
  {
    field: "retention_time_second",
    flex: 1,
    headerAlign: "center",
    align: "center",
    type: "number",
    editable: true,
    sortable: false,
    renderHeader: (params: GridColumnHeaderParams) => (
      <Typography sx={{ fontSize: 14, fontWeight: "bold" }}>tR 2</Typography>
    ),
  },
  {
    field: "width_second",
    flex: 1,
    headerAlign: "center",
    align: "center",
    type: "number",
    editable: true,
    sortable: false,
    renderHeader: (params: GridColumnHeaderParams) => (
      <Typography sx={{ fontSize: 14, fontWeight: "bold" }}>w 2</Typography>
    ),
  },
  {
    field: "area_second",
    flex: 1,
    headerAlign: "center",
    align: "center",
    type: "number",
    editable: true,
    sortable: false,
    renderHeader: (params: GridColumnHeaderParams) => (
      <Typography sx={{ fontSize: 14, fontWeight: "bold" }}>Area 2</Typography>
    ),
  },
];

type PeakTableProps = {
  peakData: PeakDataItem[];
  setPeakData: React.Dispatch<React.SetStateAction<PeakDataItem[]>>;
};

export function PeakTable({ peakData, setPeakData }: PeakTableProps) {
  const createNextRow = () => {
    return {
      name: `${peakData.length + 1}`,
      retention_time_first: 0,
      width_first: 0,
      area_first: 0,
      retention_time_second: 0,
      width_second: 0,
      area_second: 0,
    };
  };

  const handleAddRow = () => {
    setPeakData((prevRows: PeakDataItem[]) => [...prevRows, createNextRow()]);
  };

  const handleRemoveRow = () => {
    setPeakData((prevRows: PeakDataItem[]) => prevRows.slice(0, -1));
  };

  const processRowUpdate = (newRow: any, oldRow: any) => {
    const updatedRows = peakData.map((peak: PeakDataItem) => {
      if (peak.name === newRow.name) {
        return newRow;
      }
      return peak;
    });
    setPeakData(updatedRows);
    return newRow;
  };

  const handleProcessRowUpdateError = (error: Error) => {
    console.error(error);
  };

  return (
    <Stack spacing={1} sx={{ px: 2 }}>
      <Stack
        direction="row"
        justifyContent="flex-start"
        spacing={3}
        sx={{ pr: 3 }}
      >
        <IconButton disabled={peakData.length > 8} onClick={handleAddRow}>
          <AddIcon />
        </IconButton>
        <IconButton disabled={peakData.length < 3} onClick={handleRemoveRow}>
          <RemoveIcon />
        </IconButton>
      </Stack>
      <DataGrid
        columns={columns}
        rows={peakData}
        getRowId={(row) => row.name}
        processRowUpdate={processRowUpdate}
        onProcessRowUpdateError={handleProcessRowUpdateError}
        density="compact"
        hideFooter={true}
        autoHeight={true}
        disableColumnMenu={true}
        experimentalFeatures={{ newEditingApi: true }}
        sx={{
          ".MuiDataGrid-columnHeaders": { backgroundColor: "#b8b8b8" },
        }}
      />
    </Stack>
  );
}
