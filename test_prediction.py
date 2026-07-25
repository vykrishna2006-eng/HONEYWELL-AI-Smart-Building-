from ml.predict import Predictor

predictor = Predictor()

sample = {
    "Indoor_Temperature_C": 24.5,
    "Outdoor_Temperature_C": 34.0,
    "Humidity_Percent": 55,
    "CO2_ppm": 700,
    "Occupancy": 18,
    "HVAC_Setpoint_C": 22,
    "Lighting_Level_Percent": 75,
    "Equipment_Load_kW": 12.5,
    "Solar_Radiation_Wm2": 420,
    "Wind_Speed_mps": 4.8,
    "Electricity_Price_per_kWh": 0.18,
    "Renewable_Generation_kWh": 8.5,
    "Floor": 4,
    "Hour": 10,
    "Day": 15,
    "Month": 6,
    "Year": 2025,
    "DayOfWeek": 2,
    "WeekOfYear": 24,
    "Quarter": 2,
    "IsWeekend": 0,
    "Building_ID": "B1",
    "Zone": "Zone-5",
    "Room_ID": "Room-105",
    "Day_Type": "Weekday",
    "Season": "Summer",
    "HVAC_Status": "ON",
    "HVAC_Mode": "Cooling",
}

result = predictor.predict(sample)

print(result)