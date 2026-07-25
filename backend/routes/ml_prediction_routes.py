"""
=========================================================
Machine Learning Prediction Routes
=========================================================
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.services.ml_prediction_service import (
    MLPredictionService,
)

from database.database import get_db

from database.schemas.ml_prediction_schema import (
    MLPredictionRequest,
    MLPredictionResponse,
    SimplePredictionRequest,
)

router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"],
)

service = MLPredictionService()


@router.post(
    "/predict",
    response_model=MLPredictionResponse,
)
def predict(
    sensor_data: MLPredictionRequest,
    db: Session = Depends(get_db),
):
    """
    Generate ML prediction, optimize the result,
    save prediction and recommendation to the database,
    and return the response.
    """

    return service.predict(
        db=db,
        sensor_data=sensor_data.model_dump(),
    )


@router.post(
    "/predict-simple",
    response_model=MLPredictionResponse,
)
def predict_simple(
    sensor_data: SimplePredictionRequest,
    db: Session = Depends(get_db),
):
    """
    Generate a prediction from a simplified 5-field input.
    """

    return service.predict_simple(
        db=db,
        simple_data=sensor_data.model_dump(),
    )