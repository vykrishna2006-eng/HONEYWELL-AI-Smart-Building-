"""
Dashboard Routes
Reads simulation report data from energyplus/reports/ (primary)
with fallback to reports/ (legacy path).
"""

from fastapi import APIRouter
import pandas as pd
import json
import math
from pathlib import Path

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)

# Project root: backend/routes/dashboard_routes.py → 3 levels up
_BASE = Path(__file__).resolve().parent.parent.parent


def _find_report(filename: str) -> Path | None:
    """Search for a report file in known locations."""
    candidates = [
        _BASE / "energyplus" / "reports" / filename,
        _BASE / "reports" / filename,
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def _clean(value):
    """Replace NaN/Inf (not valid JSON) with None."""
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def _clean_record(record: dict) -> dict:
    return {k: _clean(v) for k, v in record.items()}


@router.get("/current")
def current():
    csv_file = _find_report("savings_report.csv")
    if csv_file is None:
        return {"error": "savings_report.csv not found. Run the simulation first."}

    try:
        df = pd.read_csv(csv_file)
        latest = df.iloc[-1].to_dict()
        return _clean_record(latest)
    except Exception as e:
        return {"error": str(e)}


@router.get("/history")
def history():
    csv_file = _find_report("savings_report.csv")
    if csv_file is None:
        return []

    try:
        df = pd.read_csv(csv_file)
        return [_clean_record(r) for r in df.to_dict(orient="records")]
    except Exception:
        return []


@router.get("/recommendation")
def recommendation():
    json_file = _find_report("savings_report.json")
    if json_file is None:
        return {"error": "savings_report.json not found. Run the simulation first."}

    try:
        with open(json_file, "r") as f:
            report = json.load(f)
        return report[-1]
    except Exception as e:
        return {"error": str(e)}
