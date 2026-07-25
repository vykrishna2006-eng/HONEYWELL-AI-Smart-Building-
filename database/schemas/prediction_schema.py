"""
=========================================================
Prediction Schemas
=========================================================
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PredictionBase(BaseModel):

    sensor_id: int

    energy_prediction: float

    comfort_prediction: float

    confidence: float

    model_version: str


class PredictionCreate(PredictionBase):
    pass


class PredictionUpdate(BaseModel):
    energy_prediction: float | None = None
    comfort_prediction: float | None = None
    confidence: float | None = None
    model_version: str | None = None


class PredictionResponse(PredictionBase):
    id: int

    prediction_time: datetime

    model_config = ConfigDict(from_attributes=True)