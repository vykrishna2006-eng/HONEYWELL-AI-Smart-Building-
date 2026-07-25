from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.api import api_router

from backend.utils.exceptions import (
    RoomNotFound,
    SensorNotFound,
    EnergyNotFound,
    PredictionNotFound,
    RecommendationNotFound,
)

app = FastAPI(
    title="AI Smart Building Optimization API",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "message": "AI Smart Building Optimization API",
        "status": "Running",
    }


# =========================================================
# Global Exception Handlers
# =========================================================

@app.exception_handler(RoomNotFound)
async def room_not_found_handler(
    request: Request,
    exc: RoomNotFound,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message,
        },
    )


@app.exception_handler(SensorNotFound)
async def sensor_not_found_handler(
    request: Request,
    exc: SensorNotFound,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message,
        },
    )


@app.exception_handler(EnergyNotFound)
async def energy_not_found_handler(
    request: Request,
    exc: EnergyNotFound,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message,
        },
    )


@app.exception_handler(PredictionNotFound)
async def prediction_not_found_handler(
    request: Request,
    exc: PredictionNotFound,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message,
        },
    )


@app.exception_handler(RecommendationNotFound)
async def recommendation_not_found_handler(
    request: Request,
    exc: RecommendationNotFound,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message,
        },
    )