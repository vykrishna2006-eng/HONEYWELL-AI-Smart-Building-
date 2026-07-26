"""
=========================================================
AI Smart Building — MCP Server  (Requirement 2)

"Implement an MCP Server or custom agentic tools.
 The LLM must use these tools to parse files, extract
 runtime errors, and execute tasks without human code
 modification."

Tools provided:
  REQ 1 – EnergyPlus + eppy bridge
    run_simulation           – run EnergyPlus
    parse_simulation_output  – read eplusout.csv
    inspect_idf              – eppy IDF summary
    get_idf_setpoints        – eppy setpoint reader
    list_idf_objects         – eppy object inspector

  REQ 2 – Error extraction + MCP
    extract_energyplus_errors – parse eplusout.err

  REQ 3 – Closed-Loop
    stream_building_metrics       – Feedback: zone temps/IAQ/PMV
    evaluate_against_targets      – Reasoning: target evaluation
    inject_setpoints              – Forward injection → IDF
    run_closed_loop_optimisation  – Full loop execution

  ML / Analytics
    predict_energy_comfort
    get_building_analytics
    get_llm_recommendation

Run standalone: python -m smart_building_mcp.server
=========================================================
"""

from fastmcp import FastMCP

from smart_building_mcp.analytics_tool      import get_dashboard
from smart_building_mcp.prediction_tool     import predict
from smart_building_mcp.simulation_tool     import simulation
from smart_building_mcp.recommendation_tool import recommendation

mcp = FastMCP("AI Smart Building MCP")


# ═══════════════════════════════════════════════════════════
# REQ 1 — EnergyPlus Engine + eppy IDF bridge
# ═══════════════════════════════════════════════════════════

@mcp.tool
def run_simulation() -> dict:
    """
    Run a full EnergyPlus building energy simulation.
    Returns simulation status, row count, and column list.
    Req 1: Utilise EnergyPlus for high-fidelity simulations.
    """
    return simulation()


@mcp.tool
def parse_simulation_output() -> dict:
    """
    Parse the latest EnergyPlus eplusout.csv.
    Returns file name, row count, columns and 10-row preview.
    Req 1 + Req 2: LLM parses output files without human modification.
    """
    from energyplus.parser import parse_results
    return parse_results()


@mcp.tool
def inspect_idf() -> dict:
    """
    Use eppy to read building.idf and return a structured summary:
    object counts, zone names, thermostats, current setpoints.
    Req 1: eppy bridges Python with the IDF file.
    Req 2: LLM executes tasks without human code modification.
    """
    from energyplus.idf_reader import get_idf_summary
    return get_idf_summary()


@mcp.tool
def get_idf_setpoints() -> dict:
    """
    Use eppy to read the current cooling/heating setpoints from the IDF.
    Returns {cooling_setpoint_c, heating_setpoint_c, source}.
    """
    from energyplus.idf_reader import get_current_setpoints
    return get_current_setpoints()


@mcp.tool
def list_idf_objects(object_type: str) -> dict:
    """
    List all IDF objects of a given type (e.g. 'ZONE', 'LIGHTS').
    Req 2: LLM inspects building components without human code modification.
    """
    from energyplus.idf_reader import list_idf_objects as _list
    return _list(object_type)


# ═══════════════════════════════════════════════════════════
# REQ 2 — Error extraction (LLM parses runtime errors)
# ═══════════════════════════════════════════════════════════

@mcp.tool
def extract_energyplus_errors() -> dict:
    """
    Read eplusout.err and extract Warning / Severe / Fatal messages.
    Req 2: LLM uses tools to parse files and extract runtime errors.
    """
    from pathlib import Path
    from energyplus.config import OUTPUT_DIR

    err_file = Path(OUTPUT_DIR) / "eplusout.err"
    if not err_file.exists():
        return {"found": False, "message": "No eplusout.err file found."}

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
        "found":          True,
        "warning_count":  len(warnings),
        "severe_count":   len(severe),
        "fatal_count":    len(fatal),
        "warnings":       warnings[-10:],
        "severe_errors":  severe,
        "fatal_errors":   fatal,
        "simulation_ok":  len(severe) == 0 and len(fatal) == 0,
    }


# ═══════════════════════════════════════════════════════════
# REQ 3 — Closed-Loop: Feedback → Reasoning → ECMs → Injection
# ═══════════════════════════════════════════════════════════

@mcp.tool
def stream_building_metrics() -> dict:
    """
    REQ 3 — Feedback (EnergyPlus → AI):
    Stream continuous performance metrics from the latest simulation:
      zone temperatures, indoor air quality (CO2), energy consumption,
      Predicted Mean Vote (PMV), PPD thermal comfort indices.
    """
    from energyplus.metrics import get_all_metrics
    from ml.comfort import calculate_comfort
    from ml.iaq import calculate_iaq

    metrics = get_all_metrics()
    try:
        comfort = calculate_comfort(
            air_temp=metrics["indoor_temperature"]     or 22.0,
            radiant_temp=metrics["radiant_temperature"] or 22.0,
            humidity=metrics["humidity"]               or 50.0,
            air_speed=metrics["air_speed"]             or 0.15,
        )
        metrics["pmv"] = comfort["pmv"]
        metrics["ppd"] = comfort["ppd"]
    except Exception:
        metrics["pmv"] = None
        metrics["ppd"] = None

    co2 = metrics.get("co2")
    metrics["iaq_status"] = calculate_iaq(co2)["iaq"] if co2 is not None else "Unknown"
    return metrics


@mcp.tool
def evaluate_against_targets() -> dict:
    """
    REQ 3 — Reasoning:
    Evaluate metrics against predefined targets:
      - Occupancy comfort: PMV ±0.5, PPD < 10%
      - Peak demand thresholds
      - Local carbon grid intensity (> 400 gCO2/kWh)
    Returns PerformanceFlags with specific issue reasons.
    """
    from energyplus.metrics import get_all_metrics
    from ml.comfort import calculate_comfort
    from decision_engine.decision import evaluate_metrics

    metrics = get_all_metrics()
    try:
        comfort = calculate_comfort(
            air_temp=metrics["indoor_temperature"]     or 22.0,
            radiant_temp=metrics["radiant_temperature"] or 22.0,
            humidity=metrics["humidity"]               or 50.0,
            air_speed=metrics["air_speed"]             or 0.15,
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


@mcp.tool
def inject_setpoints(cooling_setpoint_c: float, heating_setpoint_c: float) -> dict:
    """
    REQ 3 — Forward Injection (AI → EnergyPlus):
    Computed set-points automatically feed back into the active
    EnergyPlus IDF instance.
    Uses eppy (Req 1) first, regex fallback.
    Safety-clamped: cooling 22–27°C, heating 16–22°C, deadband ≥ 1°C.
    """
    from energyplus.idf_editor import update_setpoints
    actual_cool, actual_heat = update_setpoints(
        cooling_setpoint=cooling_setpoint_c,
        heating_setpoint=heating_setpoint_c,
    )
    return {
        "success":            True,
        "cooling_setpoint_c": actual_cool,
        "heating_setpoint_c": actual_heat,
        "message": f"IDF updated → Cooling {actual_cool}°C / Heating {actual_heat}°C",
    }


@mcp.tool
def run_closed_loop_optimisation(iterations: int = 2) -> dict:
    """
    REQ 3 — Full Closed-Loop Execution Framework:
    Automates smart building operations through an autonomous pipeline:
      1. Feedback:   EnergyPlus runs, metrics streamed (temps/IAQ/PMV/energy)
      2. Reasoning:  LLM evaluates vs occupancy comfort, peak demand, carbon intensity
      3. Control:    LLM calculates optimal ECMs (HVAC setpoints, lighting, ventilation)
      4. Injection:  Setpoints + supervisory overrides injected back into active IDF
    Returns full history with energy savings proof (quantifiable kWh reduction).
    """
    from automation.controller import run_closed_loop
    history = run_closed_loop(iterations=iterations)
    if not history:
        return {"status": "error", "message": "No iterations completed"}

    first = history[0]["energy"]["total_energy_kwh"]
    last  = history[-1]["energy"]["total_energy_kwh"]
    savings_pct = round(((first - last) / first) * 100, 2) if first and last else 0.0

    return {
        "status":               "completed",
        "iterations":           len(history),
        "energy_savings_pct":   savings_pct,
        "first_iteration_kwh":  first,
        "last_iteration_kwh":   last,
        "history":              history,
    }


# ═══════════════════════════════════════════════════════════
# ML + Analytics
# ═══════════════════════════════════════════════════════════

@mcp.tool
def predict_energy_comfort(sensor_data: dict) -> dict:
    """
    Random Forest ML: predict energy (kWh), comfort score,
    optimal HVAC setpoint and expected savings.
    Input keys: temperature, humidity, co2, occupancy, hvac_temp.
    """
    return predict(sensor_data)


@mcp.tool
def get_building_analytics() -> dict:
    """
    Aggregated analytics: total predictions, avg energy,
    avg comfort score, avg expected savings.
    """
    return get_dashboard()


@mcp.tool
def get_llm_recommendation() -> dict:
    """
    LLM free-text recommendation based on latest EnergyPlus output.
    """
    return recommendation()


if __name__ == "__main__":
    mcp.run()
