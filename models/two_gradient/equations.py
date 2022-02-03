import math
import numpy as np


class ParameterEquations:
    @staticmethod
    def estimate_b(
        beta: np.ndarray, tr1: np.ndarray, tr2: np.ndarray, t0: float, td: float
    ):
        """
        Estimate value for gradient factor b from scouting data.

        Arguments
        ---------
        beta : (4,) np.ndarray
        tr1 : (4,) np.ndarray
        tr2 : (4,) np.ndarray
        t0 : float
        td : float

        Returns
        -------
        b : (4,) np.ndarray
        """
        b = np.sqrt(
            (
                (t0 * np.log10(beta))
                / (tr1 - (tr2 / beta) - (t0 + td) * (beta - 1) / beta)
            )
            ** 2
        )

        return b

    @staticmethod
    def calculate_logk0(b: np.ndarray, tr: np.ndarray, t0: float, td: float):
        """
        Calculate logk0 value from scouting data.

        Arguments
        ---------
        b : (2,4) np.ndarray
        tr : (2,4) np.ndarray
        t0 : float
        td : float

        Returns
        -------
        logk0_est : (2,4) np.ndarray
        """
        logk0_est = b * (tr - t0 - td) / t0 - np.log10(2.3 * b)

        return logk0_est

    @staticmethod
    def retention_f(
        b: np.ndarray,
        b_est: np.ndarray,
        logk0_est: np.ndarray,
        tr: np.ndarray,
        t0: float,
        td: float,
    ):
        """
        Function used to optimise value of b by arriving back at retention times in scouting data.
        b varied in order to minimise difference between estimated and observed retention times.

        Arguments
        ---------
        b : (2,4) np.ndarray
        b_est : (2,4) np.ndarray
        logk0_est : (2,4) np.ndarray
        tr : (2,4) np.ndarray
        t0 : float
        td : float

        Returns
        -------
        (2,4) np.ndarray
            differences between estimated and observed retention times
        """
        b_est = b_est.flatten()
        logk0_est = logk0_est.flatten()
        tr = tr.flatten()

        tr_est = (
            (t0 / b_est)
            * np.log10(
                2.3 * (10 ** logk0_est) * b * (1 - (td / (t0 * (10 ** logk0_est)))) + 1
            )
            + t0
            + td
        )

        return np.sqrt((tr_est - tr) ** 2)

    @staticmethod
    def calculate_s(
        b: np.ndarray, tg: np.ndarray, delta_phi: np.ndarray, t0: float
    ):
        """
        Calculate s parameter.

        Arguments
        ---------
        b : (2,4) np.ndarray
        tg : (2,4) np.ndarray
        delta_phi : (2,4) np.ndarray
        t0 : float

        Returns
        -------
        s : (2,4) np.ndarray
        """
        s = (b * tg) / (t0 * delta_phi)

        return s

    @staticmethod
    def calculate_logkw(logk0: np.ndarray, s: np.ndarray, phi0_init: float):
        """
        Calculate logkw parameter - retention in water

        Arguments
        ---------
        logk0 : (2,4) np.ndarray
        s : (2,4) np.ndarray
        phi0_init : float

        Returns
        -------
        logkw : (2,4) np.ndarray
        """
        logkw = logk0 + (s * phi0_init)
        return logkw

    @staticmethod
    def estimate_N(
        logk0: np.ndarray, b: np.ndarray, w: np.ndarray, t0: float, td: float
    ):
        """
        Calculate N parameter - resolution number

        Arguments
        ---------
        logk0 : (2,4) np.ndarray
        b : (2,4) np.ndarray
        w : (2,4) np.ndarray
        t0 : float
        td : float

        Returns
        -------
        logkw : (2,4) np.ndarray
        """
        k_star = (10 ** logk0) / (2.3 * b * ((10 ** logk0) / 2) - (t0 / td) + 1)

        N = (4 * ((k_star + 2) ** 2) * (t0 ** 2)) / w ** 2

        return N


class RetentionWidthEquations:
    def calculate_logk0(logkw: np.ndarray, s: np.ndarray, phi0: float):
        """
        Calculate logk0.

        Arguments
        ---------
        logkw : (4,) np.ndarray
        s : (4,) np.ndarray
        phi0 : float

        Returns
        -------
        logk0 : (4,) np.ndarray
        """
        logk0 = logkw - (s * phi0)

        return logk0

    def calculate_b(s: np.ndarray, t0: float, delta_phi: float, tg_final: float):
        """
        Calculate b.

        Arguments
        ---------
        s : (4,) np.ndarray
        t0 : float
        delta_phi : float
        tg_final : float

        Returns
        -------
        b : (4,) np.ndarray
        """
        b = (s * t0 * delta_phi) / tg_final

        return b

    def calculate_tr_smallk0(t0: float, logk0: np.ndarray):
        """
        Calculate retention time when k0 is small.

        Arguments
        ---------
        t0 : float
        logk0 : (4,) np.ndarray

        Returns
        -------
        tr : (4,) np.ndarray
        """
        tr = t0 * (1 + (10 ** logk0))

        return tr

    def calculate_tr_largek0(t0: float, td: float, b: np.ndarray, logk0: np.ndarray):
        """
        Calculate retention time when k0 is large.

        Arguments
        ---------
        t0 : float
        td : float
        b : (4,) np.ndarray
        logk0 : (4,) np.ndarray

        Returns
        -------
        tr : (4,) np.ndarray
        """
        tr = (
            (t0 / b)
            * np.log10(2.3 * (10 ** logk0) * b * (1 - (td / (t0 * (10 ** logk0)))) + 1)
            + t0
            + td
        )

        return tr

    def calculate_w(logk0: np.ndarray, b: np.ndarray, N: np.ndarray, t0: float, td: float):
        """
        Calculate peak width.

        Arguments
        ---------
        logk0 : (4,) np.ndarray
        b : (4,) np.ndarray
        N : (4,) np.ndarray
        t0 : float
        td : float

        Returns
        -------
        w : (4,) np.ndarray
        """
        k_star = (10 ** logk0) / (2.3 * b * ((10 ** logk0) / 2) - (t0 / td) + 1)

        w = (4 * (N ** (-1 / 2))) * t0 * (1 + (k_star / 2))

        return w


class ResolutionEquations:
    def calculate_res(tr1: np.ndarray, tr2: np.ndarray, w1: np.ndarray, w2: np.ndarray):
        """
        Calculate resolution
        """
        res = np.sqrt((2 * (tr2 - tr1) / (w1 + w2)) ** 2)
        return res
