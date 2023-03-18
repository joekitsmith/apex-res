import sys
from pathlib import Path

root_dir = (Path(__file__).parent / "../").resolve()
sys.path.append(str(root_dir))

import numpy as np
import pytest
from resolution_equations import ResolutionEquations


class TestCalculateRes:
    @pytest.mark.parametrize(
        "tr1, tr2, w1, w2, expected_res",
        [
            (
                np.array([8.2, 9.4]),
                np.array([12.6, 13.8]),
                np.array([0.12, 0.24]),
                np.array([0.16, 0.28]),
                np.array([31.428571, 16.923077]),
            ),
        ],
        ids=[
            "valid",
        ],
    )
    def test_calculateRes_numberReturned(self, tr1, tr2, w1, w2, expected_res):
        # act
        actual_res = ResolutionEquations.calculate_res(tr1, tr2, w1, w2)
        # assert
        np.testing.assert_array_almost_equal(actual_res, expected_res)
