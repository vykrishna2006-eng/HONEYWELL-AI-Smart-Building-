import subprocess
from pathlib import Path

from energyplus.config import (
    ENERGYPLUS_EXE,
    IDF_FILE,
    WEATHER_FILE,
    OUTPUT_DIR,
)

def run_energyplus():
    OUTPUT_DIR.mkdir(exist_ok=True)

    command = [
        ENERGYPLUS_EXE,
        "-w",
        str(WEATHER_FILE),
        "-d",
        str(OUTPUT_DIR),
        str(IDF_FILE),
    ]

    print("Running EnergyPlus...")
    print(command)

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


if __name__ == "__main__":
    response = run_energyplus()

    print(response)