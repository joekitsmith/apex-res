import React from "react";
import {
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  TextField,
} from "@mui/material";
import { PeakDataItem } from "../types";

type PeakTableProps = {
  peakData: PeakDataItem[];
  setPeakData: React.Dispatch<React.SetStateAction<PeakDataItem[]>>;
};

export function PeakTable({ peakData, setPeakData }: PeakTableProps) {
  return (
    <Table size="small">
      <TableHead>
        <TableRow>
          <TableCell sx={{ backgroundColor: "#dcdcdc" }} />
          <TableCell
            align="center"
            colSpan={3}
            sx={{
              fontSize: 12,
              fontWeight: "bold",
              backgroundColor: "#afafaf",
            }}
          >
            Run 1
          </TableCell>
          <TableCell
            align="center"
            colSpan={3}
            sx={{
              fontSize: 12,
              fontWeight: "bold",
              backgroundColor: "#afafaf",
            }}
          >
            Run 2
          </TableCell>
        </TableRow>
        <TableRow>
          <PeakTableHeaderCell label="Peak" />
          <PeakTableHeaderCell label={`t\u0280`} />
          <PeakTableHeaderCell label="Width" />
          <PeakTableHeaderCell label="Area" />
          <PeakTableHeaderCell label={`t\u0280`} />
          <PeakTableHeaderCell label="Width" />
          <PeakTableHeaderCell label="Area" />
        </TableRow>
      </TableHead>
      <TableBody>
        {peakData.map((peak) => (
          <TableRow key={peak.name}>
            <PeakTableHeaderCell label={peak.name} />
            <PeakTableValueCell
              row={peak}
              peakKey="retention_time_first"
              setPeakData={setPeakData}
            />
            <PeakTableValueCell
              row={peak}
              peakKey="width_first"
              setPeakData={setPeakData}
            />
            <PeakTableValueCell
              row={peak}
              peakKey="area_first"
              setPeakData={setPeakData}
            />
            <PeakTableValueCell
              row={peak}
              peakKey="retention_time_second"
              setPeakData={setPeakData}
            />
            <PeakTableValueCell
              row={peak}
              peakKey="width_second"
              setPeakData={setPeakData}
            />
            <PeakTableValueCell
              row={peak}
              peakKey="area_second"
              setPeakData={setPeakData}
            />
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}

type PeakTableHeaderCellProps = {
  label: string;
};

function PeakTableHeaderCell({ label }: PeakTableHeaderCellProps) {
  return (
    <TableCell
      align="center"
      sx={{ fontSize: 12, fontWeight: "bold", backgroundColor: "#dcdcdc" }}
    >
      {label}
    </TableCell>
  );
}

type PeakTableValueCellProps = {
  row: PeakDataItem;
  peakKey: keyof PeakDataItem;
  setPeakData: React.Dispatch<React.SetStateAction<PeakDataItem[]>>;
};

function PeakTableValueCell({
  row,
  peakKey,
  setPeakData,
}: PeakTableValueCellProps) {
  const handleCellChange = (
    row: PeakDataItem,
    key: keyof PeakDataItem,
    value: string | undefined
  ) => {
    setPeakData((prevPeakData: PeakDataItem[]) => {
      return prevPeakData.map((prevPeakDataItem) => {
        if (prevPeakDataItem.name === row.name) {
          return { ...prevPeakDataItem, [key]: value };
        }
        return prevPeakDataItem;
      });
    });
  };

  return (
    <TableCell sx={{ p: 0, px: 1.5, minWidth: 25 }}>
      <TextField
        value={row[peakKey]}
        onChange={(e) => handleCellChange(row, peakKey, e.target.value)}
        variant="standard"
        size="small"
        sx={{ pt: 0.2 }}
        InputProps={{
          disableUnderline: true,
          style: {
            padding: 0,
            paddingBottom: 0,
            fontSize: 10,
          },
          inputProps: {
            style: {
              textAlign: "center",
              paddingBottom: 0,
            },
          },
        }}
      />
    </TableCell>
  );
}
