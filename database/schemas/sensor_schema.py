"""
=========================================================
Sensor Schemas
=========================================================
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SensorBase(BaseModel):
    room_id: int

    temperature: float

    humidity: float

    co2: float

    occupancy: int

    lighting: float

    hvac_status: str


class SensorCreate(SensorBase):
    pass


class SensorUpdate(BaseModel):
    temperature: float | None = None
    humidity: float | None = None
    co2: float | None = None
    occupancy: int | None = None
    lighting: float | None = None
    hvac_status: str | None = None


class SensorResponse(SensorBase):
    id: int

    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)