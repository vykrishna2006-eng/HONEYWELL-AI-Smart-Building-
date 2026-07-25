"""
=========================================================
Room Schemas
=========================================================
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RoomBase(BaseModel):
    room_name: str
    floor: int
    zone: str
    area: float
    capacity: int


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    room_name: str | None = None
    floor: int | None = None
    zone: str | None = None
    area: float | None = None
    capacity: int | None = None


class RoomResponse(RoomBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)