import React from "react";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { useAuth } from "../../../lib/auth";

type LoginBoxProps = {
  onSuccess: () => void;
};

export function LoginBox({ onSuccess }: LoginBoxProps) {
  const { login, isLoggingIn } = useAuth();

  const useSubmit = async () => {
    await login(null);
    onSuccess();
  };

  return (
    <Paper
      elevation={10}
      sx={{
        border: 3,
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
        onClick={useSubmit}
        sx={{
          borderTop: "2px solid black",
          borderRadius: 0,
          p: 1,
          backgroundColor: "#6fc75b",
          width: "100%",
          mt: 3,
          "&.MuiButton-text": {
            color: "#000000",
            fontWeight: "bold",
            fontSize: 15,
          },
        }}
      >
        Login
      </Button>
    </Paper>
  );
}
