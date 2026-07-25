from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.database import get_db

from database.schemas.prediction_schema import (
    PredictionCreate,
    PredictionUpdate,
    PredictionResponse,
)

from backend.services.prediction_service import PredictionService

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


@router.post(
    "/",
    response_model=PredictionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_prediction(
    prediction: PredictionCreate,
    db: Session = Depends(get_db),
):
    return PredictionService.create(db, prediction)


@router.get(
    "/",
    response_model=list[PredictionResponse],
)
def get_predictions(
    db: Session = Depends(get_db),
):
    return PredictionService.get_all(db)


@router.get(
    "/{prediction_id}",
    response_model=PredictionResponse,
)
def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
):
    return PredictionService.get(db, prediction_id)


@router.put(
    "/{prediction_id}",
    response_model=PredictionResponse,
)
def update_prediction(
    prediction_id: int,
    prediction: PredictionUpdate,
    db: Session = Depends(get_db),
):
    return PredictionService.update(
        db,
        prediction_id,
        prediction,
    )


@router.delete("/{prediction_id}")
def delete_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
):
    PredictionService.delete(
        db,
        prediction_id,
    )

    return {
        "message": "Prediction deleted successfully"
    }