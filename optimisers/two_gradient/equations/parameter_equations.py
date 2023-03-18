import numpy as np


class ParameterEquations:
    @classmethod
    def estimate_b(
        cls, beta: np.ndarray, tr1: np.ndarray, tr2: np.ndarray, t0: float, td: float
    ):
        """
        Estimate value for gradient factor b from scouting data.

        Arguments
        ---------
        beta : (n,) np.ndarray
        tr1 : (n,) np.ndarray
        tr2 : (n,) np.ndarray
        t0 : float
        td : float

        Returns
        -------
        b : (n,) np.ndarray
        """
        b = np.sqrt(
            (
                (t0 * np.log10(beta))
                / (tr1 - (tr2 / beta) - (t0 + td) * (beta - 1) / beta)
            )
            ** 2
        )

        return b

    @classmethod
    def calculate_logk0(cls, b: np.ndarray, tr: np.ndarray, t0: float, td: float):
        """
        Calculate logk0 value from scouting data.

        Arguments
        ---------
        b : (2,n) np.ndarray
        tr : (2,n) np.ndarray
        t0 : float
        td : float

        Returns
        -------
        logk0_est : (2,n) np.ndarray
        """
        logk0_est = b * (tr - t0 - td) / t0 - np.log10(2.3 * b)

        return logk0_est

    @classmethod
    def retention_f(
        cls,
        b: np.ndarray,
        b_est: np.ndarray,
        logk0_est: np.ndarray,
        tr: np.ndarray,
        t0: float,
        td: float,
    ):
        """
        Function used to optimise value of b by arriving back at retention times in scouting data.
        b varied to minimise difference between estimated and observed retention times.

        Arguments
        ---------
        b : (n,) np.ndarray
        b_est : (2,n) np.ndarray
        logk0_est : (2,n) np.ndarray
        tr : (2,n) np.ndarray
        t0 : float
        td : float

        Returns
        -------
        (2,n) np.ndarray
            differences between estimated and observed retention times
        """
        b_est = b_est.flatten()
        logk0_est = logk0_est.flatten()
        tr = tr.flatten()

        tr_est = (
            (t0 / b_est)
            * np.log10(
                2.3 * (10**logk0_est) * b * (1 - (td / (t0 * (10**logk0_est)))) + 1
            )
            + t0
            + td
        )

        return np.sqrt((tr_est - tr) ** 2)

    @classmethod
    def calculate_s(
        cls, b: np.ndarray, tg: np.ndarray, delta_phi: np.ndarray, t0: float
    ):
        """
        Calculate s parameter.

        Arguments
        ---------
        b : (2,n) np.ndarray
        tg : (2,n) np.ndarray
        delta_phi : (2,n) np.ndarray
        t0 : float

        Returns
        -------
        s : (2,n) np.ndarray
        """
        s = (b * tg) / (t0 * delta_phi)

        return s

    @classmethod
    def calculate_logkw(cls, logk0: np.ndarray, s: np.ndarray, phi0_init: float):
        """
        Calculate logkw parameter - retention in water

        Arguments
        ---------
        logk0 : (2,n) np.ndarray
        s : (2,n) np.ndarray
        phi0_init : float

        Returns
        -------
        logkw : (2,n) np.ndarray
        """
        logkw = logk0 + (s * phi0_init)

        return logkw

    @classmethod
    def estimate_N(
        cls, logk0: np.ndarray, b: np.ndarray, w: np.ndarray, t0: float, td: float
    ):
        """
        Calculate N parameter - resolution number

        Arguments
        ---------
        logk0 : (2,n) np.ndarray
        b : (2,n) np.ndarray
        w : (2,n) np.ndarray
        t0 : float
        td : float

        Returns
        -------
        logkw : (2,n) np.ndarray
        """
        k_star = (10**logk0) / (2.3 * b * ((10**logk0) / 2) - (t0 / td) + 1)

        N = (4 * ((k_star + 2) ** 2) * (t0**2)) / w**2

        return N
