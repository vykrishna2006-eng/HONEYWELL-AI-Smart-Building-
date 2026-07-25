from fastapi import APIRouter

from backend.routes.room_routes import (
    router as room_router,
)

from backend.routes.sensor_routes import (
    router as sensor_router,
)

from backend.routes.energy_routes import (
    router as energy_router,
)

from backend.routes.prediction_routes import (
    router as prediction_router,
)

from backend.routes.recommendation_routes import (
    router as recommendation_router,
)

from backend.routes.ml_prediction_routes import (
    router as ml_prediction_router,
)

from backend.routes.analytics_routes import (
    router as analytics_router,
)

from backend.routes.simulation_routes import (
    router as simulation_router,
)

from backend.routes.llm_routes import router as llm_router

api_router = APIRouter()

api_router.include_router(room_router)
api_router.include_router(sensor_router)
api_router.include_router(energy_router)
api_router.include_router(prediction_router)
api_router.include_router(recommendation_router)
api_router.include_router(ml_prediction_router)
api_router.include_router(analytics_router)
api_router.include_router(simulation_router)
api_router.include_router(llm_router)
