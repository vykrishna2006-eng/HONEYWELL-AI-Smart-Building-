"""
=========================================================
Decision Merger

Merges the rule-based recommendation from decision.py
with the LLM-generated JSON decision, enforcing safety
bounds on the final output.

Requirements covered:
  Req 3 – Forward Injection: computed set-points and
          supervisory overrides feed back to EnergyPlus.
=========================================================
"""

from __future__ import annotations
from decision_engine.decision import PerformanceFlags, recommend_setpoints
from energyplus.idf_editor import _clamp_setpoints


def merge_decisions(
    llm_decision: dict,
    flags: PerformanceFlags,
    current_cooling: float = 24.0,
    current_heating: float = 20.0,
) -> dict:
    """
    Takes the raw LLM JSON decision and applies:
      1. Safety clamping via idf_editor._clamp_setpoints
      2. Rule-based override if LLM values are still unsafe
      3. Fills in missing fields with sensible defaults

    Returns the final merged & validated decision dict.
    """
    # ── Extract LLM values ─────────────────────────────────
    try:
        llm_cool = float(llm_decision.get("cooling_setpoint_c", current_cooling))
        llm_heat = float(llm_decision.get("heating_setpoint_c", current_heating))
    except (TypeError, ValueError):
        llm_cool = current_cooling
        llm_heat = current_heating

    # ── Clamp (safety guard in idf_editor) ─────────────────
    safe_cool, safe_heat = _clamp_setpoints(llm_cool, llm_heat)

    # ── Rule-based fallback if LLM gave unreasonable values ─
    rb_cool, rb_heat = recommend_setpoints(safe_cool, safe_heat, flags)

    # Prefer LLM if within ±1 °C of rule-based; otherwise use rule-based
    final_cool = safe_cool if abs(safe_cool - rb_cool) <= 1.0 else rb_cool
    final_heat = safe_heat if abs(safe_heat - rb_heat) <= 1.0 else rb_heat

    # Build reason: combine LLM reason + flag reasons
    llm_reason = (llm_decision.get("reason") or "").strip()
    flag_notes  = "; ".join(flags.reasons) if flags.reasons else ""

    if llm_reason and flag_notes:
        full_reason = f"{llm_reason} | System flags: {flag_notes}"
    elif llm_reason:
        full_reason = llm_reason
    elif flag_notes:
        full_reason = f"Rule-based override: {flag_notes}"
    else:
        full_reason = "Optimised to reduce energy while maintaining occupant comfort."

    return {
        "cooling_setpoint_c":  round(final_cool, 1),
        "heating_setpoint_c":  round(final_heat, 1),
        "lighting_action":     llm_decision.get("lighting_action",    "Maintain current lighting"),
        "ventilation_action":  llm_decision.get("ventilation_action", "Maintain current ventilation"),
        "equipment_schedule":  llm_decision.get("equipment_schedule", "Normal schedule"),
        "reason":              full_reason,
        "llm_cool_raw":        round(llm_cool, 2),
        "llm_heat_raw":        round(llm_heat, 2),
        "flags":               flags.reasons,
    }
