"""
=========================================================
Decision Engine — Core Decision Maker

Evaluates EnergyPlus metrics against predefined comfort,
energy and carbon targets, then produces validated ECMs.

Requirements covered:
  Req 3 – Closed-Loop: Reasoning against occupancy comfort,
          peak demand thresholds, and local carbon intensity.
=========================================================
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


# ── Targets ───────────────────────────────────────────────
TARGETS = {
    "pmv_min":           -0.5,
    "pmv_max":            0.5,
    "ppd_max":           10.0,       # %
    "co2_max":         1000.0,       # ppm
    "peak_demand_high":   5.0,       # kW
    "carbon_high":      400.0,       # gCO2/kWh
    "occupancy_low":      0.1,       # fraction (10 %)
}


@dataclass
class PerformanceFlags:
    pmv_ok:          bool = True
    ppd_ok:          bool = True
    co2_ok:          bool = True
    energy_ok:       bool = True
    peak_demand_high: bool = False
    carbon_high:     bool = False
    occupancy_low:   bool = False
    reasons:         list[str] = field(default_factory=list)


def evaluate_metrics(metrics: dict) -> PerformanceFlags:
    """
    Compare live EnergyPlus metrics against targets.
    Returns a PerformanceFlags object describing what is
    outside tolerance — used by the LLM prompt and the
    ECM generator.
    """
    flags = PerformanceFlags()

    pmv  = metrics.get("pmv")
    ppd  = metrics.get("ppd")
    co2  = metrics.get("co2")
    peak = metrics.get("peak_demand")
    carb = metrics.get("carbon_intensity")
    occ  = metrics.get("occupancy")          # fraction or %

    if pmv is not None:
        if pmv < TARGETS["pmv_min"]:
            flags.pmv_ok = False
            flags.reasons.append(f"PMV={pmv:.2f} is too cold (target ≥ {TARGETS['pmv_min']})")
        elif pmv > TARGETS["pmv_max"]:
            flags.pmv_ok = False
            flags.reasons.append(f"PMV={pmv:.2f} is too warm (target ≤ {TARGETS['pmv_max']})")

    if ppd is not None and ppd > TARGETS["ppd_max"]:
        flags.ppd_ok = False
        flags.reasons.append(f"PPD={ppd:.1f}% exceeds {TARGETS['ppd_max']}% threshold")

    if co2 is not None and co2 > TARGETS["co2_max"]:
        flags.co2_ok = False
        flags.reasons.append(f"CO₂={co2:.0f} ppm exceeds {TARGETS['co2_max']} ppm limit")

    if peak is not None and peak > TARGETS["peak_demand_high"]:
        flags.peak_demand_high = True
        flags.reasons.append(f"Peak demand={peak:.1f} kW is high — avoid excessive cooling")

    if carb is not None and carb > TARGETS["carbon_high"]:
        flags.carbon_high = True
        flags.reasons.append(f"Grid carbon intensity={carb} gCO₂/kWh — favour energy saving")

    # Occupancy can come as fraction (0–1) or percentage (0–100)
    if occ is not None:
        occ_frac = occ / 100.0 if occ > 1 else occ
        if occ_frac < TARGETS["occupancy_low"]:
            flags.occupancy_low = True
            flags.reasons.append(f"Occupancy={occ:.1f}% is low — reduce lighting & HVAC")

    return flags


def recommend_setpoints(
    current_cooling: float,
    current_heating: float,
    flags: PerformanceFlags,
) -> tuple[float, float]:
    """
    Rule-based fallback setpoint recommendation when the LLM
    is unavailable.  Returns (cooling_°C, heating_°C).
    """
    cool = current_cooling if isinstance(current_cooling, float) else 24.0
    heat = current_heating if isinstance(current_heating, float) else 20.0

    if not flags.pmv_ok:
        # Too cold → lower heating; too warm → raise cooling
        if flags.reasons and "too cold" in flags.reasons[0]:
            heat = max(18.0, heat - 1.0)
        else:
            cool = min(27.0, cool + 1.0)

    if flags.peak_demand_high:
        cool = min(27.0, cool + 0.5)   # relax cooling slightly

    if flags.carbon_high:
        cool = min(27.0, cool + 0.5)
        heat = max(16.0, heat - 0.5)

    if flags.occupancy_low:
        cool = min(27.0, cool + 1.0)   # unoccupied setback

    # Deadband guard
    if cool <= heat + 1.0:
        cool = heat + 2.0
    cool = max(22.0, min(cool, 27.0))
    heat = max(16.0, min(heat, 22.0))

    return round(cool, 1), round(heat, 1)
