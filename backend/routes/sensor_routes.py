from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.database import get_db

from database.schemas.sensor_schema import (
    SensorCreate,
    SensorUpdate,
    SensorResponse,
)

from backend.services.sensor_service import SensorService

router = APIRouter(
    prefix="/sensors",
    tags=["Sensors"],
)


@router.post(
    "/",
    response_model=SensorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_sensor(
    sensor: SensorCreate,
    db: Session = Depends(get_db),
):
    return SensorService.create(db, sensor)


@router.get(
    "/",
    response_model=list[SensorResponse],
)
def get_sensors(
    db: Session = Depends(get_db),
):
    return SensorService.get_all(db)


@router.get(
    "/{sensor_id}",
    response_model=SensorResponse,
)
def get_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
):
    return SensorService.get(db, sensor_id)


@router.put(
    "/{sensor_id}",
    response_model=SensorResponse,
)
def update_sensor(
    sensor_id: int,
    sensor: SensorUpdate,
    db: Session = Depends(get_db),
):
    return SensorService.update(
        db,
        sensor_id,
        sensor,
    )


@router.delete("/{sensor_id}")
def delete_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
):
    SensorService.delete(db, sensor_id)

    return {
        "message": "Sensor deleted successfully"
    }