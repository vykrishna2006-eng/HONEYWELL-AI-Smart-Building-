from ml.predict import Predictor
from ml.optimization.optimizer import Optimizer

predictor = Predictor()
optimizer = Optimizer()

sensor_data = {
    "Indoor_Temperature_C": 25,
    "Outdoor_Temperature_C": 34,
    "Humidity_Percent": 65,
    "CO2_ppm": 1200,
    "Occupancy": 40,
    "HVAC_Setpoint_C": 22,
    "Lighting_Level_Percent": 80,
    "Equipment_Load_kW": 14,
    "Solar_Radiation_Wm2": 600,
    "Wind_Speed_mps": 4,
    "Electricity_Price_per_kWh": 0.20,
    "Renewable_Generation_kWh": 5,
    "Floor": 3,
    "Hour": 14,
    "Day": 10,
    "Month": 7,
    "Year": 2025,
    "DayOfWeek": 3,
    "WeekOfYear": 28,
    "Quarter": 3,
    "IsWeekend": 0,
    "Building_ID": "B1",
    "Zone": "Zone-2",
    "Room_ID": "Room-203",
    "Day_Type": "Weekday",
    "Season": "Summer",
    "HVAC_Status": "ON",
    "HVAC_Mode": "Cooling",
}

# Generate predictions
prediction = predictor.predict(sensor_data)

print("\nPrediction")
print(prediction)

# Generate optimization result
result = optimizer.optimize(sensor_data, prediction)

print("\nOptimization")
print(result)