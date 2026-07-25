import pandas as pd


class DataCleaner:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_data(self) -> pd.DataFrame:
        """
        Load Excel dataset.
        """
        return pd.read_excel(self.file_path)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the dataset.
        """

        print("=" * 60)
        print("Original Dataset Information")
        print("=" * 60)

        print(f"Rows    : {df.shape[0]}")
        print(f"Columns : {df.shape[1]}")

        print("\nMissing Values:")
        print(df.isnull().sum())

        print("\nDuplicate Rows:", df.duplicated().sum())

        # Remove duplicates
        df = df.drop_duplicates()

        # Convert timestamp
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])

        # Fill missing numeric values
        numeric_columns = df.select_dtypes(include=["number"]).columns

        for column in numeric_columns:
            df[column] = df[column].fillna(df[column].median())

        # Fill missing categorical values
        categorical_columns = df.select_dtypes(include=["object"]).columns

        for column in categorical_columns:
            df[column] = df[column].fillna(df[column].mode()[0])

        print("\nCleaning Completed Successfully")
        print("=" * 60)

        return df