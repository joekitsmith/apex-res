from typing import NamedTuple
from unittest.loader import VALID_MODULE_NAME


class ParameterGroupNames(NamedTuple):
    INSTRUMENT = "Instrument"
    METHOD = "Method"
    PEAKS = "Peaks"


class InstrumentParameterNames(NamedTuple):
    # instrument
    # INSTRUMENT_NAME = "Instrument name"
    T0 = "Dwell volume"

    # column
    # COLUMN_NAME = "Column name"
    # COLUMN_LENGTH = "Column length"
    # COLUMN_DIAMETER = "Column diameter"
    N_EST = "N (est.)"
    # PARTICLE_SIZE = "Particle size"
    TD = "Dead volume"


class MethodParameterNames(NamedTuple):
    # method
    # FLOW_RATE = "Flow rate"
    TG_FINAL = "Gradient time"
    PHI0 = "Initial % organic"
    PHIF = "Final % organic"


class ConditionParameterNames(NamedTuple):
    # condition
    PHI0 = MethodParameterNames.PHI0
    PHIF = MethodParameterNames.PHIF


class DataEntryParameterNames(NamedTuple):
    TG1 = "tg1"
    TG2 = "tg2"


class PeakParameterNames(NamedTuple):
    DEV = "In development"
