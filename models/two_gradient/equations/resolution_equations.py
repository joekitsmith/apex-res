import math
import numpy as np

class ResolutionEquations:
    def calculate_res(tr1: np.ndarray, tr2: np.ndarray, w1: np.ndarray, w2: np.ndarray):
        """
        Calculate resolution.

        Arguments
        ---------
        tr1 : (n,) np.ndarray
        tr2 : (n,) np.ndarray
        w1 : (n,) np.ndarray
        w2 : (n,) np.ndarray
        """
        res = np.sqrt((2 * (tr2 - tr1) / (w1 + w2)) ** 2)

        return res
