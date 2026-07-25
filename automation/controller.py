"""
=========================================================
Closed-Loop Controller

Ingests EnergyPlus simulation results, sends them to the
LLM for a control decision, injects the recommended
setpoints back into building.idf before the next run,
and tracks energy usage across iterations to prove savings.
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


def _extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError(
            f"No JSON found in LLM response: {text}"
        )

    return json.loads(match.group(0))


def _backup_idf():
    backup_path = IDF_FILE.with_suffix(".idf.bak")

    if not backup_path.exists():
        shutil.copy(IDF_FILE, backup_path)

    return backup_path


def _compute_total_energy() -> dict:
    """
    Reads the latest EnergyPlus output CSV and sums the
    heating/cooling rate columns as an energy usage proxy
    (kWh, assuming hourly timesteps in the output).
    """

    csv_file = get_csv_file()

    if csv_file is None:
        return {
            "total_cooling_kwh": None,
            "total_heating_kwh": None,
            "total_energy_kwh": None,
        }

    df = pd.read_csv(csv_file)

    cooling_cols = [
        col for col in df.columns
        if "Cooling" in col and "Rate" in col
    ]

    heating_cols = [
        col for col in df.columns
        if "Heating" in col and "Rate" in col
    ]

    total_cooling_w = df[cooling_cols].sum().sum() if cooling_cols else 0
    total_heating_w = df[heating_cols].sum().sum() if heating_cols else 0

    total_cooling_kwh = round(total_cooling_w / 1000, 2)
    total_heating_kwh = round(total_heating_w / 1000, 2)

    return {
        "total_cooling_kwh": total_cooling_kwh,
        "total_heating_kwh": total_heating_kwh,
        "total_energy_kwh": round(
            total_cooling_kwh + total_heating_kwh, 2
        ),
    }


def run_closed_loop(iterations: int = 2):
    """
    Runs the ingest -> evaluate -> inject control loop
    and tracks energy usage across iterations.
    """

    backup = _backup_idf()

    history = []

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
            "decision": decision,
        })

        print("Applying new setpoints to building.idf...")
        update_setpoints(
            cooling_setpoint=decision["cooling_setpoint_c"],
            heating_setpoint=decision["heating_setpoint_c"],
        )

    print("\n===== LOOP COMPLETE =====")

    for h in history:
        print(h)

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
                f"Iteration 1 = {first_energy} kWh -> "
                f"Iteration {len(history)} = {last_energy} kWh "
                f"({savings_pct}% change)"
            )

    print(f"\nOriginal IDF backed up at: {backup}")

    return history


if __name__ == "__main__":
    run_closed_loop(iterations=2)