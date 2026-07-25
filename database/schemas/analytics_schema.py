"""
=========================================================
Analytics Schemas
=========================================================
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


# =====================================================
# Dashboard Summary
# =====================================================

class DashboardSummaryResponse(BaseModel):

    total_predictions: int
    average_energy_prediction: float
    average_comfort_score: float
    average_expected_savings: float

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Prediction Response
# =====================================================

class PredictionAnalyticsResponse(BaseModel):

    id: int
    sensor_id: int
    energy_prediction: float
    comfort_prediction: float
    confidence: float
    model_version: str
    prediction_time: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Recommendation Response
# =====================================================

class RecommendationAnalyticsResponse(BaseModel):

    id: int
    prediction_id: int
    recommended_setpoint: float
    expected_savings: float
    reason: str
    llm_response: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Energy Statistics
# =====================================================

class EnergyStatisticsResponse(BaseModel):

    minimum: float
    maximum: float
    average: float

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Comfort Statistics
# =====================================================

class ComfortStatisticsResponse(BaseModel):

    minimum: float
    maximum: float
    average: float

    model_config = ConfigDict(from_attributes=True)