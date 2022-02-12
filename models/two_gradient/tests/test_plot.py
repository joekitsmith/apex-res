from pathlib import Path
import sys

root_dir = (Path(__file__).parent / "../../../").resolve()
sys.path.append(str(root_dir))

import pytest
import numpy as np

from ui.chromatogram.figure_canvas import ChromatogramCanvas
from models.two_gradient.plot import TwoGradOptimisePlot
from models.two_gradient.two_grad_optimise import TwoGradOptimise
from models.two_gradient.data_classes import (
    InstrumentParams,
    ColumnParams,
    TwoGradMethodParams,
    InputParams,
)


@pytest.fixture
def figure():
    return ChromatogramCanvas()


@pytest.fixture
def optimiser():
    return TwoGradOptimise(
        InstrumentParams("", 3.05),
        ColumnParams("", 250, 4, 5, 2, 19000, 2.56),
        TwoGradMethodParams(1, 15, 0.6, 1, 254, 15, 30),
        InputParams(4, 5),
        np.array(
            [
                [[9.06, 10.53], [0.200, 0.242], [326.5, 259.6]],
                [[10.78, 13.2], [0.143, 0.19], [335, 292.4]],
                [[12.91, 16.24], [0.198, 0.24], [4291, 4291]],
                [[13.73, 17.50], [0.214, 0.332], [1528, 1528]],
            ]
        ),
    )


@pytest.fixture
def plotter():
    return TwoGradOptimisePlot(figure, optimiser)


class TestGenerateXY:
    def test_generateXY(self, optimiser, figure):
        # assemble
        optimiser.calculate()
        optimiser.predict()
        plotter = TwoGradOptimisePlot(figure, optimiser)
        plotter.resolution = 1000
        # act
        actual_x, actual_total_y = plotter._generate_x_y()
        # assert
        assert actual_x.shape == (1000,)
        assert actual_total_y.shape == (1000,)
        assert plotter.y_max == pytest.approx(26.63, abs=0.01)
