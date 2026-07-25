"""
=========================================================
Log Schemas
=========================================================
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LogBase(BaseModel):

    module: str

    action: str

    status: str

    message: str


class LogCreate(LogBase):
    pass


class LogResponse(LogBase):
    id: int

    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)