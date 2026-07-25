from pathlib import Path

from ml.preprocessing.clean_data import DataCleaner
from ml.preprocessing.feature_engineering import FeatureEngineer


# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATASET = BASE_DIR / "datasets" / "raw" / "Smart_Building_Industrial_Dataset_1Year.xlsx"

PROCESSED_DATASET = BASE_DIR / "datasets" / "processed" / "processed_dataset.csv"


def preprocess_dataset():
    """
    Complete preprocessing pipeline.
    """

    print("=" * 60)
    print("SMART BUILDING DATA PREPROCESSING")
    print("=" * 60)

    # -----------------------------
    # Load & Clean
    # -----------------------------
    cleaner = DataCleaner(RAW_DATASET)

    df = cleaner.load_data()

    df = cleaner.clean_data(df)

    # -----------------------------
    # Feature Engineering
    # -----------------------------
    engineer = FeatureEngineer()

    df = engineer.engineer_features(df)

    # -----------------------------
    # Create processed directory
    # -----------------------------
    PROCESSED_DATASET.parent.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # Save dataset
    # -----------------------------
    print(df.columns.tolist())
    print(df.head())
    df.to_csv(PROCESSED_DATASET, index=False)

    print("\nProcessed Dataset Saved Successfully!")

    print(PROCESSED_DATASET)

    print("\nFinal Shape:")

    print(df.shape)

    print("=" * 60)


if __name__ == "__main__":
    preprocess_dataset()