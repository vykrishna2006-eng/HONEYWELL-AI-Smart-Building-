from energyplus.parser import parse_results
from llm.generator import generate
import traceback


def building_recommendation():
    try:
        print("STEP 1")

        simulation = parse_results()
        print("STEP 2:", simulation)

        if not simulation["success"]:
            print("STEP 3")
            return simulation

        prompt = f"""
EnergyPlus Simulation Results

File:
{simulation['file']}

Rows:
{simulation['rows']}

Columns:
{simulation['columns']}

Preview:
{simulation['preview']}
"""

        print("STEP 4")

        recommendation = generate(prompt)

        print("STEP 5")

        return {
            "success": True,
            "simulation": simulation,
            "recommendation": recommendation,
        }

    except Exception:
        traceback.print_exc()
        raise