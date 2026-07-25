"""
=========================================================
Recommendation Service
=========================================================
"""

from sqlalchemy.orm import Session

from database.crud.recommendation_crud import (
    create_recommendation,
    get_recommendation,
    get_recommendations,
    update_recommendation,
    delete_recommendation,
)

from database.schemas.recommendation_schema import (
    RecommendationCreate,
    RecommendationUpdate,
)

from backend.utils.exceptions import RecommendationNotFound


class RecommendationService:

    @staticmethod
    def create(
        db: Session,
        recommendation: RecommendationCreate,
    ):
        return create_recommendation(
            db,
            recommendation,
        )

    @staticmethod
    def get(
        db: Session,
        recommendation_id: int,
    ):
        recommendation = get_recommendation(
            db,
            recommendation_id,
        )

        if recommendation is None:
            raise RecommendationNotFound()

        return recommendation

    @staticmethod
    def get_all(
        db: Session,
    ):
        return get_recommendations(db)

    @staticmethod
    def update(
        db: Session,
        recommendation_id: int,
        recommendation_update: RecommendationUpdate,
    ):
        recommendation = update_recommendation(
            db,
            recommendation_id,
            recommendation_update,
        )

        if recommendation is None:
            raise RecommendationNotFound()

        return recommendation

    @staticmethod
    def delete(
        db: Session,
        recommendation_id: int,
    ):
        recommendation = delete_recommendation(
            db,
            recommendation_id,
        )

        if recommendation is None:
            raise RecommendationNotFound()

        return recommendation