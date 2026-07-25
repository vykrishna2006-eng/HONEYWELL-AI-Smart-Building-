"""
=========================================================
Machine Learning Predictor
=========================================================
"""

from typing import Dict

import pandas as pd

from ml.model_loader import ModelLoader
from ml.feature_columns import FEATURE_COLUMNS


class Predictor:
    """
    Generates Energy and Comfort predictions.
    """

    def __init__(self):
        loader = ModelLoader()

        self.energy_model = loader.load_energy_model()
        self.comfort_model = loader.load_comfort_model()

    def predict(self, input_data: Dict):

        try:

            # Create dataframe
            df = pd.DataFrame([input_data])

            # Verify all required features exist
            missing = [
                feature
                for feature in FEATURE_COLUMNS
                if feature not in df.columns
            ]

            if missing:
                raise ValueError(
                    f"Missing features: {missing}"
                )

            # Arrange in training order
            df = df[FEATURE_COLUMNS]

            print("\n==============================")
            print("MODEL TYPE")
            print(type(self.energy_model))
            print(type(self.comfort_model))

            print("\nINPUT DATA")
            print(df)

            print("\nFEATURE ORDER")
            print(list(df.columns))

            # Predictions
            energy_prediction = float(
                self.energy_model.predict(df)[0]
            )

            comfort_prediction = float(
                self.comfort_model.predict(df)[0]
            )

            print("\nENERGY =", energy_prediction)
            print("COMFORT =", comfort_prediction)
            print("==============================\n")

            return {
                "predicted_energy_kWh": round(
                    energy_prediction,
                    2,
                ),
                "predicted_comfort_score": round(
                    comfort_prediction,
                    2,
                ),
            }

        except Exception as e:
            raise Exception(
                f"Prediction failed: {str(e)}"
            )