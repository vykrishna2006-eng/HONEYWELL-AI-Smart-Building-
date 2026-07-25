"""
=========================================================
Recommendation Schemas
=========================================================
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RecommendationBase(BaseModel):

    prediction_id: int

    recommended_setpoint: float

    expected_savings: float

    reason: str

    llm_response: str


class RecommendationCreate(RecommendationBase):
    pass


class RecommendationUpdate(BaseModel):
    recommended_setpoint: float | None = None
    expected_savings: float | None = None
    reason: str | None = None
    llm_response: str | None = None


class RecommendationResponse(RecommendationBase):
    id: int

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)