"""
=========================================================
Analytics Routes
=========================================================
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.services.analytics_service import AnalyticsService

from database.database import get_db

from database.schemas.analytics_schema import (
    DashboardSummaryResponse,
    PredictionAnalyticsResponse,
    RecommendationAnalyticsResponse,
    EnergyStatisticsResponse,
    ComfortStatisticsResponse,
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)

service = AnalyticsService()


# =====================================================
# Dashboard Summary
# =====================================================

@router.get(
    "/dashboard",
    response_model=DashboardSummaryResponse,
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
):
    """
    Get dashboard summary.
    """

    return service.get_dashboard_summary(db)


# =====================================================
# Latest Prediction
# =====================================================

@router.get(
    "/latest-prediction",
    response_model=PredictionAnalyticsResponse,
)
def get_latest_prediction(
    db: Session = Depends(get_db),
):
    """
    Get latest prediction.
    """

    return service.get_latest_prediction(db)


# =====================================================
# Prediction History
# =====================================================

@router.get(
    "/predictions",
    response_model=list[PredictionAnalyticsResponse],
)
def get_prediction_history(
    db: Session = Depends(get_db),
):
    """
    Get all predictions.
    """

    return service.get_prediction_history(db)


# =====================================================
# Predictions by Sensor
# =====================================================

@router.get(
    "/sensor/{sensor_id}",
    response_model=list[PredictionAnalyticsResponse],
)
def get_predictions_by_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
):
    """
    Get prediction history for a sensor.
    """

    return service.get_predictions_by_sensor(
        db,
        sensor_id,
    )


# =====================================================
# Latest Recommendation
# =====================================================

@router.get(
    "/latest-recommendation",
    response_model=RecommendationAnalyticsResponse,
)
def get_latest_recommendation(
    db: Session = Depends(get_db),
):
    """
    Get latest recommendation.
    """

    return service.get_latest_recommendation(db)


# =====================================================
# Recommendation History
# =====================================================

@router.get(
    "/recommendations",
    response_model=list[RecommendationAnalyticsResponse],
)
def get_recommendation_history(
    db: Session = Depends(get_db),
):
    """
    Get recommendation history.
    """

    return service.get_recommendation_history(db)


# =====================================================
# Energy Statistics
# =====================================================

@router.get(
    "/energy",
    response_model=EnergyStatisticsResponse,
)
def get_energy_statistics(
    db: Session = Depends(get_db),
):
    """
    Get energy statistics.
    """

    return service.get_energy_statistics(db)


# =====================================================
# Comfort Statistics
# =====================================================

@router.get(
    "/comfort",
    response_model=ComfortStatisticsResponse,
)
def get_comfort_statistics(
    db: Session = Depends(get_db),
):
    """
    Get comfort statistics.
    """

    return service.get_comfort_statistics(db)