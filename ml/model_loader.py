from pathlib import Path

import joblib


class ModelLoader:
    """
    Loads trained machine learning models.
    """

    def __init__(self):

        base_dir = Path(__file__).resolve().parent

        self.energy_model_path = (
            base_dir
            / "saved_models"
            / "energy_model.pkl"
        )

        self.comfort_model_path = (
            base_dir
            / "saved_models"
            / "comfort_model.pkl"
        )

        self._energy_model = None
        self._comfort_model = None

    # --------------------------------------------------------
    # Energy Model
    # --------------------------------------------------------

    def load_energy_model(self):

        if self._energy_model is None:
            self._energy_model = joblib.load(self.energy_model_path)

        return self._energy_model

    # --------------------------------------------------------
    # Comfort Model
    # --------------------------------------------------------

    def load_comfort_model(self):

        if self._comfort_model is None:
            self._comfort_model = joblib.load(self.comfort_model_path)

        return self._comfort_model

    # --------------------------------------------------------
    # Load Both
    # --------------------------------------------------------

    def load_models(self):

        return {
            "energy_model": self.load_energy_model(),
            "comfort_model": self.load_comfort_model(),
        }