"""
=========================================================
Closed-Loop Controller

Ingests EnergyPlus simulation results, sends them to the
LLM for a control decision, injects the recommended
setpoints back into building.idf before the next run,
saves a versioned .idf per iteration, and exports a
savings report proving energy reduction.
=========================================================
"""

import json
import re
import shutil

import pandas as pd

from energyplus.simulator import simulate
from energyplus.idf_editor import update_setpoints
from energyplus.config import IDF_FILE
from energyplus.parser import get_csv_file
from llm.generator import generate


CONTROL_PROMPT = """
You are an HVAC control optimization engine for a building
running in EnergyPlus.

Below is a summary of the last simulation run.
Recommend new occupied-period thermostat setpoints that
reduce energy use while keeping indoor comfort reasonable
(cooling between 22-26C, heating between 19-23C).

Simulation Summary:
{summary}

Respond with ONLY a JSON object, no markdown, no explanation,
in exactly this format:
{{"cooling_setpoint_c": <number>, "heating_setpoint_c": <number>, "reason": "<short reason>"}}
"""

VERSIONS_DIR = IDF_FILE.parent / "versions"
REPORTS_DIR = IDF_FILE.parent.parent / "reports"


def _extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError(
            f"No JSON found in LLM response: {text}"
        )

    return json.loads(match.group(0))


def _restore_baseline():
    """
    Resets building.idf back to the true original baseline
    before starting a new loop, so iteration 1 always
    reflects the untouched building, not leftover setpoints
    from a previous run.
    """

    baseline_path = VERSIONS_DIR / "building_baseline.idf"

    if baseline_path.exists():
        shutil.copy(baseline_path, IDF_FILE)
        print(f"Restored building.idf from baseline: {baseline_path}")
    else:
        print(
            "No baseline snapshot found yet — "
            "this run will become the baseline."
        )


def _backup_baseline():
    """
    Saves the original, untouched IDF as the baseline
    reference (only ever done once).
    """

    VERSIONS_DIR.mkdir(exist_ok=True)

    baseline_path = VERSIONS_DIR / "building_baseline.idf"

    if not baseline_path.exists():
        shutil.copy(IDF_FILE, baseline_path)

    return baseline_path


def _save_iteration_idf(iteration: int):
    """
    Saves a snapshot of building.idf after it has been
    updated for this iteration, so every runtime version
    is preserved for submission.
    """

    VERSIONS_DIR.mkdir(exist_ok=True)

    snapshot_path = (
        VERSIONS_DIR / f"building_iteration_{iteration}.idf"
    )

    shutil.copy(IDF_FILE, snapshot_path)

    return snapshot_path


def _compute_total_energy() -> dict:
    """
    Reads the latest EnergyPlus output CSV and sums the
    actual equipment energy input columns (chiller
    electricity + boiler gas) as the real energy
    consumption proxy, in kWh (assuming hourly timesteps).
    """

    csv_file = get_csv_file()

    if csv_file is None:
        return {
            "total_cooling_kwh": None,
            "total_heating_kwh": None,
            "total_energy_kwh": None,
        }

    df = pd.read_csv(csv_file)

    chiller_col = next(
        (col for col in df.columns if "Chiller Electricity Rate" in col),
        None,
    )

    boiler_col = next(
        (col for col in df.columns if "Boiler NaturalGas Rate" in col),
        None,
    )

    total_cooling_w = df[chiller_col].sum() if chiller_col else 0
    total_heating_w = df[boiler_col].sum() if boiler_col else 0

    total_cooling_kwh = round(total_cooling_w / 1000, 2)
    total_heating_kwh = round(total_heating_w / 1000, 2)

    return {
        "total_cooling_kwh": total_cooling_kwh,
        "total_heating_kwh": total_heating_kwh,
        "total_energy_kwh": round(
            total_cooling_kwh + total_heating_kwh, 2
        ),
    }


def _save_iteration_csv(iteration: int):
    """
    Saves a snapshot of the full eplusout.csv per iteration
    so we can directly compare simulated behavior (not just
    plant totals) between iterations afterward.
    """

    csv_file = get_csv_file()

    if csv_file is None:
        return None

    REPORTS_DIR.mkdir(exist_ok=True)

    snapshot_path = (
        REPORTS_DIR / f"eplusout_iteration_{iteration}.csv"
    )

    shutil.copy(csv_file, snapshot_path)

    return snapshot_path


def _diagnose_zone_demand(iteration: int):
    """
    Prints the total zone-level heating/cooling demand for
    a quick sanity check on whether the setpoint change is
    actually affecting simulated zone behavior.
    """

    csv_file = get_csv_file()

    if csv_file is None:
        return

    df = pd.read_csv(csv_file)

    zone_cooling_cols = [
        col for col in df.columns
        if "Zone Air System Sensible Cooling Rate" in col
    ]

    zone_heating_cols = [
        col for col in df.columns
        if "Zone Air System Sensible Heating Rate" in col
    ]

    zone_cooling_total = round(
        df[zone_cooling_cols].sum().sum() / 1000, 2
    )

    zone_heating_total = round(
        df[zone_heating_cols].sum().sum() / 1000, 2
    )

    print(
        f"[Iteration {iteration}] Zone-level demand -> "
        f"Cooling: {zone_cooling_total} kWh, "
        f"Heating: {zone_heating_total} kWh"
    )


def _export_report(history: list):
    """
    Exports the full run history (energy + applied
    setpoints per iteration) as both JSON and CSV, and
    prints the baseline-vs-final savings percentage. This
    is the Quantitative Savings Dashboard data export
    deliverable.
    """

    REPORTS_DIR.mkdir(exist_ok=True)

    json_path = REPORTS_DIR / "savings_report.json"
    csv_path = REPORTS_DIR / "savings_report.csv"

    with open(json_path, "w") as f:
        json.dump(history, f, indent=2)

    rows = []

    for h in history:
        rows.append({
            "iteration": h["iteration"],
            "total_energy_kwh": h["energy"]["total_energy_kwh"],
            "total_cooling_kwh": h["energy"]["total_cooling_kwh"],
            "total_heating_kwh": h["energy"]["total_heating_kwh"],
            "applied_cooling_setpoint_c": h["applied_cooling_setpoint_c"],
            "applied_heating_setpoint_c": h["applied_heating_setpoint_c"],
            "next_decision_reason": h["decision"]["reason"],
        })

    pd.DataFrame(rows).to_csv(csv_path, index=False)

    print(f"\nSavings report exported to:\n- {json_path}\n- {csv_path}")

    if len(history) >= 2:
        first_energy = history[0]["energy"]["total_energy_kwh"]
        last_energy = history[-1]["energy"]["total_energy_kwh"]

        if first_energy and last_energy:
            savings_pct = round(
                ((first_energy - last_energy) / first_energy) * 100,
                2,
            )

            print(
                f"\nENERGY COMPARISON: "
                f"Baseline (Iteration 1) = {first_energy} kWh -> "
                f"Final (Iteration {len(history)}) = {last_energy} kWh "
                f"({savings_pct}% change)"
            )


def run_closed_loop(iterations: int = 2):
    """
    Runs the ingest -> evaluate -> inject control loop,
    tracks energy usage against the setpoints that actually
    produced it, and exports a savings report + versioned
    IDFs for submission.
    """

    _restore_baseline()

    baseline = _backup_baseline()
    print(f"Baseline IDF saved at: {baseline}")

    history = []

    current_cooling = "Baseline"
    current_heating = "Baseline"

    for i in range(iterations):

        print(f"\n===== ITERATION {i + 1} =====")

        print("Running EnergyPlus simulation...")
        result = simulate()

        if result.get("status") != "completed":
            print("Simulation failed:", result)
            break

        parsed = result["results"]

        energy = _compute_total_energy()

        print("Energy usage this iteration:", energy)

        _diagnose_zone_demand(i + 1)
        _save_iteration_csv(i + 1)

        summary = f"""
File: {parsed['file']}
Rows: {parsed['rows']}
Columns: {parsed['columns']}
Preview (first rows): {parsed['preview']}
Estimated Energy Usage: {energy}
"""

        print("Sending results to LLM for a control decision...")
        raw_response = generate(
            CONTROL_PROMPT.format(summary=summary)
        )

        decision = _extract_json(raw_response)
        print("LLM decision:", decision)

        history.append({
            "iteration": i + 1,
            "energy": energy,
            "applied_cooling_setpoint_c": current_cooling,
            "applied_heating_setpoint_c": current_heating,
            "decision": decision,
        })

        print("Applying new setpoints to building.idf...")
        update_setpoints(
            cooling_setpoint=decision["cooling_setpoint_c"],
            heating_setpoint=decision["heating_setpoint_c"],
        )

        current_cooling = decision["cooling_setpoint_c"]
        current_heating = decision["heating_setpoint_c"]

        snapshot = _save_iteration_idf(i + 1)
        print(f"Saved runtime IDF snapshot: {snapshot}")

    print("\n===== LOOP COMPLETE =====")

    for h in history:
        print(h)

    if history:
        _export_report(history)

    return history


if __name__ == "__main__":
    run_closed_loop(iterations=2)