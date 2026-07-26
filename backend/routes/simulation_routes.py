"""
Simulation Routes

Requirement 1 — EnergyPlus engine via subprocess
Requirement 2 — MCP agentic tools
Requirement 3 — Closed-loop: single-run + full optimisation loop
"""

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse

from energyplus.config import IDF_FILE, ENERGYPLUS_EXE

router = APIRouter(
    prefix="/simulation",
    tags=["Simulation"],
)

REPORTS_DIR = IDF_FILE.parent.parent / "reports"


# ── /simulation/run  (single EnergyPlus run) ─────────────
@router.post("/run")
async def run_simulation():
    """
    Run one EnergyPlus simulation pass.
    Returns structured success/error response the frontend can display.
    """
    from energyplus.runner  import run_energyplus
    from energyplus.parser  import parse_results

    exe_path     = Path(ENERGYPLUS_EXE)
    idf_path     = IDF_FILE
    weather_path = IDF_FILE.parent.parent / "weather" / "weather.epw"

    missing = []
    if not exe_path.exists():
        missing.append({
            "item": "EnergyPlus executable",
            "path": str(exe_path),
            "fix":  "Download EnergyPlus from https://energyplus.net/downloads "
                    f"and install to {exe_path}",
        })
    if not idf_path.exists():
        missing.append({"item": "Building IDF file", "path": str(idf_path),
                         "fix":  "Ensure energyplus/idf/building.idf exists."})
    if not weather_path.exists():
        missing.append({"item": "Weather EPW file",  "path": str(weather_path),
                         "fix":  "Ensure energyplus/weather/weather.epw exists."})

    if missing:
        return JSONResponse(status_code=200, content={
            "status": "error", "code": "MISSING_FILES",
            "message": "Required files are missing — see 'missing' list.",
            "missing": missing,
        })

    try:
        result = run_energyplus()
    except Exception as exc:
        return JSONResponse(status_code=200, content={
            "status": "error", "code": "RUNNER_EXCEPTION",
            "message": str(exc), "stdout": "", "stderr": "",
        })

    if not result["success"]:
        stderr   = result.get("stderr", "")
        stdout   = result.get("stdout", "")
        combined = (stderr + "\n" + stdout).lower()

        # Auto-restore IDF on thermostat error
        if "dualsetpointwithdeadband" in combined or "heating set-point higher" in combined:
            _auto_restore_idf()

        return JSONResponse(status_code=200, content={
            "status":    "error",
            "code":      "ENERGYPLUS_FAILED",
            "message":   "EnergyPlus exited with a non-zero return code.",
            "diagnosis": _diagnose(stderr + "\n" + stdout),
            "stdout":    stdout[-2000:],
            "stderr":    stderr[-2000:],
        })

    try:
        parsed = parse_results()
    except Exception as exc:
        return JSONResponse(status_code=200, content={
            "status": "error", "code": "PARSE_FAILED", "message": str(exc),
        })

    return {"status": "completed", "results": parsed}


# ── /simulation/run-closed-loop  (full AI optimisation) ──
@router.post("/run-closed-loop")
async def run_closed_loop_endpoint(iterations: int = 2):
    """
    Requirement 3 — Full closed-loop execution:
      EnergyPlus → metrics → LLM reasoning → ECMs → IDF injection → repeat.
    Returns the full iteration history.
    This can take several minutes depending on IDF complexity.
    """
    try:
        from automation.controller import run_closed_loop
        history = run_closed_loop(iterations=iterations)
        return {
            "status":     "completed",
            "iterations": len(history),
            "history":    history,
        }
    except Exception as exc:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=200, content={
            "status":  "error",
            "code":    "CLOSED_LOOP_FAILED",
            "message": str(exc),
        })


# ── /simulation/closed-loop-report ───────────────────────
@router.get("/closed-loop-report")
async def get_closed_loop_report():
    """Return the latest saved closed-loop JSON report."""
    for p in [REPORTS_DIR / "savings_report.json", Path("reports") / "savings_report.json"]:
        if p.exists():
            with open(p) as f:
                return json.load(f)
    raise HTTPException(status_code=404, detail={
        "message": "No closed-loop report found.",
        "fix": "Run POST /simulation/run-closed-loop",
    })


# ── /simulation/closed-loop-chart ────────────────────────
@router.get("/closed-loop-chart")
async def get_closed_loop_chart():
    """Return the latest energy savings bar chart image."""
    for p in [REPORTS_DIR / "savings_chart.png", Path("reports") / "savings_chart.png"]:
        if p.exists():
            return FileResponse(p, media_type="image/png")
    raise HTTPException(status_code=404, detail={
        "message": "No chart found. Run POST /simulation/run-closed-loop first.",
    })


# ── /simulation/metrics ──────────────────────────────────
@router.get("/metrics")
async def get_live_metrics():
    """
    Requirement 3 — Feedback: stream continuous performance metrics
    (zone temperatures, IAQ, energy, PMV comfort indices).
    """
    from energyplus.metrics import get_all_metrics
    from ml.comfort import calculate_comfort
    from ml.iaq import calculate_iaq

    metrics = get_all_metrics()

    try:
        comfort = calculate_comfort(
            air_temp=metrics["indoor_temperature"]    or 22.0,
            radiant_temp=metrics["radiant_temperature"] or 22.0,
            humidity=metrics["humidity"]              or 50.0,
            air_speed=metrics["air_speed"]            or 0.15,
        )
        metrics["pmv"] = comfort["pmv"]
        metrics["ppd"] = comfort["ppd"]
    except Exception:
        metrics["pmv"] = None
        metrics["ppd"] = None

    co2 = metrics.get("co2")
    if co2 is not None:
        from ml.iaq import calculate_iaq
        metrics["iaq"] = calculate_iaq(co2)["iaq"]

    return metrics


# ── /simulation/evaluate ─────────────────────────────────
@router.get("/evaluate")
async def evaluate_performance():
    """
    Requirement 3 — Reasoning: evaluate metrics against targets
    (occupancy comfort, peak demand, carbon grid intensity).
    Returns PerformanceFlags.
    """
    from energyplus.metrics import get_all_metrics
    from ml.comfort import calculate_comfort
    from decision_engine.decision import evaluate_metrics

    metrics = get_all_metrics()
    try:
        comfort = calculate_comfort(
            air_temp=metrics["indoor_temperature"]    or 22.0,
            radiant_temp=metrics["radiant_temperature"] or 22.0,
            humidity=metrics["humidity"]              or 50.0,
            air_speed=metrics["air_speed"]            or 0.15,
        )
        metrics["pmv"] = comfort["pmv"]
        metrics["ppd"] = comfort["ppd"]
    except Exception:
        metrics["pmv"] = None
        metrics["ppd"] = None

    flags = evaluate_metrics(metrics)
    return {
        "pmv_ok":           flags.pmv_ok,
        "ppd_ok":           flags.ppd_ok,
        "co2_ok":           flags.co2_ok,
        "peak_demand_high": flags.peak_demand_high,
        "carbon_high":      flags.carbon_high,
        "occupancy_low":    flags.occupancy_low,
        "issues":           flags.reasons,
        "all_targets_met":  not flags.reasons,
    }


# ── /simulation/status ───────────────────────────────────
@router.get("/status")
async def simulation_status():
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


# ── /simulation/errors ───────────────────────────────────
@router.get("/errors")
async def get_simulation_errors():
    """
    Requirement 2 — MCP: parse EnergyPlus .err file and
    extract all runtime errors for LLM diagnosis.
    """
    from energyplus.config import OUTPUT_DIR
    err_file = Path(OUTPUT_DIR) / "eplusout.err"
    if not err_file.exists():
        return {"found": False}

    warnings, severe, fatal = [], [], []
    with open(err_file, encoding="utf-8", errors="replace") as f:
        for line in f:
            low = line.lower()
            if "** warning **" in low:
                warnings.append(line.strip())
            elif "** severe" in low:
                severe.append(line.strip())
            elif "** fatal" in low:
                fatal.append(line.strip())

    return {
        "found":         True,
        "warning_count": len(warnings),
        "severe_count":  len(severe),
        "fatal_count":   len(fatal),
        "warnings":      warnings[-5:],
        "severe_errors": severe,
        "fatal_errors":  fatal,
        "simulation_ok": len(severe) == 0 and len(fatal) == 0,
    }


# ── Helpers ───────────────────────────────────────────────
def _auto_restore_idf():
    import shutil
    for src in [IDF_FILE.with_suffix(".idf.bak"),
                IDF_FILE.parent / "versions" / "building_baseline.idf"]:
        if src.exists():
            shutil.copy(src, IDF_FILE)
            print(f"[simulation] IDF restored from {src}")
            return


def _diagnose(output: str) -> str:
    low = output.lower()
    if "dualsetpointwithdeadband" in low or "heating set-point higher" in low:
        return ("THERMOSTAT ERROR: heating setpoint > cooling setpoint. "
                "IDF has been auto-restored. Click Start Simulation again.")
    if "severe" in low and "fatal" in low:
        lines  = output.splitlines()
        severe = [l.strip() for l in lines if "severe" in l.lower() or "fatal" in l.lower()]
        return "Fatal IDF error: " + " | ".join(severe[-3:])
    if "weather file" in low or "epw" in low:
        return "Cannot read weather file — check energyplus/weather/weather.epw"
    if "cannot open" in low or "no such file" in low:
        return "A required file could not be opened — check IDF and EPW paths"
    if not output.strip():
        return "EnergyPlus produced no output — try running manually"
    return "Check stderr/stdout below for details."
