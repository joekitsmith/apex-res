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
  console.log({
    ...data,
    method_params: {
      gradient_time: {
        first: data.method_params.gradient_time_first,
        second: data.method_params.gradient_time_second,
      },
      gradient_solvent: {
        initial: data.method_params.gradient_solvent_initial,
        final: data.method_params.gradient_solvent_final,
      },
    },
  });
  return axios.post("/two_gradient/initialise", {
    ...data,
    method_params: {
      gradient_time: {
        first: data.method_params.gradient_time_first,
        second: data.method_params.gradient_time_second,
      },
      gradient_solvent: {
        initial: data.method_params.gradient_solvent_initial,
        final: data.method_params.gradient_solvent_final,
      },
    },
  });
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
