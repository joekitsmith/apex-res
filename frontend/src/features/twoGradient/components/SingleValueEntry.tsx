import React from "react";
import { Typography, TextField, Stack } from "@mui/material";

type SingleValueEntryProps = {
  label: string;
  descriptor: string;
  value: any;
  setValue: React.Dispatch<React.SetStateAction<any>>;
};

export function SingleValueEntry({
  label,
  descriptor,
  value,
  setValue,
}: SingleValueEntryProps) {
  return (
    <Stack
      direction="row"
      alignItems="center"
      justifyContent="flex-end"
      spacing={2}
      sx={{ px: 2.5 }}
    >
      <Typography sx={{ fontSize: 16, fontWeight: "bold" }}>{label}</Typography>
      <Stack direction="row" alignItems="center" spacing={1}>
        <TextField
          value={value}
          variant="outlined"
          onChange={(e) => setValue(e.target.value)}
          size="small"
          InputProps={{ style: { fontSize: 13 } }}
        />
        <Typography sx={{ fontSize: 8, color: "grey", maxWidth: "30px" }}>
          {descriptor}
        </Typography>
      </Stack>
    </Stack>
  );
}
