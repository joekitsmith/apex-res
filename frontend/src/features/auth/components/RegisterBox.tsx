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
import { RegisterCredentials } from "../api/register";

type RegisterBoxProps = {
  onSuccess: () => void;
};

export function RegisterBox({ onSuccess }: RegisterBoxProps) {
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [fullName, setFullName] = React.useState("");

  const registerInputs = [
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
    {
      label: "Email",
      type: "email",
      setValue: setEmail,
    },
    {
      label: "Full Name",
      type: "text",
      setValue: setFullName,
    },
  ];

  const { register, isRegistering } = useAuth();

  const handleClickRegister = async () => {
    const credentials: RegisterCredentials = {
      username: username,
      password: password,
      email: email,
      full_name: fullName,
      disabled: false,
    };
    await register(credentials);
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
      <Stack alignItems="center" spacing={3}>
        <Typography
          variant="h4"
          sx={{
            pt: 3,
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
            width: 300,
            height: 70,
          }}
          m="auto"
          src={require("../../../assets/apex-res-logo.png")}
        />
        <Stack spacing={2}>
          {registerInputs.map((input) => (
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
            onClick={handleClickRegister}
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
            Register
          </Button>
        </Stack>
      </Stack>
    </Paper>
  );
}
