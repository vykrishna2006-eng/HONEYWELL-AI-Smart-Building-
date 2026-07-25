"""
=========================================================
Sensor CRUD Operations
=========================================================
"""

from sqlalchemy.orm import Session

from database.models import Sensor

from database.schemas.sensor_schema import (
    SensorCreate,
    SensorUpdate,
)


def create_sensor(db: Session, sensor: SensorCreate):

    db_sensor = Sensor(**sensor.model_dump())

    db.add(db_sensor)

    db.commit()

    db.refresh(db_sensor)

    return db_sensor


def get_sensor(db: Session, sensor_id: int):

    return db.query(Sensor).filter(
        Sensor.id == sensor_id
    ).first()


def get_sensors(db: Session):

    return db.query(Sensor).all()


def update_sensor(
        db: Session,
        sensor_id: int,
        sensor_update: SensorUpdate
):

    sensor = get_sensor(db, sensor_id)

    if sensor is None:

        return None

    update_data = sensor_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():

        setattr(sensor, key, value)

    db.commit()

    db.refresh(sensor)

    return sensor


def delete_sensor(
        db: Session,
        sensor_id: int
):

    sensor = get_sensor(db, sensor_id)

    if sensor is None:

        return None

    db.delete(sensor)

    db.commit()

    return sensor