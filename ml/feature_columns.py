"""
Feature definitions for the Smart Building ML pipeline.
"""

# =====================================================
# Target Columns
# =====================================================

ENERGY_TARGET = "Energy_Consumption_kWh"

COMFORT_TARGET = "Comfort_Score"


# =====================================================
# Columns Not Used for Training
# =====================================================

DROP_COLUMNS = [
    "Predicted_Energy_kWh",
    "Recommended_HVAC_Setpoint_C",
    "Expected_Energy_Saving_Percent",
    "AI_Action",
]


# =====================================================
# Numerical Features
# =====================================================

NUMERICAL_FEATURES = [
    "Indoor_Temperature_C",
    "Outdoor_Temperature_C",
    "Humidity_Percent",
    "CO2_ppm",
    "Occupancy",
    "HVAC_Setpoint_C",
    "Lighting_Level_Percent",
    "Equipment_Load_kW",
    "Solar_Radiation_Wm2",
    "Wind_Speed_mps",
    "Electricity_Price_per_kWh",
    "Renewable_Generation_kWh",
    "Floor",
    "Hour",
    "Day",
    "Month",
    "Year",
    "DayOfWeek",
    "WeekOfYear",
    "Quarter",
    "IsWeekend",
]


# =====================================================
# Categorical Features
# =====================================================

CATEGORICAL_FEATURES = [
    "Building_ID",
    "Zone",
    "Room_ID",
    "Day_Type",
    "Season",
    "HVAC_Status",
    "HVAC_Mode",
]


# =====================================================
# Complete Feature List
# =====================================================

FEATURE_COLUMNS = NUMERICAL_FEATURES + CATEGORICAL_FEATURES