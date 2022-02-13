import math
import numpy as np

class RetentionWidthEquations:
    def calculate_logk0(logkw: np.ndarray, s: np.ndarray, phi0: np.ndarray):
        """
        Calculate logk0.

        Arguments
        ---------
        logkw : (n,) np.ndarray
        s : (n,) np.ndarray
        phi0 : (n,) np.ndarray

        Returns
        -------
        logk0 : (n,) np.ndarray
        """
        logk0 = logkw - (s * phi0)

        return logk0

    def calculate_b(s: np.ndarray, delta_phi: np.ndarray, tg: np.ndarray, t0: float):
        """
        Calculate b.

        Arguments
        ---------
        s : (n,) np.ndarray
        delta_phi : (n,) np.ndarray
        tg_final : (n,) np.ndarray
        t0 : float

        Returns
        -------
        b : (n,) np.ndarray
        """
        b = (s * t0 * delta_phi) / tg

        return b

    def calculate_tr_smallk0(t0: float, logk0: np.ndarray):
        """
        Calculate retention time when k0 is small.

        Arguments
        ---------
        t0 : float
        logk0 : (n,) np.ndarray

        Returns
        -------
        tr : (n,) np.ndarray
        """
        tr = t0 * (1 + (10**logk0))

        return tr

    def calculate_tr_largek0(t0: float, td: float, b: np.ndarray, logk0: np.ndarray):
        """
        Calculate retention time when k0 is large.

        Arguments
        ---------
        t0 : float
        td : float
        b : (n,) np.ndarray
        logk0 : (n,) np.ndarray

        Returns
        -------
        tr : (n,) np.ndarray
        """
        tr = (
            (t0 / b)
            * np.log10(2.3 * (10**logk0) * b * (1 - (td / (t0 * (10**logk0)))) + 1)
            + t0
            + td
        )

        return tr

    def calculate_w(
        logk0: np.ndarray, b: np.ndarray, N: np.ndarray, t0: float, td: float
    ):
        """
        Calculate peak width.

        Arguments
        ---------
        logk0 : (n,) np.ndarray
        b : (n,) np.ndarray
        N : (n,) np.ndarray
        t0 : float
        td : float

        Returns
        -------
        w : (n,) np.ndarray
        """
        k_star = (10**logk0) / (2.3 * b * ((10**logk0) / 2) - (t0 / td) + 1)

        w = (4 * (N ** (-1 / 2))) * t0 * (1 + (k_star / 2))

        return w