"""
=========================================================
Database Models
=========================================================
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from database.base import Base


# =====================================================
# Rooms
# =====================================================

class Room(Base):

    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)

    room_name: Mapped[str]

    floor: Mapped[int]

    zone: Mapped[str]

    area: Mapped[float]

    capacity: Mapped[int]

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    sensors: Mapped[list["Sensor"]] = relationship(
        back_populates="room",
        cascade="all, delete-orphan",
    )


# =====================================================
# Sensors
# =====================================================

class Sensor(Base):

    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(primary_key=True)

    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id")
    )

    timestamp: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    temperature: Mapped[float]

    humidity: Mapped[float]

    co2: Mapped[float]

    occupancy: Mapped[int]

    lighting: Mapped[float]

    hvac_status: Mapped[str]

    room: Mapped["Room"] = relationship(
        back_populates="sensors"
    )

    energy: Mapped[list["Energy"]] = relationship(
        back_populates="sensor",
        cascade="all, delete-orphan",
    )

    predictions: Mapped[list["Prediction"]] = relationship(
        back_populates="sensor",
        cascade="all, delete-orphan",
    )


# =====================================================
# Energy
# =====================================================

class Energy(Base):

    __tablename__ = "energy"

    id: Mapped[int] = mapped_column(primary_key=True)

    sensor_id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id")
    )

    energy_consumption: Mapped[float]

    renewable_generation: Mapped[float]

    electricity_price: Mapped[float]

    carbon_emission: Mapped[float]

    sensor: Mapped["Sensor"] = relationship(
        back_populates="energy"
    )


# =====================================================
# Prediction
# =====================================================

class Prediction(Base):

    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True)

    sensor_id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id")
    )

    energy_prediction: Mapped[float]

    comfort_prediction: Mapped[float]

    confidence: Mapped[float] = mapped_column(default=1.0)

    model_version: Mapped[str] = mapped_column(
        default="RandomForest_v1.0"
    )

    prediction_time: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    sensor: Mapped["Sensor"] = relationship(
        back_populates="predictions"
    )

    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="prediction",
        cascade="all, delete-orphan",
    )


# =====================================================
# Recommendation
# =====================================================

class Recommendation(Base):

    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)

    prediction_id: Mapped[int] = mapped_column(
        ForeignKey("predictions.id")
    )

    recommended_setpoint: Mapped[float]

    expected_savings: Mapped[float]

    reason: Mapped[str]

    llm_response: Mapped[Optional[str]] = mapped_column(
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    prediction: Mapped["Prediction"] = relationship(
        back_populates="recommendations"
    )


# =====================================================
# Logs
# =====================================================

class Log(Base):

    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    module: Mapped[str]

    action: Mapped[str]

    status: Mapped[str]

    message: Mapped[str]

    timestamp: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )