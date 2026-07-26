"""
=========================================================
AI Smart Building — Closed-Loop Optimisation Controller

Requirement 3 — Closed-Loop Execution Framework:
  1. Feedback  (EnergyPlus → AI)
       Run EnergyPlus, stream continuous performance metrics
       (zone temperatures, IAQ, energy, PMV comfort indices).

  2. Reasoning (AI evaluates metrics vs targets)
       Evaluate against: occupancy comfort, peak demand
       thresholds, and local carbon grid intensity.

  3. Control Actions (AI → EnergyPlus)
       LLM calculates optimal ECMs and updates dynamic
       setpoints (cooling, heating, lighting, ventilation,
       equipment schedule).

  4. Forward Injection
       Validated setpoints injected back into the active
       building.idf for the next EnergyPlus run.
=========================================================
"""

from __future__ import annotations

import json
import re
import shutil
import traceback

import pandas as pd

from energyplus.simulator   import simulate
from energyplus.runner      import run_energyplus   # Req 1: direct EnergyPlus engine call
from energyplus.idf_editor  import update_setpoints
from energyplus.config      import IDF_FILE
from energyplus.parser      import get_csv_file
from energyplus.metrics     import get_all_metrics

from llm.generator          import generate

from ml.comfort             import calculate_comfort
from ml.iaq                 import calculate_iaq

from decision_engine.decision       import evaluate_metrics
from decision_engine.merger         import merge_decisions
from decision_engine.response_builder import build_iteration_response, build_summary_table

# ── Paths ──────────────────────────────────────────────────
VERSIONS_DIR = IDF_FILE.parent / "versions"
REPORTS_DIR  = IDF_FILE.parent.parent / "reports"

# ── LLM Prompt ────────────────────────────────────────────
CONTROL_PROMPT = """
You are an expert AI Building Energy Management System (BEMS).

Your objective: minimise energy consumption while maintaining occupant comfort.

Strict rules:
1. Cooling setpoint: 22 – 27 °C  (MUST be greater than heating + 1 °C)
2. Heating setpoint: 16 – 22 °C
3. PMV target: −0.5 to +0.5  (ISO 7730 neutral comfort zone)
4. PPD target: below 10 %
5. If occupancy is low (<10%), increase setpoints to save energy (setback mode).
6. If peak demand is high, avoid excessive cooling.
7. If carbon intensity is high (>400 gCO₂/kWh), prefer energy-saving actions.
8. Always provide a specific, meaningful reason.
9. Return ONLY valid JSON — no explanation outside the JSON block.

=== LIVE BUILDING PERFORMANCE SUMMARY ===

{summary}

=== PERFORMANCE FLAGS ===
{flags}

Return EXACTLY this JSON (no extra keys, no markdown):

{{
    "cooling_setpoint_c":  24.0,
    "heating_setpoint_c":  20.0,
    "lighting_action":     "Reduce lighting by 20% in unoccupied zones",
    "ventilation_action":  "Maintain minimum ventilation rate",
    "equipment_schedule":  "Delay non-essential equipment start by 30 min",
    "reason":              "PMV is −0.81 indicating overcooling; raising cooling setpoint from 23.9 to 25°C reduces chiller load while keeping occupants comfortable."
}}
"""


# ── Helpers ────────────────────────────────────────────────

def _extract_json(text: str) -> dict:
    match = re.search(r"\{.*?\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in LLM response:\n{text[:500]}")
    return json.loads(match.group())


def _restore_baseline():
    baseline = VERSIONS_DIR / "building_baseline.idf"
    if baseline.exists():
        shutil.copy(baseline, IDF_FILE)
        print(f"[controller] Restored baseline IDF")
    else:
        print("[controller] No baseline found — current IDF becomes baseline")


def _backup_baseline():
    VERSIONS_DIR.mkdir(exist_ok=True)
    baseline = VERSIONS_DIR / "building_baseline.idf"
    if not baseline.exists():
        shutil.copy(IDF_FILE, baseline)
    return baseline


def _save_iteration_idf(iteration: int):
    VERSIONS_DIR.mkdir(exist_ok=True)
    snap = VERSIONS_DIR / f"building_iteration_{iteration}.idf"
    shutil.copy(IDF_FILE, snap)
    return snap


def _save_iteration_csv(iteration: int):
    csv_file = get_csv_file()
    if csv_file is None:
        return None
    REPORTS_DIR.mkdir(exist_ok=True)
    snap = REPORTS_DIR / f"eplusout_iteration_{iteration}.csv"
    shutil.copy(csv_file, snap)
    return snap


def _compute_total_energy() -> dict:
    csv_file = get_csv_file()
    if csv_file is None:
        return {"total_cooling_kwh": None, "total_heating_kwh": None, "total_energy_kwh": None}

    df = pd.read_csv(csv_file)

    chiller_col = next((c for c in df.columns if "Chiller Electricity Rate" in c), None)
    boiler_col  = next((c for c in df.columns if "Boiler NaturalGas Rate"   in c), None)

    total_cooling = round(df[chiller_col].sum() / 1000, 2) if chiller_col else 0
    total_heating = round(df[boiler_col].sum()  / 1000, 2) if boiler_col  else 0

    return {
        "total_cooling_kwh": total_cooling,
        "total_heating_kwh": total_heating,
        "total_energy_kwh":  round(total_cooling + total_heating, 2),
    }


def _export_report(history: list):
    REPORTS_DIR.mkdir(exist_ok=True)

    json_path = REPORTS_DIR / "savings_report.json"
    csv_path  = REPORTS_DIR / "savings_report.csv"

    with open(json_path, "w") as f:
        json.dump(history, f, indent=2, default=str)

    rows = build_summary_table(history)
    pd.DataFrame(rows).to_csv(csv_path, index=False)

    print(f"\n[controller] Reports saved → {json_path} | {csv_path}")

    if len(history) >= 2:
        first = history[0]["energy"]["total_energy_kwh"]
        last  = history[-1]["energy"]["total_energy_kwh"]
        if first and last:
            savings = round(((first - last) / first) * 100, 2)
            print(f"[controller] Energy savings across iterations: {savings}%")


# ── Main closed-loop ───────────────────────────────────────

def run_closed_loop(iterations: int = 2) -> list:
    """
    Full Closed-Loop Execution:
      EnergyPlus → metrics → reasoning → ECMs → IDF injection → repeat
    """
    _restore_baseline()
    _backup_baseline()

    history = []
    current_cooling: str | float = "Baseline"
    current_heating: str | float = "Baseline"

    for i in range(iterations):
        print(f"\n{'='*60}\nITERATION {i + 1}\n{'='*60}")

        # ── Step 1: Run EnergyPlus (Req 1 & 3-Feedback) ───
        print("[controller] Running EnergyPlus...")
        result = simulate()

        if result.get("status") != "completed":
            print(f"[controller] Simulation failed: {result}")
            break

        parsed = result["results"]

        # ── Step 2: Stream metrics from output CSV ─────────
        print("[controller] Reading performance metrics from EnergyPlus output...")
        energy  = _compute_total_energy()
        metrics = get_all_metrics()

        print(f"  Indoor temp : {metrics.get('indoor_temperature')} °C")
        print(f"  Humidity    : {metrics.get('humidity')} %")
        print(f"  Occupancy   : {metrics.get('occupancy')}")
        print(f"  CO₂         : {metrics.get('co2')} ppm")
        print(f"  Total energy: {energy['total_energy_kwh']} kWh")

        # ── Step 3: Calculate comfort (PMV/PPD) ────────────
        try:
            comfort = calculate_comfort(
                air_temp=metrics["indoor_temperature"]   or 22.0,
                radiant_temp=metrics["radiant_temperature"] or 22.0,
                humidity=metrics["humidity"]             or 50.0,
                air_speed=metrics["air_speed"]           or 0.15,
            )
        except Exception:
            traceback.print_exc()
            comfort = {"pmv": None, "ppd": None}

        metrics["pmv"] = comfort["pmv"]
        metrics["ppd"] = comfort["ppd"]

        print(f"  PMV         : {comfort.get('pmv')}")
        print(f"  PPD         : {comfort.get('ppd')} %")

        # ── Step 4: IAQ ────────────────────────────────────
        co2 = metrics.get("co2")
        iaq = calculate_iaq(co2) if co2 is not None else {"co2": None, "iaq": "Unknown"}

        # ── Step 5: Evaluate against targets (Req 3-Reasoning)
        flags = evaluate_metrics(metrics)
        print(f"  Performance flags: {flags.reasons if flags.reasons else 'All targets met'}")

        _save_iteration_csv(i + 1)

        # ── Step 6: Build LLM prompt ───────────────────────
        summary = f"""
ENERGY
  Cooling : {energy['total_cooling_kwh']} kWh
  Heating : {energy['total_heating_kwh']} kWh
  Total   : {energy['total_energy_kwh']} kWh

THERMAL COMFORT
  Indoor Temp     : {metrics.get('indoor_temperature')} °C
  Outdoor Temp    : {metrics.get('outdoor_temperature')} °C
  Humidity        : {metrics.get('humidity')} %
  PMV             : {comfort.get('pmv')}  (target: -0.5 to +0.5)
  PPD             : {comfort.get('ppd')} %  (target: < 10%)

INDOOR AIR QUALITY
  CO₂             : {iaq['co2']} ppm  (target: < 1000 ppm)
  IAQ Status      : {iaq['iaq']}

BUILDING OPERATION
  Occupancy       : {metrics.get('occupancy')} %
  Peak Demand     : {metrics.get('peak_demand')} kW
  Carbon Intensity: {metrics.get('carbon_intensity')} gCO₂/kWh
  Solar Radiation : {metrics.get('solar_radiation')} W/m²

CURRENT SETPOINTS
  Cooling : {current_cooling} °C
  Heating : {current_heating} °C
"""
        flag_text = "\n".join(f"  • {r}" for r in flags.reasons) if flags.reasons else "  • All performance targets met"

        prompt = CONTROL_PROMPT.format(summary=summary, flags=flag_text)

        # ── Step 7: Ask LLM (Req 2 — OSS LLM) ────────────
        print("[controller] Querying LLM for optimal ECMs...")
        try:
            raw_response = generate(prompt)
            print(f"  LLM response: {raw_response[:200]}...")
            llm_decision = _extract_json(raw_response)
        except Exception as e:
            print(f"[controller] LLM failed ({e}) — using rule-based fallback")
            from decision_engine.decision import recommend_setpoints
            cool_f = float(current_cooling) if isinstance(current_cooling, float) else 24.0
            heat_f = float(current_heating) if isinstance(current_heating, float) else 20.0
            cool_rb, heat_rb = recommend_setpoints(cool_f, heat_f, flags)
            llm_decision = {
                "cooling_setpoint_c": cool_rb,
                "heating_setpoint_c": heat_rb,
                "lighting_action":    "Maintain current lighting",
                "ventilation_action": "Maintain current ventilation",
                "equipment_schedule": "Normal schedule",
                "reason":             f"Rule-based fallback: {'; '.join(flags.reasons) or 'nominal operation'}",
            }

        # ── Step 8: Merge + validate (Req 3-Control Actions)
        cool_prev = float(current_cooling) if isinstance(current_cooling, (int, float)) else 24.0
        heat_prev = float(current_heating) if isinstance(current_heating, (int, float)) else 20.0

        final_decision = merge_decisions(
            llm_decision=llm_decision,
            flags=flags,
            current_cooling=cool_prev,
            current_heating=heat_prev,
        )

        print(f"  → Cooling setpoint : {final_decision['cooling_setpoint_c']} °C")
        print(f"  → Heating setpoint : {final_decision['heating_setpoint_c']} °C")
        print(f"  → Lighting         : {final_decision['lighting_action']}")
        print(f"  → Ventilation      : {final_decision['ventilation_action']}")
        print(f"  → Equipment        : {final_decision['equipment_schedule']}")
        print(f"  → Reason           : {final_decision['reason']}")

        # ── Step 9: Store iteration result ────────────────
        record = build_iteration_response(
            iteration=i + 1,
            energy=energy,
            comfort=comfort,
            iaq=iaq,
            metrics=metrics,
            decision=final_decision,
            applied_cooling=current_cooling,
            applied_heating=current_heating,
        )
        history.append(record)

        # ── Step 10: Forward Injection → IDF (Req 3) ──────
        print("[controller] Injecting setpoints into building.idf...")
        actual_cool, actual_heat = update_setpoints(
            cooling_setpoint=final_decision["cooling_setpoint_c"],
            heating_setpoint=final_decision["heating_setpoint_c"],
        )

        current_cooling = actual_cool
        current_heating = actual_heat

        _save_iteration_idf(i + 1)

    # ── Export reports ─────────────────────────────────────
    print(f"\n{'='*70}\nOPTIMISATION COMPLETE — {len(history)} iterations\n{'='*70}")
    if history:
        _export_report(history)
        _generate_chart_safe()

    return history


def _generate_chart_safe():
    """Generate the savings chart, silently skip on error."""
    try:
        from automation.generate_chart import generate_chart
        generate_chart()
    except Exception as e:
        print(f"[controller] Chart generation skipped: {e}")


if __name__ == "__main__":
    run_closed_loop(iterations=2)
