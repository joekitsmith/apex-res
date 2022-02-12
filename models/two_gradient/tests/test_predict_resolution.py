from pathlib import Path
import sys

root_dir = (Path(__file__).parent / "../").resolve()
sys.path.append(str(root_dir))

import pytest
import numpy as np

from resolution import Resolution


class TestPredictResolution:
    @pytest.mark.parametrize(
        "tr_pred, w_pred, tg_final, peak_of_interest, expected_total_res, expected_critical_res,",
        [
            (
                np.array([11.77, 11.76, 14.49, 14.50]),
                np.array([0.181, 0.182, 0.237, 0.237]),
                15,
                1,
                52.28,
                0.06,
            ),
        ],
    )
    def test_predict_resolution(
        self,
        tr_pred,
        w_pred,
        tg_final,
        peak_of_interest,
        expected_total_res,
        expected_critical_res,
    ):
        # act
        actual_total_res, actual_critical_res = Resolution.predict_resolution(
            tr_pred, w_pred, tg_final, peak_of_interest
        )
        # assert
        assert actual_total_res == pytest.approx(expected_total_res, abs=0.01)
        assert actual_critical_res == pytest.approx(expected_critical_res, abs=0.01)
