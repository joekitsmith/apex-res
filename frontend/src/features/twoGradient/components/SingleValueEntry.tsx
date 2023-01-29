import React from "react";
import { Typography, TextField, Stack } from "@mui/material";

type SingleValueEntryProps = {
  label: string;
};

export function SingleValueEntry({ label }: SingleValueEntryProps) {
  return (
    <Stack direction="row" alignItems="center" spacing={2} sx={{ px: 3 }}>
      <Typography sx={{ fontSize: 14 }}>{label}</Typography>
      <TextField
        size="small"
        variant="standard"
        InputProps={{ style: { fontSize: 14 } }}
        InputLabelProps={{ style: { fontSize: 14 } }}
      />
    </Stack>
  );
}
