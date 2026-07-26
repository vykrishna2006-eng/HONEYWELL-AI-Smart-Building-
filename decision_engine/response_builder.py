"""
=========================================================
Response Builder

Formats the closed-loop iteration result into a
structured dict suitable for JSON serialisation and
frontend display.
=========================================================
"""

from __future__ import annotations
from datetime import datetime, timezone


def build_iteration_response(
    iteration: int,
    energy: dict,
    comfort: dict,
    iaq: dict,
    metrics: dict,
    decision: dict,
    applied_cooling: str | float,
    applied_heating: str | float,
) -> dict:
    """
    Assembles one iteration's data into a standardised dict.
    Strips any non-serialisable values (NaN → None).
    """
    import math

    def _safe(v):
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return None
        return v

    return {
        "iteration":                iteration,
        "timestamp":                datetime.now(timezone.utc).isoformat(),

        # Energy
        "energy": {
            "total_energy_kwh":    _safe(energy.get("total_energy_kwh")),
            "total_cooling_kwh":   _safe(energy.get("total_cooling_kwh")),
            "total_heating_kwh":   _safe(energy.get("total_heating_kwh")),
        },

        # Thermal comfort (PMV/PPD)
        "comfort": {
            "pmv": _safe(comfort.get("pmv")),
            "ppd": _safe(comfort.get("ppd")),
        },

        # Indoor air quality
        "iaq": {
            "co2": _safe(iaq.get("co2")),
            "iaq": iaq.get("iaq", "Unknown"),
        },

        # Environmental / operational
        "occupancy":            _safe(metrics.get("occupancy")),
        "outdoor_temperature":  _safe(metrics.get("outdoor_temperature")),
        "indoor_temperature":   _safe(metrics.get("indoor_temperature")),
        "humidity":             _safe(metrics.get("humidity")),
        "peak_demand":          _safe(metrics.get("peak_demand")),
        "carbon_intensity":     _safe(metrics.get("carbon_intensity")),
        "solar_radiation":      _safe(metrics.get("solar_radiation")),
        "wind_speed":           _safe(metrics.get("wind_speed")),

        # What was applied this iteration (from previous decision)
        "applied_cooling_setpoint_c": applied_cooling,
        "applied_heating_setpoint_c": applied_heating,

        # AI decision for next iteration
        "decision": {
            "cooling_setpoint_c": decision.get("cooling_setpoint_c"),
            "heating_setpoint_c": decision.get("heating_setpoint_c"),
            "lighting_action":    decision.get("lighting_action"),
            "ventilation_action": decision.get("ventilation_action"),
            "equipment_schedule": decision.get("equipment_schedule"),
            "reason":             decision.get("reason"),
            "flags":              decision.get("flags", []),
        },
    }


def build_summary_table(history: list[dict]) -> list[dict]:
    """
    Produces a flat list of dicts for CSV export.
    """
    rows = []
    for h in history:
        rows.append({
            "iteration":            h["iteration"],
            "energy_kwh":           h["energy"]["total_energy_kwh"],
            "cooling_kwh":          h["energy"]["total_cooling_kwh"],
            "heating_kwh":          h["energy"]["total_heating_kwh"],
            "pmv":                  h["comfort"]["pmv"],
            "ppd":                  h["comfort"]["ppd"],
            "co2":                  h["iaq"]["co2"],
            "iaq":                  h["iaq"]["iaq"],
            "occupancy":            h["occupancy"],
            "indoor_temperature":   h.get("indoor_temperature"),
            "outdoor_temperature":  h.get("outdoor_temperature"),
            "humidity":             h.get("humidity"),
            "peak_demand":          h.get("peak_demand"),
            "carbon_intensity":     h.get("carbon_intensity"),
            "cooling_setpoint":     h["applied_cooling_setpoint_c"],
            "heating_setpoint":     h["applied_heating_setpoint_c"],
            "next_cooling":         h["decision"]["cooling_setpoint_c"],
            "next_heating":         h["decision"]["heating_setpoint_c"],
            "lighting_action":      h["decision"]["lighting_action"],
            "ventilation_action":   h["decision"]["ventilation_action"],
            "equipment_schedule":   h["decision"]["equipment_schedule"],
            "reason":               h["decision"]["reason"],
        })
    return rows
