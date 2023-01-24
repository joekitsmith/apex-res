import { axios } from "../../../lib/axios";
import { TokenResponse } from "../types";

export const loginWithSpotify = (): Promise<TokenResponse> => {
  return axios.post("/user/login");
};
