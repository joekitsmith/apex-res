from pathlib import Path
import sys

root_dir = (Path(__file__).parent / "../").resolve()
sys.path.append(str(root_dir))

import pytest
import numpy as np

from two_grad_optimise import TwoGradOptimise
from data_classes import (
    InstrumentParams,
    ColumnParams,
    TwoGradMethodParams,
    InputParams,
)


@pytest.fixture
def optimiser():
    return TwoGradOptimise(
        InstrumentParams("", 1.0),
        ColumnParams("", 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
        TwoGradMethodParams(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
        InputParams(1.0, 1.0),
        np.array(
            [
                [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]],
                [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]],
                [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]],
                [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]],
            ]
        ),
    )


class TestCalculate:
    def test_calculate(self, optimiser):
        # assemble
        optimiser.data = np.array(
            [
                [[9.06, 10.53], [0.200, 0.242], [326.5, 259.6]],
                [[10.78, 13.2], [0.143, 0.19], [1528, 1528]],
                [[12.91, 16.24], [0.198, 0.24], [11562, 11562]],
                [[13.73, 17.50], [0.214, 0.332], [983.5, 1028.5]],
            ]
        )
        optimiser.number_of_peaks = 4
        optimiser.phi0_init = 0.4
        optimiser.phif_init = 1.0
        optimiser.tg1 = 15
        optimiser.tg2 = 30
        optimiser.t0 = 2.56
        optimiser.td = 3.05
        expected_s = np.array([8.133, 5.490, 3.650, 3.312])
        expected_logkw = np.array([4.092, 3.226, 2.604, 2.521])
        expected_N = np.array([6630.0, 16985.6, 15737.3, 11486.6])
        # act
        optimiser.process_data()
        optimiser.calculate()
        # assert
        assert optimiser.s == pytest.approx(expected_s, abs=0.001)
        assert optimiser.logkw == pytest.approx(expected_logkw, abs=0.001)
        assert optimiser.n == pytest.approx(expected_N, abs=0.1)


# @pytest.mark.skip(reason="in the way")
class TestPredict:
    def test_predict(self, optimiser):
        # assemble
        optimiser.phi0 = 0.4
        optimiser.phif = 1
        optimiser.delta_phi = 0.6
        optimiser.tg_final = 15
        optimiser.t0 = 2.56
        optimiser.td = 3.05
        optimiser.s = np.array([8.133, 5.490, 3.650, 3.312])
        optimiser.logkw = np.array([4.092, 3.226, 2.604, 2.521])
        optimiser.n = np.array([6630.0, 16985.6, 15737.3, 11486.6])
        expected_tr_pred = np.array([8.92, 10.73, 12.99, 13.84])
        expected_w_pred = np.array([0.190, 0.138, 0.174, 0.215])
        # act
        optimiser.predict()
        # assert
        assert optimiser.tr_pred == pytest.approx(expected_tr_pred, abs=0.01)
        assert optimiser.w_pred == pytest.approx(expected_w_pred, abs=0.001)


class TestCalculateParameters:
    def test_calculate_parameters(self, optimiser):
        # assemble
        b_opt = np.array([[0.12, 0.24], [0.36, 0.48]])
        tr_np = np.array([[6.0, 7.2], [8.4, 9.6]])
        w_np = np.array([[0.12, 0.24], [0.36, 0.48]])
        tg_np = np.array([[15, 15], [30, 30]])
        delta_phi_np = np.array([[0.6, 0.6], [0.6, 0.6]])
        optimiser.t0 = 2.56
        optimiser.td = 3.05
        optimiser.phi0_init = 0.4
        expected_s_avg = np.array([4.101562, 5.859375])
        expected_logkw_avg = np.array([2.166468, 2.89989])
        expected_N_avg = np.array([53475.392334, 6361.369882])
        # act
        s_avg, logkw_avg, N_avg = optimiser._calculate_parameters(
            b_opt, tr_np, w_np, tg_np, delta_phi_np
        )
        # assert
        np.testing.assert_array_almost_equal(s_avg, expected_s_avg)
        np.testing.assert_array_almost_equal(logkw_avg, expected_logkw_avg)
        np.testing.assert_array_almost_equal(N_avg, expected_N_avg)


class TestGenerateMeshArrays:
    def test_generateMeshArrays(self, optimiser, mocker):
        # assemble
        beta_np = np.array([[1.2, 2.4], [3.6, 4.8]])
        tr_np = np.array([[6.0, 7.2], [8.4, 9.6]])
        w_np = np.array([[10.8, 12.0], [13.2, 14.4]])
        mocker.patch(
            "two_grad_optimise.TwoGradOptimise._generate_mesh_arrays",
            return_value=[beta_np, tr_np, w_np],
        )
        optimiser.tg1 = 15
        optimiser.tg2 = 30
        optimiser.phif_init = 0.4
        optimiser.phi0_init = 1.0
        expected_beta_np = np.array([[1.2, 2.4], [3.6, 4.8]])
        expected_tr_np = np.array([[6.0, 7.2], [8.4, 9.6]])
        expected_w_np = np.array([[10.8, 12.0], [13.2, 14.4]])
        expected_tg_np = np.array([[15, 15], [30, 30]])
        expected_delta_phi_np = np.array([[0.6, 0.6], [0.6, 0.6]])
        # act
        (
            actual_beta_np,
            actual_tr_np,
            actual_w_np,
            actual_tg_np,
            actual_delta_phi_np,
        ) = optimiser._generate_mesh_arrays()
        # assert
        assert np.testing.assert_array_equal(actual_beta_np, expected_beta_np)
        assert np.testing.assert_array_equal(actual_tr_np, expected_tr_np)
        assert np.testing.assert_array_equal(actual_w_np, expected_w_np)
        assert np.testing.assert_array_equal(actual_tg_np, expected_tg_np)
        assert np.testing.assert_array_equal(actual_delta_phi_np, expected_delta_phi_np)


class TestBetaMeshArrays:
    def test_betaMeshArrays(self, optimiser):
        # assemble
        optimiser.tg1 = 15
        optimiser.tg2 = 30
        optimiser.tr = np.array([[1.2, 2.4]])
        optimiser.w = np.array([[0.36, 0.48]])
        optimiser.number_of_peaks = 2
        expected_combined_values = [
            np.array([[2, 2], [0.5, 0.5]]),
            np.array([[1.2, 2.4], [1.2, 2.4]]),
            np.array([[0.36, 0.48], [0.36, 0.48]]),
        ]
        # act
        combined_values = optimiser._generate_mesh_arrays()
        # assert
        assert np.testing.assert_array_equal(actual_beta_np, expected_beta_np)
        assert np.testing.assert_array_equal(actual_tr_np, expected_tr_np)
        assert np.testing.assert_array_equal(actual_w_np, expected_w_np)
        assert np.testing.assert_array_equal(actual_tg_np, expected_tg_np)
        assert np.testing.assert_array_equal(actual_delta_phi_np, expected_delta_phi_np)
