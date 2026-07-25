from energyplus.runner import run_energyplus
from energyplus.parser import parse_results


def simulate():

    result = run_energyplus()

    if not result["success"]:
        return result

    parsed = parse_results()

    return {
        "status": "completed",
        "results": parsed,
    }


if __name__ == "__main__":
    print(simulate())