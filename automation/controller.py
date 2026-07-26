CONTROL_PROMPT = """
You are an expert AI Building Energy Management System.

Your objective is to minimise energy consumption while maintaining occupant comfort.

Rules:

1. Cooling setpoint must be between 22 and 27 °C.
2. Heating setpoint must be between 18 and 22 °C.
3. Cooling setpoint must always be greater than heating setpoint.
4. Keep PMV between -0.5 and +0.5 whenever possible.
5. Keep PPD below 10%.
6. If occupancy is low, reduce lighting.
7. If peak demand is high, avoid excessive cooling.
8. If carbon intensity is high, recommend energy-saving actions.
9. Always provide a meaningful reason.
10. Return ONLY valid JSON.

Simulation Summary

{summary}

Return exactly this JSON format:

{{
    "cooling_setpoint_c": 24,
    "heating_setpoint_c": 20,
    "lighting_action": "Reduce lighting by 20%",
    "ventilation_action": "Maintain current ventilation",
    "equipment_schedule": "Delay non-essential equipment",
    "reason": "Cooling demand is high while occupancy is moderate, so increasing the cooling setpoint slightly reduces energy while maintaining acceptable comfort."
}}
"""


import json
import re
import shutil

from matplotlib.pyplot import cool
import pandas as pd

from decision_engine import decision
from energyplus.simulator import simulate
from energyplus.idf_editor import update_setpoints
from energyplus.config import IDF_FILE
from energyplus.parser import get_csv_file

from llm import prompt
from llm.generator import generate

from ml.comfort import calculate_comfort
from ml.iaq import calculate_iaq





VERSIONS_DIR = IDF_FILE.parent / "versions"
REPORTS_DIR = IDF_FILE.parent.parent / "reports"


def _extract_json(text: str) -> dict:

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError(
            f"No JSON found in LLM response:\n{text}"
        )

    return json.loads(match.group())


def _restore_baseline():

    baseline_path = VERSIONS_DIR / "building_baseline.idf"

    if baseline_path.exists():

        shutil.copy(
            baseline_path,
            IDF_FILE,
        )

        print(
            f"Restored baseline IDF from {baseline_path}"
        )

    else:

        print(
            "Baseline not found. Current IDF "
            "will become the baseline."
        )


def _backup_baseline():

    VERSIONS_DIR.mkdir(exist_ok=True)

    baseline_path = (
        VERSIONS_DIR /
        "building_baseline.idf"
    )

    if not baseline_path.exists():

        shutil.copy(
            IDF_FILE,
            baseline_path,
        )

    return baseline_path


def _save_iteration_idf(iteration: int):

    VERSIONS_DIR.mkdir(exist_ok=True)

    snapshot_path = (
        VERSIONS_DIR /
        f"building_iteration_{iteration}.idf"
    )

    shutil.copy(
        IDF_FILE,
        snapshot_path,
    )

    return snapshot_path

def _compute_total_energy() -> dict:
    """
    Reads the latest EnergyPlus output CSV and computes
    total cooling, heating and combined energy usage.
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
        (
            col
            for col in df.columns
            if "Chiller Electricity Rate" in col
        ),
        None,
    )

    boiler_col = next(
        (
            col
            for col in df.columns
            if "Boiler NaturalGas Rate" in col
        ),
        None,
    )

    total_cooling = (
        df[chiller_col].sum() / 1000
        if chiller_col
        else 0
    )

    total_heating = (
        df[boiler_col].sum() / 1000
        if boiler_col
        else 0
    )

    total_energy = total_cooling + total_heating

    return {
        "total_cooling_kwh": round(total_cooling, 2),
        "total_heating_kwh": round(total_heating, 2),
        "total_energy_kwh": round(total_energy, 2),
    }


def _save_iteration_csv(iteration: int):

    csv_file = get_csv_file()

    if csv_file is None:
        return None

    REPORTS_DIR.mkdir(exist_ok=True)

    snapshot = (
        REPORTS_DIR
        / f"eplusout_iteration_{iteration}.csv"
    )

    shutil.copy(csv_file, snapshot)

    return snapshot


def _diagnose_zone_demand(iteration: int):

    csv_file = get_csv_file()

    if csv_file is None:
        return

    df = pd.read_csv(csv_file)

    cooling_cols = [
        c
        for c in df.columns
        if "Zone Air System Sensible Cooling Rate" in c
    ]

    heating_cols = [
        c
        for c in df.columns
        if "Zone Air System Sensible Heating Rate" in c
    ]

    cooling = round(
        df[cooling_cols].sum().sum() / 1000,
        2,
    )

    heating = round(
        df[heating_cols].sum().sum() / 1000,
        2,
    )

    print(
        f"\nIteration {iteration}"
    )

    print(
        f"Zone Cooling : {cooling} kWh"
    )

    print(
        f"Zone Heating : {heating} kWh"
    )

def _export_report(history: list):

    REPORTS_DIR.mkdir(exist_ok=True)

    json_path = REPORTS_DIR / "savings_report.json"
    csv_path = REPORTS_DIR / "savings_report.csv"

    with open(json_path, "w") as f:
        json.dump(history, f, indent=2)

    rows = []

    for h in history:

        rows.append({

            "iteration": h["iteration"],

            "energy_kwh":
            h["energy"]["total_energy_kwh"],

            "cooling_kwh":
            h["energy"]["total_cooling_kwh"],

            "heating_kwh":
            h["energy"]["total_heating_kwh"],

            "pmv":
            h["comfort"]["pmv"],

            "ppd":
            h["comfort"]["ppd"],

            "co2":
            h["iaq"]["co2"],

            "iaq":
            h["iaq"]["iaq"],

            "occupancy":
            h["occupancy"],

            "cooling_setpoint":
            h["applied_cooling_setpoint_c"],

            "heating_setpoint":
            h["applied_heating_setpoint_c"],

            "reason":
            h["decision"]["reason"],
        })

    pd.DataFrame(rows).to_csv(
        csv_path,
        index=False,
    )

    print(
        f"\nReports exported to\n"
        f"{json_path}\n"
        f"{csv_path}"
    )

    if len(history) >= 2:

        first = history[0]["energy"]["total_energy_kwh"]

        last = history[-1]["energy"]["total_energy_kwh"]

        if first and last:

            savings = round(
                ((first - last) / first) * 100,
                2,
            )

            print(
                f"\nEnergy Savings = {savings}%"
            )

def run_closed_loop(iterations: int = 2):
    """
    Runs the closed-loop optimisation process.
    """

    _restore_baseline()

    baseline = _backup_baseline()

    print(f"Baseline IDF : {baseline}")

    history = []

    current_cooling = "Baseline"
    current_heating = "Baseline"

    for i in range(iterations):

        print("\n" + "=" * 60)
        print(f"ITERATION {i + 1}")
        print("=" * 60)

        print("\nRunning EnergyPlus...")

        result = simulate()

        if result.get("status") != "completed":
            print(result)
            break

        parsed = result["results"]

        # --------------------------------------------------
        # Energy
        # --------------------------------------------------

        energy = _compute_total_energy()

        print("\nEnergy")

        print(energy)

        # --------------------------------------------------
        # Building Conditions
        #
        # Replace these later with actual sensor values
        # or values parsed from EnergyPlus.
        # --------------------------------------------------
        from energyplus.metrics import get_all_metrics

        metrics = get_all_metrics()
        print("\n===== METRICS =====")
        print(metrics)
        print("===================\n")

        air_temp = metrics["indoor_temperature"]
        radiant_temp = metrics["radiant_temperature"]
        humidity = metrics["humidity"]
        air_speed = metrics["air_speed"]

        co2 = metrics["co2"]
        occupancy = metrics["occupancy"]

        outdoor_temp = metrics["outdoor_temperature"]
        wind_speed = metrics["wind_speed"]
        solar_radiation = metrics["solar_radiation"]

        peak_demand = metrics["peak_demand"]
        carbon_intensity = metrics["carbon_intensity"]

 
    

 

  
        # --------------------------------------------------
        # Thermal Comfort
        # --------------------------------------------------
        print("\n===== COMFORT INPUTS =====")
        print(type(air_temp), air_temp)
        print(type(radiant_temp), radiant_temp)
        print(type(humidity), humidity)
        print(type(air_speed), air_speed)
        print("==========================\n")

        comfort = calculate_comfort(

            air_temp=air_temp,

            radiant_temp=radiant_temp,

            humidity=humidity,

            air_speed=air_speed,

        )

        # --------------------------------------------------
        # Indoor Air Quality
        # --------------------------------------------------

        iaq = (
    calculate_iaq(co2)
    if co2 is not None
    else {
        "co2": None,
        "iaq": "Unknown",
    }
)

        print("\nComfort")

        print(
            f"PMV : {comfort['pmv']}"
        )

        print(
            f"PPD : {comfort['ppd']} %"
        )

        print("\nIndoor Air Quality")

        print(
            f"CO₂ : {iaq['co2']} ppm"
        )

        print(
            f"Status : {iaq['iaq']}"
        )

        _diagnose_zone_demand(i + 1)

        _save_iteration_csv(i + 1)

        # --------------------------------------------------
        # AI Summary
        # --------------------------------------------------

        summary = f"""
==================================================

AI BUILDING PERFORMANCE SUMMARY

==================================================

Simulation File

{parsed['file']}

Rows

{parsed['rows']}

Columns

{parsed['columns']}

Preview

{parsed['preview']}

==================================================

ENERGY

==================================================

Cooling Energy

{energy['total_cooling_kwh']} kWh

Heating Energy

{energy['total_heating_kwh']} kWh

Total Energy

{energy['total_energy_kwh']} kWh

==================================================

THERMAL COMFORT

==================================================

Indoor Temperature

{air_temp} °C

Outdoor Temperature

{outdoor_temp} °C

Relative Humidity

{humidity} %

PMV

{comfort['pmv']}

PPD

{comfort['ppd']} %

==================================================

INDOOR AIR QUALITY

==================================================

CO₂

{iaq['co2']} ppm

Indoor Air Quality

{iaq['iaq']}

==================================================

BUILDING OPERATION

==================================================

Occupancy

{occupancy} %

Peak Demand

{peak_demand}

Grid Carbon Intensity

{carbon_intensity} gCO₂/kWh

==================================================
"""

        print("\nSending Summary To Local Qwen LLM...")

        # ==================================================
        # Ask Local LLM
        # ==================================================

        prompt = CONTROL_PROMPT.format(summary=summary)

        raw_response = generate(prompt)
        print("\n===== RAW LLM RESPONSE =====")
        print(raw_response)
        print("============================\n")

        decision = _extract_json(raw_response)
        cool = float(decision["cooling_setpoint_c"])
        heat = float(decision["heating_setpoint_c"])

# Safe limits
        cool = max(22, min(cool, 27))
        heat = max(18, min(heat, 22))

# Ensure cooling > heating
        if cool <= heat:
            cool = heat + 2

        decision["cooling_setpoint_c"] = round(cool, 1)
        decision["heating_setpoint_c"] = round(heat, 1)

# Default reason
        if not decision.get("reason", "").strip():
            decision["reason"] = "Optimized to reduce energy while maintaining occupant comfort."

        print("\n===== VALIDATED AI DECISION =====")
        print(f"Cooling Setpoint : {decision['cooling_setpoint_c']}")
        print(f"Heating Setpoint : {decision['heating_setpoint_c']}")
        print("=================================\n")

        # --------------------------------------------------
        # Store History
        # --------------------------------------------------

        history.append({

            "iteration": i + 1,

            "energy": energy,

            "comfort": comfort,

            "iaq": iaq,

            "occupancy": occupancy,

            "outdoor_temperature": outdoor_temp,

            "peak_demand": peak_demand,

            "carbon_intensity": carbon_intensity,

            "applied_cooling_setpoint_c":
                current_cooling,

            "applied_heating_setpoint_c":
                current_heating,

            "decision": decision,

        })

        # --------------------------------------------------
        # Display ECM Recommendations
        # --------------------------------------------------

        print("\nRecommended Energy Conservation Measures")

        print("-" * 60)

        print(
            "Cooling Setpoint :",
            decision["cooling_setpoint_c"],
        )

        print(
            "Heating Setpoint :",
            decision["heating_setpoint_c"],
        )

        print(
            "Lighting :",
            decision.get(
                "lighting_action",
                "No recommendation",
            ),
        )

        print(
            "Ventilation :",
            decision.get(
                "ventilation_action",
                "No recommendation",
            ),
        )

        print(
            "Equipment :",
            decision.get(
                "equipment_schedule",
                "No recommendation",
            ),
        )

        print(
            "Reason :",
            decision["reason"],
        )

        # --------------------------------------------------
        # Apply Setpoints
        # --------------------------------------------------

        print("\nUpdating building.idf ...")

        update_setpoints(

            cooling_setpoint=
                decision["cooling_setpoint_c"],

            heating_setpoint=
                decision["heating_setpoint_c"],

        )

        current_cooling = decision[
            "cooling_setpoint_c"
        ]

        current_heating = decision[
            "heating_setpoint_c"
        ]

        snapshot = _save_iteration_idf(
            i + 1
        )

        print(
            f"Saved IDF Snapshot : {snapshot}"
        )

    # ======================================================
    # Loop Finished
    # ======================================================

    print("\n")

    print("=" * 70)
    print("OPTIMIZATION COMPLETE")
    print("=" * 70)

    for item in history:

        print("\nIteration", item["iteration"])

        print(
            "Energy :",
            item["energy"]["total_energy_kwh"],
            "kWh",
        )

        print(
            "PMV :",
            item["comfort"]["pmv"],
        )

        print(
            "PPD :",
            item["comfort"]["ppd"],
        )

        print(
            "IAQ :",
            item["iaq"]["iaq"],
        )

        print(
            "CO₂ :",
            item["iaq"]["co2"],
            "ppm",
        )

        print(
            "Cooling :",
            item["decision"]["cooling_setpoint_c"],
        )

        print(
            "Heating :",
            item["decision"]["heating_setpoint_c"],
        )

        print(
            "Reason :",
            item["decision"]["reason"],
        )

    if history:

        _export_report(history)

    return history


if __name__ == "__main__":

    run_closed_loop(
        iterations=2
    )