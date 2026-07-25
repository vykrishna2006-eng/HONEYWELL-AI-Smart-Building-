import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"


def get_csv_file():
    target = OUTPUT_DIR / "eplusout.csv"

    if target.exists():
        return target

    return None


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