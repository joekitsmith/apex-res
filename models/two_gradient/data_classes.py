from typing import NamedTuple


class InstrumentParams(NamedTuple):
    name: str
    td: float


class ColumnParams(NamedTuple):
    column_name: str
    column_length: float
    column_diameter: float
    particle_size: float
    pore_diameter: float
    n_est: float
    t0: float


class TwoGradMethodParams(NamedTuple):
    flow_rate: float
    tg_final: float
    phi0: float
    phif: float
    uv: float
    tg1: float
    tg2: float


class InputParams(NamedTuple):
    number_of_peaks: int
    peak_of_interest: int
