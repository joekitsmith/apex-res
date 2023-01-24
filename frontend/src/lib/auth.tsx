import * as React from "react";
import { TokenResponse, UserResponse } from "../features/login";
import { loginWithSpotify, getUser } from "../features/login";
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

async function loginFn() {
  const response = await loginWithSpotify();
  await handleTokenResponse(response);
  const user = await loadUser();
  return user;
}

async function registerFn() {
  return Promise.resolve({ username: "" });
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
  UserResponse | null,
  UserResponse | null,
  null
>(authConfig);
