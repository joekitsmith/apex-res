import Axios, { AxiosRequestConfig } from "axios";

import { API_URL } from "../config";
import { useNotificationStore } from "../stores/notifications";
import storage from "../utils/storage";

const onFulfilled = (response: any) => {
  return response.data;
};

const onRejected = (error: any) => {
  const message = error.response?.data?.message || error.message;
  useNotificationStore.getState().addNotification({
    type: "error",
    title: "Error",
    message,
  });

  return Promise.reject(error);
};

// General axios client that uses authorization token if it exists

function requestInterceptor(config: AxiosRequestConfig) {
  const token = storage.getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  config.headers.Accept = "application/json";
  return config;
}

export const axios = Axios.create({
  baseURL: API_URL,
});
axios.interceptors.request.use(requestInterceptor);
axios.interceptors.response.use(onFulfilled, onRejected);

// Axios client for authorization

function requestInterceptorAuth(config: AxiosRequestConfig) {
  config.headers.accept = "application/json";
  config.headers["Content-Type"] = "application/x-www-form-urlencoded";
  return config;
}
export const axiosAuth = Axios.create({
  baseURL: API_URL,
});
axiosAuth.interceptors.request.use(requestInterceptorAuth);
axiosAuth.interceptors.response.use(onFulfilled, onRejected);
