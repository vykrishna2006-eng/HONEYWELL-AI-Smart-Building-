"""
Simulation Routes
"""

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from energyplus.config import IDF_FILE, ENERGYPLUS_EXE

router = APIRouter(
    prefix="/simulation",
    tags=["Simulation"],
)

REPORTS_DIR = IDF_FILE.parent.parent / "reports"


@router.post("/run")
async def run_simulation():
    """
    Run EnergyPlus simulation and return detailed status.
    Returns success result or a structured error response
    with diagnosis so the frontend can show meaningful feedback.
    """
    from energyplus.runner import run_energyplus
    from energyplus.parser import parse_results

    # Check pre-conditions before attempting to run
    exe_path = Path(ENERGYPLUS_EXE)
    idf_path = IDF_FILE
    weather_path = IDF_FILE.parent.parent / "weather" / "weather.epw"

    missing = []
    if not exe_path.exists():
        missing.append({
            "item":    "EnergyPlus executable",
            "path":    str(exe_path),
            "fix":     f"Install EnergyPlus at {exe_path}. "
                       "Download from https://energyplus.net/downloads",
        })
    if not idf_path.exists():
        missing.append({
            "item": "Building IDF file",
            "path": str(idf_path),
            "fix":  "Ensure energyplus/idf/building.idf exists.",
        })
    if not weather_path.exists():
        missing.append({
            "item": "Weather EPW file",
            "path": str(weather_path),
            "fix":  "Ensure energyplus/weather/weather.epw exists.",
        })

    if missing:
        return JSONResponse(
            status_code=200,          # keep 200 so frontend can read body
            content={
                "status":  "error",
                "code":    "MISSING_FILES",
                "message": "EnergyPlus simulation could not start — required files are missing.",
                "missing": missing,
            },
        )

    # Run the simulation
    try:
        result = run_energyplus()
    except Exception as exc:
        return JSONResponse(
            status_code=200,
            content={
                "status":  "error",
                "code":    "RUNNER_EXCEPTION",
                "message": f"EnergyPlus runner raised an exception: {exc}",
                "stdout":  "",
                "stderr":  "",
            },
        )

    if not result["success"]:
        # Parse stderr for common EnergyPlus errors
        stderr = result.get("stderr", "")
        stdout = result.get("stdout", "")

        # Auto-restore IDF from backup if it's a thermostat setpoint error
        combined = (stderr + "\n" + stdout).lower()
        if "dualsetpointwithdeadband" in combined or "heating set-point higher" in combined:
            try:
                import shutil
                backup = IDF_FILE.with_suffix(".idf.bak")
                baseline = IDF_FILE.parent / "versions" / "building_baseline.idf"
                restored_from = None
                if backup.exists():
                    shutil.copy(backup, IDF_FILE)
                    restored_from = str(backup)
                elif baseline.exists():
                    shutil.copy(baseline, IDF_FILE)
                    restored_from = str(baseline)
                if restored_from:
                    print(f"[simulation] IDF auto-restored from {restored_from}")
            except Exception as restore_err:
                print(f"[simulation] IDF restore failed: {restore_err}")

        diagnosis = _diagnose_energyplus_error(stderr + "\n" + stdout)

        return JSONResponse(
            status_code=200,
            content={
                "status":    "error",
                "code":      "ENERGYPLUS_FAILED",
                "message":   "EnergyPlus exited with a non-zero return code.",
                "diagnosis": diagnosis,
                "stdout":    stdout[-2000:] if stdout else "",
                "stderr":    stderr[-2000:] if stderr else "",
            },
        )

    # Success — parse output
    try:
        parsed = parse_results()
    except Exception as exc:
        return JSONResponse(
            status_code=200,
            content={
                "status":  "error",
                "code":    "PARSE_FAILED",
                "message": f"Simulation ran but output could not be parsed: {exc}",
            },
        )

    return {
        "status":  "completed",
        "results": parsed,
    }


def _diagnose_energyplus_error(output: str) -> str:
    """Return a human-readable diagnosis from EnergyPlus output text."""
    output_lower = output.lower()

    # Most common: invalid thermostat setpoints (heating >= cooling)
    if "dualsetpointwithdeadband" in output_lower or (
        "heating set-point higher than" in output_lower
    ):
        return (
            "THERMOSTAT ERROR: The heating setpoint is higher than the cooling setpoint "
            "in the IDF. This was caused by an invalid LLM-suggested setpoint being "
            "written to building.idf. The IDF has been automatically restored from the "
            "baseline backup. Click 'Start Simulation' again — the setpoint guard in "
            "idf_editor.py will now prevent this from happening."
        )
    if "severe" in output_lower and "fatal" in output_lower:
        # Extract the last severe error line for display
        lines = output.splitlines()
        severe_lines = [l.strip() for l in lines if "severe" in l.lower() or "fatal" in l.lower()]
        detail = " | ".join(severe_lines[-3:]) if severe_lines else ""
        return (
            f"EnergyPlus encountered a fatal error in the IDF. "
            f"{detail}"
        )
    if "weather file" in output_lower or "epw" in output_lower:
        return (
            "EnergyPlus could not read the weather file. "
            "Verify energyplus/weather/weather.epw is a valid EPW file."
        )
    if "cannot open" in output_lower or "no such file" in output_lower:
        return (
            "A required file could not be opened. "
            "Check that the IDF and EPW paths in energyplus/config.py are correct."
        )
    if "version" in output_lower and "mismatch" in output_lower:
        return (
            "EnergyPlus version mismatch. "
            "The IDF file version may not match your installed EnergyPlus version."
        )
    if not output.strip():
        return (
            "EnergyPlus produced no output. "
            "The executable may have crashed. "
            "Try running it manually: energyplus.exe -w weather.epw -d output building.idf"
        )
    return "Check the stderr/stdout fields below for details."


@router.get("/closed-loop-report")
async def get_closed_loop_report():
    """Returns the latest closed-loop savings report."""
    # Look in energyplus/reports/ first, then reports/
    candidates = [
        REPORTS_DIR / "savings_report.json",
        Path("reports") / "savings_report.json",
    ]
    for report_path in candidates:
        if report_path.exists():
            with open(report_path) as f:
                return json.load(f)

    raise HTTPException(
        status_code=404,
        detail={
            "message": "No closed-loop report found.",
            "fix": "Run the automation controller: python -m automation.controller",
        },
    )


@router.get("/closed-loop-chart")
async def get_closed_loop_chart():
    """Returns the latest closed-loop savings chart image."""
    candidates = [
        REPORTS_DIR / "savings_chart.png",
        Path("reports") / "savings_chart.png",
    ]
    for chart_path in candidates:
        if chart_path.exists():
            return FileResponse(chart_path, media_type="image/png")

    raise HTTPException(
        status_code=404,
        detail={
            "message": "No chart found.",
            "fix": "Run: python -m automation.generate_chart",
        },
    )


@router.get("/status")
async def simulation_status():
    """
    Returns the current status of EnergyPlus setup:
    whether the exe, IDF, and weather file exist.
    """
    exe_path     = Path(ENERGYPLUS_EXE)
    idf_path     = IDF_FILE
    weather_path = IDF_FILE.parent.parent / "weather" / "weather.epw"
    report_csv   = REPORTS_DIR / "savings_report.csv"
    report_json  = REPORTS_DIR / "savings_report.json"

    return {
        "energyplus_exe":    {"path": str(exe_path),     "exists": exe_path.exists()},
        "idf_file":          {"path": str(idf_path),     "exists": idf_path.exists()},
        "weather_file":      {"path": str(weather_path), "exists": weather_path.exists()},
        "report_csv":        {"path": str(report_csv),   "exists": report_csv.exists()},
        "report_json":       {"path": str(report_json),  "exists": report_json.exists()},
        "ready_to_simulate": exe_path.exists() and idf_path.exists() and weather_path.exists(),
    }
