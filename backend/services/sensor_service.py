"""
=========================================================
Sensor Service
=========================================================
"""

from sqlalchemy.orm import Session

from database.crud.sensor_crud import (
    create_sensor,
    get_sensor,
    get_sensors,
    update_sensor,
    delete_sensor,
)

from database.schemas.sensor_schema import (
    SensorCreate,
    SensorUpdate,
)

from backend.utils.exceptions import SensorNotFound


class SensorService:

    @staticmethod
    def create(db: Session, sensor: SensorCreate):
        return create_sensor(db, sensor)

    @staticmethod
    def get(db: Session, sensor_id: int):
        sensor = get_sensor(db, sensor_id)

        if sensor is None:
            raise SensorNotFound()

        return sensor

    @staticmethod
    def get_all(db: Session):
        return get_sensors(db)

    @staticmethod
    def update(db: Session, sensor_id: int, sensor_update: SensorUpdate):
        sensor = update_sensor(db, sensor_id, sensor_update)

        if sensor is None:
            raise SensorNotFound()

        return sensor

    @staticmethod
    def delete(db: Session, sensor_id: int):
        sensor = delete_sensor(db, sensor_id)

        if sensor is None:
            raise SensorNotFound()

        return sensor