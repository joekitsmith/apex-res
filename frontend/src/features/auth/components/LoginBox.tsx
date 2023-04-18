import React from "react";
import {
  Paper,
  Box,
  Typography,
  Button,
  Stack,
  TextField,
} from "@mui/material";
import { useAuth } from "../../../lib/auth";
import { useNavigate } from "react-router-dom";
import { LoginCredentials } from "../api/login";

type LoginBoxProps = {
  onSuccess: () => void;
};

export function LoginBox({ onSuccess }: LoginBoxProps) {
  const navigate = useNavigate();

  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");

  const loginInputs = [
    {
      label: "Username",
      type: "text",
      setValue: setUsername,
    },
    {
      label: "Password",
      type: "password",
      setValue: setPassword,
    },
  ];

  const { login, isLoggingIn } = useAuth();

  const useClickLogin = async () => {
    const credentials: LoginCredentials = {
      grant_type: "",
      username: username,
      password: password,
      scope: "",
      client_id: "",
      client_secret: "",
    };
    await login(credentials);
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
      <Stack alignItems="center" spacing={3}>
        <Box
          component="img"
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            pt: 3,
            width: 300,
            height: 70,
          }}
          m="auto"
          src={require("../../../assets/apex-res-logo.png")}
        />
        <Stack spacing={2}>
          {loginInputs.map((input) => (
            <TextField
              key={input.label}
              onChange={(e) => {
                input.setValue(e.target.value);
              }}
              size="small"
              type={input.type}
              label={input.label}
              InputProps={{ style: { fontSize: 14 } }}
              InputLabelProps={{ style: { fontSize: 14 } }}
            />
          ))}
        </Stack>
        <Stack sx={{ width: "100%" }}>
          <Button
            onClick={useClickLogin}
            sx={{
              borderTop: "2px solid black",
              borderRadius: 0,
              p: 1,
              backgroundColor: "#acb7fa",
              width: "100%",
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
              backgroundColor: "#d0d5f7",
              width: "100%",
              "&.MuiButton-text": {
                color: "#000000",
                fontWeight: "bold",
                fontSize: 12,
              },
            }}
          >
            Register
          </Button>
        </Stack>
      </Stack>
    </Paper>
  );
}
