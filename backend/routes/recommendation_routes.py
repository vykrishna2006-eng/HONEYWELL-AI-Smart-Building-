from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.database import get_db

from database.schemas.recommendation_schema import (
    RecommendationCreate,
    RecommendationUpdate,
    RecommendationResponse,
)

from backend.services.recommendation_service import (
    RecommendationService,
)

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.post(
    "/",
    response_model=RecommendationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_recommendation(
    recommendation: RecommendationCreate,
    db: Session = Depends(get_db),
):
    return RecommendationService.create(
        db,
        recommendation,
    )


@router.get(
    "/",
    response_model=list[RecommendationResponse],
)
def get_recommendations(
    db: Session = Depends(get_db),
):
    return RecommendationService.get_all(db)


@router.get(
    "/{recommendation_id}",
    response_model=RecommendationResponse,
)
def get_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
):
    return RecommendationService.get(
        db,
        recommendation_id,
    )


@router.put(
    "/{recommendation_id}",
    response_model=RecommendationResponse,
)
def update_recommendation(
    recommendation_id: int,
    recommendation: RecommendationUpdate,
    db: Session = Depends(get_db),
):
    return RecommendationService.update(
        db,
        recommendation_id,
        recommendation,
    )


@router.delete("/{recommendation_id}")
def delete_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
):
    RecommendationService.delete(
        db,
        recommendation_id,
    )

    return {
        "message": "Recommendation deleted successfully"
    }