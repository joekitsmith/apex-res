import React from "react";
import { Typography, TextField, Stack } from "@mui/material";

type SingleValueEntryProps = {
  label: string;
  value: any;
  setValue: React.Dispatch<React.SetStateAction<any>>;
};

export function SingleValueEntry({
  label,
  value,
  setValue,
}: SingleValueEntryProps) {
  return (
    <Stack direction="row" alignItems="center" spacing={2} sx={{ px: 3 }}>
      <Typography sx={{ fontSize: 14 }}>{label}</Typography>
      <TextField
        value={value}
        onChange={(e) => setValue(e.target.value)}
        size="small"
        variant="standard"
        InputProps={{ style: { fontSize: 14 } }}
        InputLabelProps={{ style: { fontSize: 14 } }}
      />
    </Stack>
  );
}
