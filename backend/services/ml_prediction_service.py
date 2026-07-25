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
from datetime import datetime


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

    # =============================================
    # Simplified Prediction (5-field input)
    # =============================================

    def predict_simple(
        self,
        db: Session,
        simple_data: dict,
    ) -> dict:
        """
        Accepts a simplified 5-field input and fills in
        the rest with sensible defaults before running
        the full prediction pipeline.
        """

        now = datetime.now()
        month = now.month

        if month in (12, 1, 2):
            season = "Winter"
        elif month in (3, 4, 5):
            season = "Spring"
        elif month in (6, 7, 8):
            season = "Summer"
        else:
            season = "Autumn"

        is_weekend = 1 if now.weekday() >= 5 else 0

        full_data = {
            "sensor_id": simple_data.get("sensor_id", 1),
            "Indoor_Temperature_C": simple_data["temperature"],
            "Outdoor_Temperature_C": simple_data["temperature"] - 5,
            "Humidity_Percent": simple_data["humidity"],
            "CO2_ppm": simple_data["co2"],
            "Occupancy": simple_data["occupancy"],
            "HVAC_Setpoint_C": simple_data["hvac_temp"],
            "Lighting_Level_Percent": 70,
            "Equipment_Load_kW": 5,
            "Solar_Radiation_Wm2": 200,
            "Wind_Speed_mps": 3,
            "Electricity_Price_per_kWh": 0.15,
            "Renewable_Generation_kWh": 0,
            "Floor": 1,
            "Hour": now.hour,
            "Day": now.day,
            "Month": now.month,
            "Year": now.year,
            "DayOfWeek": now.weekday(),
            "WeekOfYear": now.isocalendar()[1],
            "Quarter": (now.month - 1) // 3 + 1,
            "IsWeekend": is_weekend,
            "Building_ID": "BLDG_1",
            "Zone": "ZONE_1",
            "Room_ID": "ROOM_1",
            "Day_Type": "Weekend" if is_weekend else "Weekday",
            "Season": season,
            "HVAC_Status": "ON",
            "HVAC_Mode": "AUTO",
        }

        return self.predict(db=db, sensor_data=full_data)