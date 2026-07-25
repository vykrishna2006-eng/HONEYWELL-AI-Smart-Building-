from pathlib import Path
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ml.feature_columns import (
    FEATURE_COLUMNS,
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
    ENERGY_TARGET,
    DROP_COLUMNS,
)


# ======================================================
# Paths
# ======================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    BASE_DIR /
    "datasets" /
    "processed" /
    "processed_dataset.csv"
)

MODEL_PATH = (
    BASE_DIR /
    "ml" /
    "saved_models" /
    "energy_model.pkl"
)


# ======================================================
# Load Dataset
# ======================================================

print("=" * 70)
print("ENERGY MODEL TRAINING")
print("=" * 70)

df = pd.read_csv(DATASET_PATH)

print(f"Dataset Shape : {df.shape}")


# ======================================================
# Remove Unwanted Columns
# ======================================================

df = df.drop(columns=DROP_COLUMNS)

print(f"Shape After Dropping Columns : {df.shape}")


# ======================================================
# Features & Target
# ======================================================

X = df[FEATURE_COLUMNS]

y = df[ENERGY_TARGET]


# ======================================================
# Train/Test Split
# ======================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
)


# ======================================================
# Preprocessing Pipeline
# ======================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            NUMERICAL_FEATURES,
        ),
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            CATEGORICAL_FEATURES,
        ),
    ]
)


# ======================================================
# Machine Learning Model
# ======================================================

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
)


pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ]
)


# ======================================================
# Train
# ======================================================

print("\nTraining Model...")

pipeline.fit(X_train, y_train)

print("Training Completed.")


# ======================================================
# Prediction
# ======================================================

predictions = pipeline.predict(X_test)


# ======================================================
# Evaluation
# ======================================================

mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = mse ** 0.5
r2 = r2_score(y_test, predictions)

print("\nModel Performance")
print("-" * 40)

print(f"MAE  : {mae:.4f}")
print(f"MSE  : {mse:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")


# ======================================================
# Save Model
# ======================================================

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(pipeline, MODEL_PATH)

print("\nModel Saved Successfully!")

print(MODEL_PATH)

print("=" * 70)