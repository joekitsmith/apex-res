import numpy as np
import scipy.optimize as optimize
import itertools as itertools

from models.two_gradient.equations.parameter_equations import (
    ParameterEquations,
)
from models.two_gradient.equations.retention_width_equations import (
    RetentionWidthEquations,
)
from models.two_gradient.resolution import Resolution


class TwoGradOptimise:
    def __init__(self):
        """
        Parameters
        ----------
        instrument_params : InstrumentParameters
        column_params : ColumnParameters
        method_params : MethodParameters
        input_params : InputParameters
        data : np.ndarray
        """
        ## Instrument
        self.instrument_name = None
        self.td = None
        self.phi0_init = None

        # Column
        self.column_name = None
        self.column_length = None
        self.column_diameter = None
        self.n_est = None
        self.particle_size = None
        self.pore_diameter = None
        self.t0 = None

        ## Method
        self.flow_rate = None
        self.phi0_init = None
        self.phif_init = None
        self.uv = None
        self.tg1 = None
        self.tg2 = None

        ## Data
        self.peak_of_interest = 2
        self.data = np.zeros((8, 3, 2))

        ## Resolution
        self.phi0 = None
        self.phif = None
        self.delta_phi = None
        self.tg = None
        self.tg_final = None

        self.total_res = 0
        self.critical_res = 0

        ## Graph
        self.y_max = 0

        self.is_initialised = False

    def initialise(self):
        print(self.data)
        self.tr = self.data[:, 0][np.all(self.data[:, 0] == 0, axis=1)]
        self.tr1 = self.tr[0]
        self.tr2 = self.tr[1]

        self.w = self.data[:, 1][np.all(self.data[:, 1] == 0, axis=1)]
        self.w1 = self.w[0]
        self.w2 = self.w[1]

        self.area = self.data[:, 2][np.all(self.data[:, 2] == 0, axis=1)]
        self.area1 = self.area[0]
        self.area2 = self.area[1]

        self.number_of_peaks = sum(np.all(self.tr == 0, axis=1))

        self.phi0 = np.array([float(self.phi0_init)] * self.number_of_peaks)
        self.phif = np.array([float(self.phif_init)] * self.number_of_peaks)
        self.delta_phi = np.subtract(self.phif, self.phi0)
        self.tg_final = np.array([float(self.tg1)] * self.number_of_peaks)

        self.is_initialised = True

    def calculate(self):
        """
        Calculate s, logkw and N values.
        """
        print(f"{self.tr=}")
        print(f"{self.w=}")
        print(f"{self.area=}")
        print(f"{self.number_of_peaks=}")
        print(f"{self.phi0_init=}")
        print(f"{self.phif_init=}")
        print(f"{self.phi0=}")
        print(f"{self.phif=}")
        print(f"{self.delta_phi=}")
        print(f"{self.tg1=}")
        print(f"{self.tg2=}")
        print(f"{self.tg_final=}")
        # generate mesh arrays for vectorisation
        beta_np, tr_np, w_np, tg_np, delta_phi_np = self._generate_mesh_arrays()

        # estimate b and logk0
        b_est = self._estimate_b(beta_np, tr_np)
        logk0_est = ParameterEquations.calculate_logk0(b_est, tr_np, self.t0, self.td)

        # optimise value of b
        b_opt = self._optimise_b(b_est, logk0_est, tr_np)

        # calculate s, logkw and N
        self.s, self.logkw, self.n = self._calculate_parameters(
            b_opt, tr_np, w_np, tg_np, delta_phi_np
        )

    def predict(self):
        """
        Predict retention times and widths of peaks under set conditions.
        """
        self.delta_phi = self.phif - self.phi0

        logk0 = RetentionWidthEquations.calculate_logk0(self.logkw, self.s, self.phi0)
        b = RetentionWidthEquations.calculate_b(
            self.s, self.delta_phi, self.tg_final, self.t0
        )

        self._predict_retention(logk0, b)
        self._predict_width(logk0, b)

        self.total_res, self.critical_res = Resolution.predict_resolution(
            self.tr_pred, self.w_pred, self.tg_final, self.peak_of_interest
        )

    def _calculate_parameters(
        self,
        b_opt: np.ndarray,
        tr_np: np.ndarray,
        w_np: np.ndarray,
        tg_np: np.ndarray,
        delta_phi_np: np.ndarray,
    ):
        """
        Calculate s, logkw and N parameters.

        Arguments
        ---------
        b_opt : (2,n) np.ndarray
        tr_np : (2,n) np.ndarray
        w_np : (2,n) np.ndarray
        tg_np : (2,n) np.ndarray
        delta_phi_np : (4,n) np.ndarray

        Returns
        -------
        s_avg : (n,) np.ndarray
        logkw_avg : (n,) np.ndarray
        N_avg : (n,) np.ndarray
        """
        s = ParameterEquations.calculate_s(b_opt, tg_np, delta_phi_np, self.t0)
        logk0 = ParameterEquations.calculate_logk0(b_opt, tr_np, self.t0, self.td)
        logkw = ParameterEquations.calculate_logkw(logk0, s, self.phi0_init)
        # N = ParameterEquations.estimate_N(logk0, b_opt, w_np, self.t0, self.td) # calculate N using peak width
        N = np.array([self.n_est] * self.number_of_peaks)

        # determine average between both runs
        s_avg = s.mean(axis=0)
        logkw_avg = logkw.mean(axis=0)
        N_avg = N.mean(axis=0)

        return (s_avg, logkw_avg, N_avg)

    def _generate_mesh_arrays(self):
        """
        Generate all mesh arrays.

        Returns
        -------
        beta_np : (2,n) np.ndarray
        tr_np : (2,n) np.ndarray
        w_np : (2,n) np.ndarray
        tg_np : (2,n) np.ndarray
        delta_phi_np : (2,n) np.ndarray
        """
        beta_np, tr_np, w_np = self._beta_mesh_arrays()

        tg1 = np.full_like(beta_np[0], self.tg1)
        tg2 = np.full_like(beta_np[1], self.tg2)
        tg_np = np.vstack((tg1, tg2))

        delta_phi_np = np.full_like(beta_np, self.phif_init - self.phi0_init)

        return (beta_np, tr_np, w_np, tg_np, delta_phi_np)

    def _beta_mesh_arrays(self):
        """
        Generate mesh arrays with 2-element beta array if value is already numpy array.
        """
        # list of numpy array values
        mesh_values = [self.tr.T, self.w.T]

        # 2-element beta numpy array
        beta = np.array([self.tg2 / self.tg1, self.tg1 / self.tg2])

        combined_values = []
        for i in mesh_values:
            mesh = np.meshgrid(i, beta)

            # reshape to (4,n) array
            value_np = mesh[0].reshape(4, self.number_of_peaks)
            beta_np = mesh[1].reshape(4, self.number_of_peaks)

            value_np = value_np[0:2]
            beta_np = beta_np[[0, 2]]

            combined_values.append(value_np)

        combined_values.insert(0, beta_np)

        return combined_values

    def _estimate_b(self, beta_np: np.ndarray, tr_np: np.ndarray):
        tr1_np = tr_np[0]
        tr2_np = tr_np[1]
        beta1_np = beta_np[0]
        beta2_np = beta_np[1]

        b_est_1 = ParameterEquations.estimate_b(
            beta1_np, tr1_np, tr2_np, self.t0, self.td
        )
        b_est_2 = ParameterEquations.estimate_b(
            beta2_np, tr2_np, tr1_np, self.t0, self.td
        )

        b_est = np.vstack((b_est_1, b_est_2))

        return b_est

    def _optimise_b(self, b_est, logk0_est, tr_np):
        b_opt = optimize.root(
            ParameterEquations.retention_f,
            b_est,
            args=(b_est, logk0_est, tr_np, self.t0, self.td),
        ).x
        b_opt = np.reshape(b_opt, b_est.shape)

        return b_opt

    def _predict_retention(self, logk0, b):
        tr = np.zeros_like(self.s)
        smallk0 = np.where((self.t0 * (10**logk0)) <= self.td)
        tr[smallk0] = RetentionWidthEquations.calculate_tr_smallk0(
            self.t0, logk0[smallk0]
        )
        largek0 = np.where(tr == 0)
        tr[largek0] = RetentionWidthEquations.calculate_tr_largek0(
            self.t0, self.td, b[largek0], logk0[largek0]
        )

        beforedelay = np.where(tr < self.t0)
        tr[beforedelay] = self.t0

        self.tr_pred = tr

    def _predict_width(self, logk0, b):
        w = RetentionWidthEquations.calculate_w(logk0, b, self.n, self.t0, self.td)

        self.w_pred = w
