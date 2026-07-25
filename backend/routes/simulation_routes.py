from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from energyplus.simulator import simulate
from energyplus.config import IDF_FILE

router = APIRouter(
    prefix="/simulation",
    tags=["Simulation"],
)

REPORTS_DIR = IDF_FILE.parent.parent / "reports"


@router.post("/run")
async def run_simulation():
    return simulate()


@router.get("/closed-loop-report")
async def get_closed_loop_report():
    """
    Returns the latest closed-loop savings report
    (energy per iteration + LLM decisions).
    """

    import json

    report_path = REPORTS_DIR / "savings_report.json"

    if not report_path.exists():
        raise HTTPException(
            status_code=404,
            detail="No closed-loop report found. Run automation.controller first.",
        )

    with open(report_path) as f:
        return json.load(f)


@router.get("/closed-loop-chart")
async def get_closed_loop_chart():
    """
    Returns the latest closed-loop savings chart image.
    """

    chart_path = REPORTS_DIR / "savings_chart.png"

    if not chart_path.exists():
        raise HTTPException(
            status_code=404,
            detail="No chart found. Run automation.generate_chart first.",
        )

    return FileResponse(chart_path, media_type="image/png")