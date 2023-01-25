import { axios } from "../../../lib/axios";
import { TokenResponse } from "../types";

export type LoginCredentials = {
  username: string;
  password: string;
};

export const login = (data: LoginCredentials): Promise<TokenResponse> => {
  return axios.post("/user/token", data);
};
