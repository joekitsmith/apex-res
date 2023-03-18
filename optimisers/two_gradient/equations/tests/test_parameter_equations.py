import numpy as np
import pytest
from parameter_equations import ParameterEquations


class TestEstimateB:
    @pytest.mark.parametrize(
        "beta, tr1, tr2, t0, td, expected_b",
        [
            (
                np.array([0.5, 0.5]),
                np.array([11.2, 12.4]),
                np.array([13.6, 14.8]),
                3.05,
                2.56,
                np.array([0.088368, 0.079218]),
            ),
            (
                np.array([2.0, 2.0]),
                np.array([11.2, 12.4]),
                np.array([13.6, 14.8]),
                3.05,
                2.56,
                np.array([0.575637, 0.418288]),
            ),
            (
                np.array([2.0, 2.0]),
                np.array([13.6, 14.8]),
                np.array([11.2, 12.4]),
                3.05,
                2.56,
                np.array([0.176736, 0.158437]),
            ),
            (
                np.array([2.0, 2.0]),
                np.array([11.2, 12.4]),
                np.array([13.6, 14.8]),
                2.56,
                3.05,
                np.array([0.483158, 0.351087]),
            ),
            (
                np.array([0, 0]),
                np.array([11.2, 12.4]),
                np.array([13.6, 14.8]),
                2.56,
                3.05,
                np.array([np.nan, np.nan]),
            ),
        ],
        ids=[
            "beta_0.5",
            "beta_2",
            "tr1_above_tr2",
            "t0_below_td",
            "beta_zero__nan_array",
        ],
    )
    def test_estimateB_numberReturned(self, beta, tr1, tr2, t0, td, expected_b):
        # act
        actual_b = ParameterEquations.estimate_b(beta, tr1, tr2, t0, td)
        # assert
        np.testing.assert_array_almost_equal(actual_b, expected_b)


class TestCalculateLogk0:
    @pytest.mark.parametrize(
        "b, tr, t0, td, expected_logk0",
        [
            (
                np.array([[0.1, 0.1], [0.2, 0.2]]),
                np.array([[11.2, 12.4], [13.6, 14.8]]),
                3.05,
                2.56,
                np.array([[0.821551, 0.860895], [0.861177, 0.939865]]),
            ),
            (
                np.array([[0.1, 0.1], [0.2, 0.2]]),
                np.array([[1.2, 2.4], [3.6, 4.8]]),
                3.05,
                2.56,
                np.array([[0.493682, 0.533026], [0.205439, 0.284127]]),
            ),
        ],
        ids=[
            "t0+td_above_tr",
            "t0+td_below_tr",
        ],
    )
    def test_calculateLogk0_numberReturned(self, b, tr, t0, td, expected_logk0):
        # act
        actual_logk0 = ParameterEquations.calculate_logk0(b, tr, t0, td)
        # assert
        np.testing.assert_array_almost_equal(actual_logk0, expected_logk0)


class TestRetentionF:
    @pytest.mark.parametrize(
        "b, b_est, logk0_est, tr, t0, td, expected_diff",
        [
            (
                np.array([0.1, 0.1, 0.2, 0.2]),
                np.array([[0.1, 0.12], [0.2, 0.22]]),
                np.array([[0.5, 0.6], [0.3, 0.2]]),
                np.array([[11.2, 12.4], [13.6, 14.8]]),
                3.05,
                2.56,
                np.array([0.080045, 0.786996, 5.166004, 7.414614]),
            ),
            (
                np.array([0.1, 0.1, 0.2, 0.2]),
                np.array([[0.1, 0.12], [0.2, 0.22]]),
                np.array([[0.5, 0.6], [0.3, 0.2]]),
                np.array([[11.2, 12.4], [13.6, 14.8]]),
                0,
                2.56,
                np.array([np.nan, np.nan, np.nan, np.nan]),
            ),
        ],
        ids=["valid", "t0_zero"],
    )
    def test_retentionF_numberReturned(
        self, b, b_est, logk0_est, tr, t0, td, expected_diff
    ):
        # act
        actual_diff = ParameterEquations.retention_f(b, b_est, logk0_est, tr, t0, td)
        # assert
        np.testing.assert_array_almost_equal(actual_diff, expected_diff)


class TestCalculateS:
    @pytest.mark.parametrize(
        "b, tg, delta_phi, t0, expected_s",
        [
            (
                np.array([[0.1, 0.12], [0.2, 0.22]]),
                np.array([[15, 15], [30, 30]]),
                np.array([[0.6, 0.6], [0.6, 0.6]]),
                3.05,
                np.array([[0.819672, 0.983607], [3.278689, 3.606557]]),
            ),
            (
                np.array([[0.1, 0.12], [0.2, 0.22]]),
                np.array([[15, 15], [30, 30]]),
                np.array([[0.6, 0.6], [0.6, 0.6]]),
                0,
                np.array([[np.inf, np.inf], [np.inf, np.inf]]),
            ),
            (
                np.array([[0.1, 0.12], [0.2, 0.22]]),
                np.array([[15, 15], [30, 30]]),
                np.array([[0, 0], [0, 0]]),
                3.05,
                np.array([[np.inf, np.inf], [np.inf, np.inf]]),
            ),
        ],
        ids=["valid", "t0_zero", "delta_phi_zero"],
    )
    def test_calculateS_numberReturned(self, b, tg, delta_phi, t0, expected_s):
        # act
        actual_s = ParameterEquations.calculate_s(b, tg, delta_phi, t0)
        # assert
        np.testing.assert_array_almost_equal(actual_s, expected_s)


class TestCalculateLogkw:
    @pytest.mark.parametrize(
        "logk0, s, phi0_init, expected_logkw",
        [
            (
                np.array([[0.2, 0.3], [0.4, 0.5]]),
                np.array([[0.6, 0.7], [0.8, 0.9]]),
                0.4,
                np.array([[0.44, 0.58], [0.72, 0.86]]),
            ),
            (
                np.array([[0.2, 0.3], [0.4, 0.5]]),
                np.array([[0.6, 0.7], [0.8, 0.9]]),
                0,
                np.array([[0.2, 0.3], [0.4, 0.5]]),
            ),
        ],
        ids=["valid", "phi0_init_zero__equal_to_logk0"],
    )
    def test_calculateLogkw_numberReturned(self, logk0, s, phi0_init, expected_logkw):
        # act
        actual_logkw = ParameterEquations.calculate_logkw(logk0, s, phi0_init)
        # assert
        np.testing.assert_array_almost_equal(actual_logkw, expected_logkw)


class TestEstimateN:
    @pytest.mark.parametrize(
        "logk0, b, w, t0, td, expected_N",
        [
            (
                np.array([[0.2, 0.3], [0.4, 0.5]]),
                np.array([[0.6, 0.7], [0.8, 0.9]]),
                np.array([[0.12, 0.24], [0.36, 0.48]]),
                3.05,
                2.56,
                np.array([[36468.95286, 7513.149542], [2912.761785, 1479.011353]]),
            ),
            (
                np.array([[0.2, 0.3], [0.4, 0.5]]),
                np.array([[0.6, 0.7], [0.8, 0.9]]),
                np.array([[0, 0], [0, 0]]),
                3.05,
                2.56,
                np.array([[np.inf, np.inf], [np.inf, np.inf]]),
            ),
        ],
        ids=["valid", "w_zero"],
    )
    def test_estimateN_numberReturned(self, logk0, b, w, t0, td, expected_N):
        # act
        actual_N = ParameterEquations.estimate_N(logk0, b, w, t0, td)
        # assert
        np.testing.assert_array_almost_equal(actual_N, expected_N)
