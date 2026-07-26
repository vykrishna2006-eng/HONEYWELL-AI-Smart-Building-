"""
=========================================================
IDF Setpoint Editor

Edits the occupied-period cooling/heating thermostat
setpoints inside building.idf so the control loop can
push AI-recommended setpoints back into EnergyPlus.

Safety rules (enforced here, not just in controller.py):
  - Cooling: 22 °C – 27 °C
  - Heating: 16 °C – 22 °C
  - Cooling must always exceed Heating by at least 1 °C
  - If any value is out-of-range, it is clamped and a
    warning is printed — the IDF is never written with
    invalid values.
=========================================================
"""

import re
import shutil
from pathlib import Path

from energyplus.config import IDF_FILE

# ── Safety bounds ──────────────────────────────────────────
COOL_MIN, COOL_MAX = 22.0, 27.0
HEAT_MIN, HEAT_MAX = 16.0, 22.0
MIN_DEADBAND       = 1.0   # cooling must be > heating + this


def _clamp_setpoints(
    cooling: float,
    heating: float,
) -> tuple[float, float]:
    """
    Clamp both setpoints to safe ranges and ensure
    cooling > heating + MIN_DEADBAND.
    Returns (cooling, heating) rounded to 1 decimal.
    """
    original_cool = cooling
    original_heat = heating

    cooling = max(COOL_MIN, min(cooling, COOL_MAX))
    heating = max(HEAT_MIN, min(heating, HEAT_MAX))

    # Enforce deadband: cooling must exceed heating
    if cooling <= heating + MIN_DEADBAND:
        # Try raising cooling first
        cooling = heating + MIN_DEADBAND
        if cooling > COOL_MAX:
            # Can't raise cooling, lower heating instead
            cooling = COOL_MAX
            heating = cooling - MIN_DEADBAND
        # Final heating clamp
        heating = max(HEAT_MIN, min(heating, HEAT_MAX))

    cooling = round(cooling, 1)
    heating = round(heating, 1)

    if cooling != round(original_cool, 1) or heating != round(original_heat, 1):
        print(
            f"[idf_editor] Setpoint clamped: "
            f"cooling {original_cool} → {cooling} °C, "
            f"heating {original_heat} → {heating} °C"
        )

    return cooling, heating


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
) -> tuple[float, float]:
    """
    Writes new occupied cooling/heating setpoints into building.idf.

    Setpoints are safety-clamped before writing to prevent
    EnergyPlus fatal errors from invalid thermostat configurations.

    Returns the actual (cooling, heating) values that were written.
    """
    # ── 1. Safety clamp ────────────────────────────────────
    cooling_setpoint, heating_setpoint = _clamp_setpoints(
        float(cooling_setpoint),
        float(heating_setpoint),
    )

    # ── 2. Validate cooling > heating ─────────────────────
    if cooling_setpoint <= heating_setpoint:
        raise ValueError(
            f"After clamping: cooling ({cooling_setpoint}) must be "
            f"greater than heating ({heating_setpoint}). "
            "This should not happen — check _clamp_setpoints logic."
        )

    # ── 3. Backup before writing ────────────────────────────
    backup_path = idf_path.with_suffix(".idf.prev")
    shutil.copy(idf_path, backup_path)

    # ── 4. Apply to IDF ────────────────────────────────────
    text = idf_path.read_text()

    text = _replace_occupied_setpoint(text, "Clg-SetP-Sch", cooling_setpoint)
    text = _replace_occupied_setpoint(text, "Htg-SetP-Sch", heating_setpoint)

    idf_path.write_text(text)

    print(
        f"[idf_editor] Updated setpoints → "
        f"Cooling: {cooling_setpoint} °C, "
        f"Heating: {heating_setpoint} °C"
    )

    return cooling_setpoint, heating_setpoint


if __name__ == "__main__":
    update_setpoints(cooling_setpoint=24.0, heating_setpoint=21.0)
