import * as React from "react";
import {
  LoginCredentials,
  RegisterCredentials,
  TokenResponse,
  UserResponse,
} from "../features/auth";
import { login, getUser, register } from "../features/auth";
import storage from "../utils/storage";
import { initReactQueryAuth } from "react-query-auth";

async function handleTokenResponse(data: TokenResponse) {
  storage.setToken(data.access_token);
}

async function loadUser() {
  if (storage.getToken()) {
    const user = await getUser();
    return user;
  }
  return null;
}

async function loginFn(data: LoginCredentials) {
  const response = await login(data);
  await handleTokenResponse(response);
  const user = await loadUser();
  return user;
}

async function registerFn(registerData: RegisterCredentials) {
  const registerResponse = await register(registerData);
  const loginData = {
    grant_type: "",
    username: registerData.username,
    password: registerData.password,
    scope: "",
    client_id: "",
    client_secret: "",
  };
  const user = await loginFn(loginData);
  return user;
}

async function logoutFn() {
  storage.clearToken();
  window.location.assign(window.location.origin as unknown as string);
}

const authConfig = {
  loadUser,
  loginFn,
  registerFn,
  logoutFn,
  LoaderComponent() {
    return (
      <div className="w-screen h-screen flex justify-center items-center">
        {/* <Spinner size="xl" /> */}
      </div>
    );
  },
};

export const { AuthProvider, useAuth } = initReactQueryAuth<
  UserResponse | null,
  unknown,
  LoginCredentials,
  RegisterCredentials
>(authConfig);
