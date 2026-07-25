"""
=========================================================
Machine Learning Prediction Service
=========================================================
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.models import Sensor

from database.crud.prediction_crud import create_ml_prediction
from database.crud.recommendation_crud import (
    create_ml_recommendation,
)

from ml.predict import Predictor
from ml.optimization.optimizer import Optimizer


class MLPredictionService:
    """
    Handles Machine Learning prediction,
    optimization, and database persistence.
    """

    def __init__(self):
        self.predictor = Predictor()
        self.optimizer = Optimizer()

    def predict(
        self,
        db: Session,
        sensor_data: dict,
    ) -> dict:
        """
        Generate ML predictions, optimize them,
        store them in the database,
        and return the final response.
        """

        try:

            # =============================================
            # Validate Sensor
            # =============================================

            sensor = (
                db.query(Sensor)
                .filter(
                    Sensor.id == sensor_data["sensor_id"]
                )
                .first()
            )

            if sensor is None:
                raise HTTPException(
                    status_code=404,
                    detail="Sensor not found."
                )

            # =============================================
            # Run Prediction
            # =============================================

            prediction = self.predictor.predict(
                sensor_data
            )

            # =============================================
            # Run Optimizer
            # =============================================

            result = self.optimizer.optimize(
                sensor_data=sensor_data,
                prediction=prediction,
            )

            # =============================================
            # Save Prediction
            # =============================================

            db_prediction = create_ml_prediction(
                db=db,
                sensor_id=sensor.id,
                energy_prediction=result[
                    "predicted_energy_kWh"
                ],
                comfort_prediction=result[
                    "predicted_comfort_score"
                ],
            )

            # =============================================
            # Save Recommendation
            # =============================================

            create_ml_recommendation(
                db=db,
                prediction_id=db_prediction.id,
                recommended_setpoint=result[
                    "recommended_hvac_setpoint"
                ],
                expected_savings=result[
                    "expected_energy_saving_percent"
                ],
                reason="\n".join(
                    result.get(
                        "recommendations",
                        [],
                    )
                ),
                llm_response="Waiting for Gemini recommendation",
            )

            # =============================================
            # Return Result
            # =============================================

            return result

        except HTTPException:
            db.rollback()
            raise

        except Exception as e:
            import traceback
            print("\n========== ERROR ==========")
            traceback.print_exc()
            print("===========================\n")
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )