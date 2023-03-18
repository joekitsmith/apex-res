import itertools
import math

import numpy as np

from optimisers.two_gradient.equations.resolution_equations import ResolutionEquations


class Resolution:
    RESOLUTION = 100

    @classmethod
    def maximise_resolution(cls, optimiser):
        """
        Identify conditions that exhibit maximum resolution.
        """
        # generate all phi0 and phif values and pair up in mesh
        m = np.linspace(0, 1, cls.RESOLUTION)
        n = np.linspace(0, 1, cls.RESOLUTION)
        o = np.array(np.meshgrid(m, n))
        p = o.transpose()
        # remove pairing if difference below 0.15
        valid = np.where((o[0] - o[1] >= 0.15))
        conditions = np.array(p[valid])

        # conditions (conditions, 2)

        optimiser.phi0 = np.repeat(
            conditions[:, 0][np.newaxis, ...], optimiser.number_of_peaks, axis=0
        )
        # phi0 (number_of_peaks, conditions)
        optimiser.phif = np.repeat(
            conditions[:, 1][np.newaxis, ...], optimiser.number_of_peaks, axis=0
        )
        # phif (number_of_peaks, conditions)

        optimiser.predict()

        max_critical_res_idx = np.nanargmax(optimiser.critical_res)

        max_condition = conditions[max_critical_res_idx]
        total_res = optimiser.total_res[max_critical_res_idx]
        critical_res = optimiser.critical_res[max_critical_res_idx]

        optimiser.phi0, optimiser.phif = max_condition

        return max_condition, total_res, critical_res

    @classmethod
    def predict_resolution(cls, tr_pred, w_pred, tg_final, peak_of_interest):
        index_array = np.repeat(
            np.arange(0, len(tr_pred), 1)[..., np.newaxis], tr_pred.shape[1], axis=-1
        )

        tr_w_i = np.stack(
            (
                tr_pred,
                w_pred,
                index_array,
            ),
            axis=1,
        )

        tr_w_i_comb = np.array(list(itertools.combinations(tr_w_i, 2))).T

        tr = tr_w_i_comb[:, 0, :, :]
        tr1 = tr[:, 0, :]
        tr2 = tr[:, 1, :]

        w = tr_w_i_comb[:, 1, :, :]
        w1 = w[:, 0, :]
        w2 = w[:, 1, :]

        i = tr_w_i_comb[:, 2, :, :]
        i1 = i[:, 0, :]
        i2 = i[:, 1, :]

        tg_final = np.repeat(tg_final[np.newaxis, ...], tr1.shape[0], axis=0)

        total_res = cls.calculate_total_resolution(tr1, tr2, w1, w2, tg_final)
        critical_res = cls.calculate_critical_resolution(
            tr1, tr2, w1, w2, i1, i2, tg_final, peak_of_interest
        )

        return (total_res, critical_res)

    @classmethod
    def calculate_critical_resolution(
        cls, tr1, tr2, w1, w2, i1, i2, tg_final, peak_of_interest
    ):
        critical_res = np.zeros_like(tr1)

        # filter for only peak of interest and within gradient time
        interest = ((i1 == peak_of_interest - 1)) | ((i2 == peak_of_interest - 1))
        critical_res[interest] = ResolutionEquations.calculate_res(
            tr1[interest], tr2[interest], w1[interest], w2[interest]
        )

        # convert any zeros to nan
        critical_res[critical_res == 0] = np.nan

        critical_res = np.nanmax(critical_res, axis=1)

        # TODO: not sure what this did
        # critical_res = np.delete(critical_res, (0), axis=0)

        return critical_res

    @classmethod
    def calculate_total_resolution(cls, tr1, tr2, w1, w2, tg_final):
        total_res = np.zeros_like(tr1)

        # filter for peaks within gradient time
        valid = (tr1 < tg_final) | (tr2 < tg_final)
        total_res[valid] = ResolutionEquations.calculate_res(
            tr1[valid], tr2[valid], w1[valid], w2[valid]
        )

        total_res = np.sum(total_res, axis=1)

        return total_res
