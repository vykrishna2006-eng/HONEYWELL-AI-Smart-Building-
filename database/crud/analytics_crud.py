"""
=========================================================
Analytics CRUD Operations
=========================================================
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import Prediction, Recommendation


# =====================================================
# Dashboard Summary
# =====================================================

def get_dashboard_summary(db: Session):
    """
    Get overall dashboard statistics.
    """

    total_predictions = db.query(
        func.count(Prediction.id)
    ).scalar()

    average_energy = db.query(
        func.avg(Prediction.energy_prediction)
    ).scalar()

    average_comfort = db.query(
        func.avg(Prediction.comfort_prediction)
    ).scalar()

    average_savings = db.query(
        func.avg(Recommendation.expected_savings)
    ).scalar()

    return {
        "total_predictions": total_predictions or 0,
        "average_energy_prediction": round(average_energy or 0, 2),
        "average_comfort_score": round(average_comfort or 0, 2),
        "average_expected_savings": round(average_savings or 0, 2),
    }


# =====================================================
# Latest Prediction
# =====================================================

def get_latest_prediction(db: Session):
    """
    Get latest prediction.
    """

    return (
        db.query(Prediction)
        .order_by(Prediction.prediction_time.desc())
        .first()
    )


# =====================================================
# Prediction History
# =====================================================

def get_prediction_history(db: Session):
    """
    Get prediction history.
    """

    return (
        db.query(Prediction)
        .order_by(Prediction.prediction_time.desc())
        .all()
    )


# =====================================================
# Predictions by Sensor
# =====================================================

def get_predictions_by_sensor(
    db: Session,
    sensor_id: int,
):
    """
    Get predictions by sensor.
    """

    return (
        db.query(Prediction)
        .filter(Prediction.sensor_id == sensor_id)
        .order_by(Prediction.prediction_time.desc())
        .all()
    )


# =====================================================
# Latest Recommendation
# =====================================================

def get_latest_recommendation(db: Session):
    """
    Get latest recommendation.
    """

    return (
        db.query(Recommendation)
        .order_by(Recommendation.created_at.desc())
        .first()
    )


# =====================================================
# Recommendation History
# =====================================================

def get_recommendation_history(db: Session):
    """
    Get recommendation history.
    """

    return (
        db.query(Recommendation)
        .order_by(Recommendation.created_at.desc())
        .all()
    )


# =====================================================
# Energy Statistics
# =====================================================

def get_energy_statistics(db: Session):
    """
    Get energy statistics.
    """

    minimum = db.query(
        func.min(Prediction.energy_prediction)
    ).scalar()

    maximum = db.query(
        func.max(Prediction.energy_prediction)
    ).scalar()

    average = db.query(
        func.avg(Prediction.energy_prediction)
    ).scalar()

    return {
        "minimum": round(minimum or 0, 2),
        "maximum": round(maximum or 0, 2),
        "average": round(average or 0, 2),
    }


# =====================================================
# Comfort Statistics
# =====================================================

def get_comfort_statistics(db: Session):
    """
    Get comfort statistics.
    """

    minimum = db.query(
        func.min(Prediction.comfort_prediction)
    ).scalar()

    maximum = db.query(
        func.max(Prediction.comfort_prediction)
    ).scalar()

    average = db.query(
        func.avg(Prediction.comfort_prediction)
    ).scalar()

    return {
        "minimum": round(minimum or 0, 2),
        "maximum": round(maximum or 0, 2),
        "average": round(average or 0, 2),
    }