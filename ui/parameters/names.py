from typing import NamedTuple
from unittest.loader import VALID_MODULE_NAME


class ParameterGroupNames(NamedTuple):
    INSTRUMENT = "Instrument"
    METHOD = "Method"
    PEAKS = "Peaks"


class InstrumentParameterNames(NamedTuple):
    # instrument
    INSTRUMENT_NAME = "Instrument name"
    T0 = "Dwell volume"

    # column
    COLUMN_NAME = "Column name"
    COLUMN_LENGTH = "Column length"
    COLUMN_DIAMETER = "Column diameter"
    PARTICLE_SIZE = "Particle size"
    N = "Plate number"
    TD = "Dead volume"


class MethodParameterNames(NamedTuple):
    # method
    FLOW_RATE = "Flow rate"
    TG = "Gradient time"
    PHI0 = "Initial % organic"
    PHIF = "Final % organic"
    UV = "UV"


class PeakParameterNames(NamedTuple):
    DEV = "In development"
