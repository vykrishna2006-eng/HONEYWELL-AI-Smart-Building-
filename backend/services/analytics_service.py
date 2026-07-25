"""
=========================================================
Analytics Service
=========================================================
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.crud.analytics_crud import (
    get_dashboard_summary,
    get_latest_prediction,
    get_prediction_history,
    get_predictions_by_sensor,
    get_latest_recommendation,
    get_recommendation_history,
    get_energy_statistics,
    get_comfort_statistics,
)


class AnalyticsService:
    """
    Handles analytics and dashboard data retrieval.
    """

    # =====================================================
    # Dashboard Summary
    # =====================================================

    def get_dashboard_summary(
        self,
        db: Session,
    ):
        """
        Get dashboard summary statistics.
        """

        return get_dashboard_summary(db)

    # =====================================================
    # Latest Prediction
    # =====================================================

    def get_latest_prediction(
        self,
        db: Session,
    ):
        """
        Get latest prediction.
        """

        prediction = get_latest_prediction(db)

        if prediction is None:
            raise HTTPException(
                status_code=404,
                detail="No prediction found."
            )

        return prediction

    # =====================================================
    # Prediction History
    # =====================================================

    def get_prediction_history(
        self,
        db: Session,
    ):
        """
        Get prediction history.
        """

        return get_prediction_history(db)

    # =====================================================
    # Predictions by Sensor
    # =====================================================

    def get_predictions_by_sensor(
        self,
        db: Session,
        sensor_id: int,
    ):
        """
        Get predictions for a sensor.
        """

        return get_predictions_by_sensor(
            db,
            sensor_id,
        )

    # =====================================================
    # Latest Recommendation
    # =====================================================

    def get_latest_recommendation(
        self,
        db: Session,
    ):
        """
        Get latest recommendation.
        """

        recommendation = get_latest_recommendation(db)

        if recommendation is None:
            raise HTTPException(
                status_code=404,
                detail="No recommendation found."
            )

        return recommendation

    # =====================================================
    # Recommendation History
    # =====================================================

    def get_recommendation_history(
        self,
        db: Session,
    ):
        """
        Get recommendation history.
        """

        return get_recommendation_history(db)

    # =====================================================
    # Energy Statistics
    # =====================================================

    def get_energy_statistics(
        self,
        db: Session,
    ):
        """
        Get energy statistics.
        """

        return get_energy_statistics(db)

    # =====================================================
    # Comfort Statistics
    # =====================================================

    def get_comfort_statistics(
        self,
        db: Session,
    ):
        """
        Get comfort statistics.
        """

        return get_comfort_statistics(db)