export type InstrumentParameters = {
  dwell_time: number | null;
  dead_time: number | null;
  N: number | null;
};

export type MethodParameters = {
  gradient_time: {
    first: number | null;
    second: number | null;
  };
  gradient_solvent: {
    initial: number | null;
    final: number | null;
  };
};

export type PeakDataItem = {
  name: string;
  retention_time_first: number;
  width_first: number;
  area_first: number;
  retention_time_second: number;
  width_second: number;
  area_second: number;
};
