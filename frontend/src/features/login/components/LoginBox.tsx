import React from "react";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { useAuth } from "../../../lib/auth";
import { useNavigate } from "react-router-dom";

type LoginBoxProps = {
  onSuccess: () => void;
};

export function LoginBox({ onSuccess }: LoginBoxProps) {
  const navigate = useNavigate();

  const { login, isLoggingIn } = useAuth();

  const useClickLogin = async () => {
    await login(null);
    onSuccess();
  };

  const useClickRegister = async () => {
    navigate("/register");
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
        onClick={useClickLogin}
        sx={{
          borderTop: "2px solid black",
          borderRadius: 0,
          p: 1,
          backgroundColor: "#5797ff",
          width: "100%",
          mt: 3,
          "&.MuiButton-text": {
            color: "#000000",
            fontWeight: "bold",
            fontSize: 18,
          },
        }}
      >
        Login
      </Button>
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
