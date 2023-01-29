import React from "react";
import { Stack, Typography, IconButton, Box } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";
import {
  DataGrid,
  GridColumns,
  GridColumnHeaderParams,
  GridRenderCellParams,
  GridRowModel,
} from "@mui/x-data-grid";

type Row = {
  peak: string;
  tr1: number;
  area1: number;
  tr2: number;
  area2: number;
};

const columns: GridColumns = [
  {
    field: "peak",
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
    field: "tr1",
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
    field: "area1",
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
    field: "tr2",
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
    field: "area2",
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

export function PeakTable() {
  const [rows, setRows] = React.useState<Row[]>([
    {
      peak: "1",
      tr1: 1,
      area1: 2,
      tr2: 3,
      area2: 4,
    },
    {
      peak: "2",
      tr1: 1,
      area1: 2,
      tr2: 3,
      area2: 4,
    },
  ]);

  const createNextRow = () => {
    return { peak: `${rows.length + 1}`, tr1: 0, area1: 0, tr2: 0, area2: 0 };
  };

  const handleAddRow = () => {
    setRows((prevRows) => [...prevRows, createNextRow()]);
  };

  const handleRemoveRow = () => {
    setRows((prevRows) => prevRows.slice(0, -1));
  };

  const processRowUpdate = (newRow: any, oldRow: any) => {
    const updatedRows = rows.map((row) => {
      if (row.peak === newRow.peak) {
        return newRow;
      }
      return row;
    });
    setRows(updatedRows);
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
        <IconButton disabled={rows.length > 8} onClick={handleAddRow}>
          <AddIcon />
        </IconButton>
        <IconButton disabled={rows.length < 3} onClick={handleRemoveRow}>
          <RemoveIcon />
        </IconButton>
      </Stack>
      <DataGrid
        columns={columns}
        rows={rows}
        getRowId={(row) => row.peak}
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
