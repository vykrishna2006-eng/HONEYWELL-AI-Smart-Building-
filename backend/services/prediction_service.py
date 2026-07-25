"""
=========================================================
Prediction Service
=========================================================
"""

from sqlalchemy.orm import Session

from database.crud.prediction_crud import (
    create_prediction,
    get_prediction,
    get_predictions,
    update_prediction,
    delete_prediction,
)

from database.schemas.prediction_schema import (
    PredictionCreate,
    PredictionUpdate,
)

from backend.utils.exceptions import PredictionNotFound


class PredictionService:

    @staticmethod
    def create(
        db: Session,
        prediction: PredictionCreate,
    ):
        return create_prediction(db, prediction)

    @staticmethod
    def get(
        db: Session,
        prediction_id: int,
    ):
        prediction = get_prediction(db, prediction_id)

        if prediction is None:
            raise PredictionNotFound()

        return prediction

    @staticmethod
    def get_all(
        db: Session,
    ):
        return get_predictions(db)

    @staticmethod
    def update(
        db: Session,
        prediction_id: int,
        prediction_update: PredictionUpdate,
    ):
        prediction = update_prediction(
            db,
            prediction_id,
            prediction_update,
        )

        if prediction is None:
            raise PredictionNotFound()

        return prediction

    @staticmethod
    def delete(
        db: Session,
        prediction_id: int,
    ):
        prediction = delete_prediction(
            db,
            prediction_id,
        )

        if prediction is None:
            raise PredictionNotFound()

        return prediction