"""
=========================================================
IDF Setpoint Editor

Edits the occupied-period cooling/heating thermostat
setpoints inside building.idf so the control loop can
push AI-recommended setpoints back into EnergyPlus.
=========================================================
"""

import re
from pathlib import Path

from energyplus.config import IDF_FILE


def _replace_occupied_setpoint(
    text: str,
    schedule_name: str,
    new_value: float,
) -> str:
    """
    Finds the given Schedule:Compact block (e.g. Clg-SetP-Sch)
    and replaces the occupied WeekDays setpoint
    ("Until: 20:00,<value>,") with a new value.
    """

    pattern = re.compile(
        rf"({re.escape(schedule_name)},.*?For: WeekDays,[^\r\n]*\r?\n"
        rf"\s*Until:\s*6:00,[\d.]+,[^\r\n]*\r?\n"
        rf"\s*Until:\s*20:00,)([\d.]+)(,)",
        re.DOTALL,
    )

    match = pattern.search(text)

    if not match:
        raise ValueError(
            f"Could not find occupied setpoint pattern for '{schedule_name}'. "
            "The IDF structure may have changed."
        )

    return pattern.sub(
        lambda m: f"{m.group(1)}{new_value}{m.group(3)}",
        text,
        count=1,
    )


def update_setpoints(
    cooling_setpoint: float,
    heating_setpoint: float,
    idf_path: Path = IDF_FILE,
) -> None:
    """
    Writes new occupied cooling/heating setpoints into building.idf.
    """

    text = idf_path.read_text()

    text = _replace_occupied_setpoint(
        text, "Clg-SetP-Sch", cooling_setpoint
    )

    text = _replace_occupied_setpoint(
        text, "Htg-SetP-Sch", heating_setpoint
    )

    idf_path.write_text(text)

    print(
        f"Updated setpoints -> Cooling: {cooling_setpoint}C, "
        f"Heating: {heating_setpoint}C"
    )


if __name__ == "__main__":
    update_setpoints(cooling_setpoint=24.0, heating_setpoint=21.0)