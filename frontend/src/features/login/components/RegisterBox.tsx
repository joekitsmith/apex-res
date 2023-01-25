import React from "react";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { useAuth } from "../../../lib/auth";

type RegisterBoxProps = {
  onSuccess: () => void;
};

export function RegisterBox({ onSuccess }: RegisterBoxProps) {
  const { register, isRegistering } = useAuth();

  const useClickRegister = async () => {
    await register(null);
    onSuccess();
  };

  return (
    <Paper
      elevation={10}
      sx={{
        border: 3,
        width: "30vw",
      }}
    >
      <Typography
        variant="h4"
        sx={{
          padding: 3,
          mx: 5,
          textAlign: "center",
        }}
      >
        Apex Res
      </Typography>
      <Box
        component="img"
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          width: 80,
          height: 80,
        }}
        m="auto"
        src={require("../../../assets/peak-icon.webp")}
      />
      <Button
        onClick={useClickRegister}
        sx={{
          borderTop: "2px solid black",
          borderRadius: 0,
          p: 1,
          backgroundColor: "#9dc1fc",
          width: "100%",
          "&.MuiButton-text": {
            color: "#000000",
            fontSize: 12,
          },
        }}
      >
        Register
      </Button>
    </Paper>
  );
}
