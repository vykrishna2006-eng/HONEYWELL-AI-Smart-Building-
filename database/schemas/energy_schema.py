"""
=========================================================
Energy Schemas
=========================================================
"""

from pydantic import BaseModel, ConfigDict


class EnergyBase(BaseModel):
    sensor_id: int

    energy_consumption: float

    renewable_generation: float

    electricity_price: float

    carbon_emission: float


class EnergyCreate(EnergyBase):
    pass


class EnergyUpdate(BaseModel):
    energy_consumption: float | None = None
    renewable_generation: float | None = None
    electricity_price: float | None = None
    carbon_emission: float | None = None


class EnergyResponse(EnergyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)