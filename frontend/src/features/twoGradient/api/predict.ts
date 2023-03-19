import { axios } from "../../../lib/axios";
import { useQuery } from "react-query";

export const predict = (): Promise<any> => {
  return axios.get("/two_gradient/predict");
};

export const usePredict = (initialised: boolean = false) => {
  return useQuery({
    queryKey: ["predict"],
    queryFn: predict,
    enabled: initialised,
  });
};
