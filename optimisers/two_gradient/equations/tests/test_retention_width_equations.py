import numpy as np
import pytest
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


class TestCalculateB:
    @pytest.mark.parametrize(
        "s, delta_phi, tg, t0, expected_b",
        [
            (
                np.array([0.12, 0.36]),
                np.array([0.60, 0.60]),
                np.array([15, 30]),
                2.56,
                np.array([0.012288, 0.018432]),
            ),
        ],
        ids=[
            "valid",
        ],
    )
    def test_calculateB_numberReturned(self, s, delta_phi, tg, t0, expected_b):
        # act
        actual_b = RetentionWidthEquations.calculate_b(s, delta_phi, tg, t0)
        # assert
        np.testing.assert_array_almost_equal(actual_b, expected_b)


class TestCalculateTrSmallk0:
    @pytest.mark.parametrize(
        "t0, logk0, expected_tr",
        [
            (
                3.05,
                np.array([0.12, 0.24]),
                np.array([7.070683, 8.350293]),
            ),
        ],
        ids=[
            "valid",
        ],
    )
    def test_calculateTrSmallk0_numberReturned(self, t0, logk0, expected_tr):
        # act
        actual_tr = RetentionWidthEquations.calculate_tr_smallk0(t0, logk0)
        # assert
        np.testing.assert_array_almost_equal(actual_tr, expected_tr)


class TestCalculateTrLargek0:
    @pytest.mark.parametrize(
        "t0, td, b, logk0, expected_tr",
        [
            (
                3.05,
                2.56,
                np.array([1.2, 2.4]),
                np.array([3.6, 4.8]),
                np.array([15.880512, 12.652875]),
            ),
        ],
        ids=[
            "valid",
        ],
    )
    def test_calculateTrLargek0_numberReturned(self, t0, td, b, logk0, expected_tr):
        # act
        actual_tr = RetentionWidthEquations.calculate_tr_largek0(t0, td, b, logk0)
        # assert
        np.testing.assert_array_almost_equal(actual_tr, expected_tr)


class TestCalculateKStar:
    @pytest.mark.parametrize(
        "logk0, b, t0, td, expected_k_star",
        [
            (
                np.array([1.2, 2.4]),
                np.array([0.36, 0.48]),
                3.05,
                2.56,
                np.array([2.488038, 1.814098]),
            ),
        ],
        ids=[
            "valid",
        ],
    )
    def test_calculateKStar_numberReturned(self, logk0, b, t0, td, expected_k_star):
        # act
        actual_k_star = RetentionWidthEquations.calculate_k_star(logk0, b, t0, td)
        # assert
        np.testing.assert_array_almost_equal(actual_k_star, expected_k_star)


class TestCalculateW:
    @pytest.mark.parametrize(
        "logk0, b, N, t0, td, expected_w",
        [
            (
                np.array([1.2, 2.4]),
                np.array([0.36, 0.48]),
                np.array([12000, 18000]),
                3.05,
                2.56,
                np.array([0.249917, 0.173415]),
            ),
        ],
        ids=[
            "valid",
        ],
    )
    def test_calculateW_numberReturned(self, logk0, b, N, t0, td, expected_w):
        # act
        actual_w = RetentionWidthEquations.calculate_w(logk0, b, N, t0, td)
        # assert
        np.testing.assert_array_almost_equal(actual_w, expected_w)
