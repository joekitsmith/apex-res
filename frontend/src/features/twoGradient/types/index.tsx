export type InstrumentParameters = {
  dwell_time: string;
  dead_time: string;
  N: string;
};

export type MethodParameters = {
  gradient_time_first: string;
  gradient_time_second: string;
  gradient_solvent_initial: string;
  gradient_solvent_final: string;
};

export type PeakDataItem = {
  name: string;
  retention_time_first: string;
  width_first: string;
  area_first: string;
  retention_time_second: string;
  width_second: string;
  area_second: string;
};
