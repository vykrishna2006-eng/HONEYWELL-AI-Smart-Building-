import pandas as pd


class FeatureEngineer:
    """
    Performs feature engineering on the cleaned dataset.
    """

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Perform feature engineering on the cleaned dataset.
        """

        print("=" * 60)
        print("Feature Engineering Started")
        print("=" * 60)

        # ----------------------------
        # Timestamp Features
        # ----------------------------
        if "Timestamp" in df.columns:

            df["Hour"] = df["Timestamp"].dt.hour
            df["Day"] = df["Timestamp"].dt.day
            df["Month"] = df["Timestamp"].dt.month
            df["Year"] = df["Timestamp"].dt.year
            df["DayOfWeek"] = df["Timestamp"].dt.dayofweek
            df["WeekOfYear"] = df["Timestamp"].dt.isocalendar().week.astype(int)
            df["Quarter"] = df["Timestamp"].dt.quarter

            # Weekend Feature
            df["IsWeekend"] = df["DayOfWeek"].isin([5, 6]).astype(int)

            # Remove original timestamp
            df.drop(columns=["Timestamp"], inplace=True)

        print("\nNew Features Added:")
        print("- Hour")
        print("- Day")
        print("- Month")
        print("- Year")
        print("- DayOfWeek")
        print("- WeekOfYear")
        print("- Quarter")
        print("- IsWeekend")

        print("\nFeature Engineering Completed Successfully")
        print("=" * 60)

        print(f"Final Dataset Shape: {df.shape}")

        return df