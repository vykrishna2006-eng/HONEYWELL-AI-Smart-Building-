from fastapi import APIRouter
import pandas as pd
import json
from pathlib import Path

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)

REPORTS_DIR = Path("reports")

CSV_FILE = REPORTS_DIR / "savings_report.csv"
JSON_FILE = REPORTS_DIR / "savings_report.json"


@router.get("/current")
def current():

    if not CSV_FILE.exists():
        return {"error": "savings_report.csv not found"}

    df = pd.read_csv(CSV_FILE)

    latest = df.iloc[-1]

    return {
        "iteration": int(latest["iteration"]),
        "energy": float(latest["energy_kwh"]),
        "cooling_energy": float(latest["cooling_kwh"]),
        "heating_energy": float(latest["heating_kwh"]),
        "pmv": float(latest["pmv"]),
        "ppd": float(latest["ppd"]),
        "occupancy": float(latest["occupancy"]),
        "cooling_setpoint": latest["cooling_setpoint"],
        "heating_setpoint": latest["heating_setpoint"],
        "reason": str(latest["reason"])
    }


@router.get("/history")
def history():

    if not CSV_FILE.exists():
        return []

    df = pd.read_csv(CSV_FILE)

    return df.to_dict(orient="records")


@router.get("/recommendation")
def recommendation():

    if not JSON_FILE.exists():
        return {"error": "savings_report.json not found"}

    with open(JSON_FILE, "r") as f:
        report = json.load(f)

    return report[-1]