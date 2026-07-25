from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from ml.feature_columns import (
    FEATURE_COLUMNS,
    ENERGY_TARGET,
    COMFORT_TARGET,
    DROP_COLUMNS,
)


# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    BASE_DIR
    / "datasets"
    / "processed"
    / "processed_dataset.csv"
)

ENERGY_MODEL_PATH = (
    BASE_DIR
    / "ml"
    / "saved_models"
    / "energy_model.pkl"
)

COMFORT_MODEL_PATH = (
    BASE_DIR
    / "ml"
    / "saved_models"
    / "comfort_model.pkl"
)


# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv(DATASET_PATH)

df = df.drop(columns=DROP_COLUMNS)

X = df[FEATURE_COLUMNS]


# ==========================================================
# Load Models
# ==========================================================

energy_model = joblib.load(ENERGY_MODEL_PATH)

comfort_model = joblib.load(COMFORT_MODEL_PATH)


# ==========================================================
# Energy Evaluation
# ==========================================================

print("=" * 70)
print("ENERGY MODEL")
print("=" * 70)

energy_predictions = energy_model.predict(X)

mae = mean_absolute_error(df[ENERGY_TARGET], energy_predictions)
mse = mean_squared_error(df[ENERGY_TARGET], energy_predictions)
rmse = mse ** 0.5
r2 = r2_score(df[ENERGY_TARGET], energy_predictions)

print(f"MAE  : {mae:.4f}")
print(f"MSE  : {mse:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")


# ==========================================================
# Comfort Evaluation
# ==========================================================

print("\n")
print("=" * 70)
print("COMFORT MODEL")
print("=" * 70)

comfort_predictions = comfort_model.predict(X)

mae = mean_absolute_error(df[COMFORT_TARGET], comfort_predictions)
mse = mean_squared_error(df[COMFORT_TARGET], comfort_predictions)
rmse = mse ** 0.5
r2 = r2_score(df[COMFORT_TARGET], comfort_predictions)

print(f"MAE  : {mae:.4f}")
print(f"MSE  : {mse:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")

print("\n")
print("=" * 70)
print("Evaluation Completed Successfully")
print("=" * 70)