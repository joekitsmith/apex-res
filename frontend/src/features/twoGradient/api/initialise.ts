import * as React from "react";
import { axios } from "../../../lib/axios";
import { useMutation } from "react-query";
import { InstrumentParameters, MethodParameters, PeakDataItem } from "../types";

export type InitialiseModelQuery = {
  instrument_params: InstrumentParameters;
  method_params: MethodParameters;
  peak_data: PeakDataItem[];
};

export const initialise = (data: InitialiseModelQuery): Promise<any> => {
  return axios.post("/two_gradient/initialise", data);
};

export const useInitialise = (
  setInitialised: React.Dispatch<React.SetStateAction<boolean>>
) => {
  return useMutation({
    mutationFn: initialise,
    onSuccess: () => {
      setInitialised(true);
    },
  });
};
