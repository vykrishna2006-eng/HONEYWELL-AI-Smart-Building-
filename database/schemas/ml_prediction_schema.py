"""
=========================================================
Machine Learning Prediction Schemas
=========================================================
"""

from pydantic import BaseModel, Field


# =====================================================
# Request Schema
# =====================================================

class MLPredictionRequest(BaseModel):

    sensor_id: int = Field(..., gt=0)

    Indoor_Temperature_C: float = Field(..., ge=-20, le=60)
    Outdoor_Temperature_C: float = Field(..., ge=-50, le=60)
    Humidity_Percent: float = Field(..., ge=0, le=100)
    CO2_ppm: float = Field(..., ge=0)
    Occupancy: int = Field(..., ge=0)
    HVAC_Setpoint_C: float = Field(..., ge=16, le=30)
    Lighting_Level_Percent: float = Field(..., ge=0, le=100)
    Equipment_Load_kW: float = Field(..., ge=0)
    Solar_Radiation_Wm2: float = Field(..., ge=0)
    Wind_Speed_mps: float = Field(..., ge=0)
    Electricity_Price_per_kWh: float = Field(..., ge=0)
    Renewable_Generation_kWh: float = Field(..., ge=0)

    Floor: int

    Hour: int = Field(..., ge=0, le=23)
    Day: int = Field(..., ge=1, le=31)
    Month: int = Field(..., ge=1, le=12)
    Year: int = Field(..., ge=2000)
    DayOfWeek: int = Field(..., ge=0, le=6)
    WeekOfYear: int = Field(..., ge=1, le=53)
    Quarter: int = Field(..., ge=1, le=4)
    IsWeekend: int = Field(..., ge=0, le=1)

    Building_ID: str
    Zone: str
    Room_ID: str
    Day_Type: str
    Season: str
    HVAC_Status: str
    HVAC_Mode: str


# =====================================================
# Simplified Request Schema
# =====================================================

class SimplePredictionRequest(BaseModel):

    sensor_id: int = 1
    temperature: float
    humidity: float
    co2: float
    occupancy: int
    hvac_temp: float


# =====================================================
# Response Schema
# =====================================================

class MLPredictionResponse(BaseModel):

    objective: str

    predicted_energy_kWh: float

    predicted_comfort_score: float

    recommended_hvac_setpoint: float

    expected_energy_saving_percent: float

    recommendations: list[str]