import numpy as np

from .data_classes import (
    ColumnParams,
    InputParams,
    InstrumentParams,
    TwoGradMethodParams,
)


def generate_example_inputs():
    instrument_params = InstrumentParams("Agilent 1260 Infinity I", 3.05)
    column_params = ColumnParams("Phenomenex Gemini C18", 250, 4, 5, 2, 19000, 2.56)
    method_params = TwoGradMethodParams(1, 15, 0.6, 1, 254, 15, 30)
    input_params = InputParams(8, 5)
    data = np.array(
        [
            [[9.06, 10.53], [0.200, 0.242], [326.5, 259.6]],
            [[9.597, 10.98], [0.181, 0.231], [335, 292.4]],
            [[10.34, 12.64], [0.156, 0.17], [4291, 4291]],
            [[10.78, 13.2], [0.143, 0.19], [1528, 1528]],
            [[11.21, 13.68], [0.183, 0.21], [34269, 34269]],
            [[12.52, 15.72], [0.204, 0.249], [494.3, 175.7]],
            [[12.91, 16.24], [0.198, 0.24], [11562, 11562]],
            [[13.73, 17.50], [0.214, 0.332], [983.5, 1028.5]],
        ]
    )

    return (instrument_params, column_params, method_params, input_params, data)
