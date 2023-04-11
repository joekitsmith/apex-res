from pydantic import BaseModel


class GradientTimeConditions(BaseModel):
    first: float
    second: float


class GradientSolventConditions(BaseModel):
    initial: float
    final: float


class ResolutionResult(BaseModel):
    total: float
    critical: float


class PredictionResult(BaseModel):
    conditions: GradientSolventConditions
    retention_times: list
    widths: list
    areas: list
    resolution: ResolutionResult


class PredictionResponse(BaseModel):
    optimum: PredictionResult
    results: list


class InitialisedResponse(BaseModel):
    is_initialised: bool


class InstrumentParameters(BaseModel):
    dwell_time: float
    dead_time: float
    N: float


class PeakDataItem(BaseModel):
    name: str
    retention_time_first: float
    retention_time_second: float
    width_first: float
    width_second: float
    area_first: float
    area_second: float


class MethodParameters(BaseModel):
    gradient_time: GradientTimeConditions
    gradient_solvent: GradientSolventConditions
