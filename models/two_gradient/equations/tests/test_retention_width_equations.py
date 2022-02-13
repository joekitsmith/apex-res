from pathlib import Path
import sys

root_dir = (Path(__file__).parent / "../").resolve()
sys.path.append(str(root_dir))

import pytest
import numpy as np

from retention_width_equations import RetentionWidthEquations


class TestCalculateLogk0:
    @pytest.mark.parametrize(
        "logkw, s, phi0, expected_logk0",
        [
            (
                np.array([0.12, 0.24]),
                np.array([0.34, 0.48]),
                np.array([0.60, 0.60]),
                np.array([-0.084, -0.048]),
            ),
        ],
        ids=[
            "valid",
        ],
    )
    def test_calculateLogk0_numberReturned(self, logkw, s, phi0, expected_logk0):
        # act
        actual_logk0 = RetentionWidthEquations.calculate_logk0(logkw, s, phi0)
        # assert
        np.testing.assert_array_almost_equal(actual_logk0, expected_logk0)
