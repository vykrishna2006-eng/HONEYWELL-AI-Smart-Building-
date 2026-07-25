import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"


def get_csv_file():
    csv_files = list(OUTPUT_DIR.glob("*.csv"))

    if not csv_files:
        return None

    return csv_files[0]


def parse_results():

    csv_file = get_csv_file()

    if csv_file is None:
        return {
            "success": False,
            "message": "No CSV file found"
        }

    df = pd.read_csv(csv_file)

    return {
        "success": True,
        "file": csv_file.name,
        "rows": len(df),
        "columns": list(df.columns),
        "preview": df.head(10).to_dict(orient="records")
    }


if __name__ == "__main__":
    print(parse_results())