import numpy as np
from fastapi import APIRouter, HTTPException

from apex_res.optimisers.two_gradient.two_grad_optimise import TwoGradOptimise
from apex_res.schemas.two_gradient import (
    GradientSolventConditions,
    InitialisedResponse,
    InstrumentParameters,
    MethodParameters,
    PeakDataItem,
    PredictionResponse,
    PredictionResult,
    ResolutionResult,
)

two_gradient_router = APIRouter()

optimiser = TwoGradOptimise()


@two_gradient_router.post("/initialise")
async def initialise_model(
    instrument_params: InstrumentParameters,
    method_params: MethodParameters,
    peak_data: list[PeakDataItem],
) -> InitialisedResponse:
    optimiser.t0 = instrument_params.dwell_time
    optimiser.td = instrument_params.dead_time
    optimiser.n_est = instrument_params.N

    optimiser.tg1 = method_params.gradient_time.first
    optimiser.tg2 = method_params.gradient_time.second
    optimiser.phi0_init = method_params.gradient_solvent.initial
    optimiser.phif_init = method_params.gradient_solvent.final

    data = np.array(
        [
            (
                p.retention_time_first,
                p.retention_time_second,
                p.width_first,
                p.width_second,
                p.area_first,
                p.area_second,
            )
            for p in peak_data
        ]
    )
    optimiser.data = data.reshape(len(peak_data), 3, 2)

    optimiser.initialise()

    optimiser.calculate()

    if optimiser.is_initialised:
        return InitialisedResponse(is_initialised=True)

    raise HTTPException(status_code=400, detail="Model not initialised")


@two_gradient_router.get("/predict")
async def predict() -> PredictionResponse:
    RESOLUTION = 101

    # generate all phi0 and phif values and pair up in mesh
    m = np.linspace(0, 1, RESOLUTION)
    n = np.linspace(0, 1, RESOLUTION)
    o = np.array(np.meshgrid(m, n))
    p = o.transpose()
    # remove pairing if difference below 0.15
    valid = np.where((o[0] - o[1] >= 0.15))
    conditions = np.array(p[valid])

    optimiser.phi0 = np.repeat(
        conditions[:, 0][np.newaxis, ...], optimiser.number_of_peaks, axis=0
    )
    optimiser.phif = np.repeat(
        conditions[:, 1][np.newaxis, ...], optimiser.number_of_peaks, axis=0
    )

    optimiser.predict()

    phi0 = (conditions[:, 0]).tolist()
    phif = (conditions[:, 1]).tolist()
    tr_pred = optimiser.tr_pred.T
    w_pred = optimiser.w_pred.T
    area = optimiser.area.mean(axis=1).tolist()

    results = []
    for i, phi0_val in enumerate(phi0):
        results.append(
            PredictionResult(
                conditions=GradientSolventConditions(initial=phi0_val, final=phif[i]),
                retention_times=tr_pred[i].tolist(),
                widths=w_pred[i].tolist(),
                areas=area,
                resolution=ResolutionResult(
                    total=optimiser.total_res[i], critical=optimiser.critical_res[i]
                ),
            )
        )

    optimal_idx = np.nanargmax(optimiser.critical_res)

    optimal_condition = conditions[optimal_idx]
    optimal_tr_pred = tr_pred[optimal_idx].tolist()
    optimal_w_pred = w_pred[optimal_idx].tolist()
    optimal_total_res = optimiser.total_res[optimal_idx]
    optimal_critical_res = optimiser.critical_res[optimal_idx]

    area = optimiser.area.mean(axis=1).tolist()

    return PredictionResponse(
        optimum=PredictionResult(
            conditions=GradientSolventConditions(
                initial=optimal_condition[0], final=optimal_condition[1]
            ),
            retention_times=optimal_tr_pred,
            widths=optimal_w_pred,
            areas=area,
            resolution=ResolutionResult(
                total=optimal_total_res, critical=optimal_critical_res
            ),
        ),
        results=results,
    )
