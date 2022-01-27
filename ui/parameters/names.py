from typing import NamedTuple
from unittest.loader import VALID_MODULE_NAME


class InstrumentParameterNames(NamedTuple):
    # instrument
    INSTRUMENT = "Instrument"
    INSTRUMENT_NAME = "Instrument name"
    DWELL_VOLUME = "Dwell volume"

    # column
    COLUMN_NAME = "Column name"
    COLUMN_LENGTH = "Column length"
    COLUMN_DIAMETER = "Column diameter"
    PARTICLE_SIZE = "Particle size"
    PLATE_NUMBER = "Plate number"
    DEAD_VOLUME = "Dead volume"


class MethodParameterNames(NamedTuple):
    # method
    METHOD = "Method"
    FLOW_RATE = "Flow rate"
    GRADIENT_TIME = "Gradient time"
    INITIAL_B = "Initial % organic"
    FINAL_B = "Final % organic"
    UV = "UV"


class PeakParameterNames(NamedTuple):
    PEAKS = "Peaks"
    DEV = "In development"
