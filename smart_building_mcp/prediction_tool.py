from backend.services.ml_prediction_service import MLPredictionService
from database.database import SessionLocal

service = MLPredictionService()

def predict(sensor_data: dict):
    print("\n========== RECEIVED ==========")
    print(sensor_data)
    print(type(sensor_data))
    print("==============================")

    db = SessionLocal()
    try:
        return service.predict(db, sensor_data)
    finally:
        db.close()