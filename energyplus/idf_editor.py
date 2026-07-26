"""
=========================================================
IDF Setpoint Editor

Requirement 1 — Simulation Engine (EnergyPlus):
  "You may use functional libraries (e.g., eppy, PyEnergyPlus,
   or EMS/BCVTB) to bridge Python or execution runtimes with
   the underlying Input Data File (.idf)"

Primary method : eppy  (IDD-aware IDF editing)
Fallback method: regex (used only when eppy fails)

Safety rules enforced on EVERY write:
  - Cooling : 22 – 27 °C
  - Heating : 16 – 22 °C
  - Cooling must always exceed Heating by ≥ 1 °C
=========================================================
"""

from __future__ import annotations
import re
import shutil
from pathlib import Path

from energyplus.config import IDF_FILE, ENERGYPLUS_EXE

# ── Safety bounds ─────────────────────────────────────────
COOL_MIN, COOL_MAX = 22.0, 27.0
HEAT_MIN, HEAT_MAX = 16.0, 22.0
MIN_DEADBAND = 1.0


# ── Public clamp function (imported by merger.py) ─────────
def _clamp_setpoints(cooling: float, heating: float) -> tuple[float, float]:
    """
    Clamp setpoints to safe ranges and enforce deadband.
    Returns (cooling, heating) rounded to 1 dp.
    """
    orig_cool, orig_heat = cooling, heating

    cooling = max(COOL_MIN, min(float(cooling), COOL_MAX))
    heating = max(HEAT_MIN, min(float(heating), HEAT_MAX))

    if cooling <= heating + MIN_DEADBAND:
        cooling = heating + MIN_DEADBAND
        if cooling > COOL_MAX:
            cooling = COOL_MAX
            heating = cooling - MIN_DEADBAND
        heating = max(HEAT_MIN, min(heating, HEAT_MAX))

    cooling = round(cooling, 1)
    heating = round(heating, 1)

    if cooling != round(orig_cool, 1) or heating != round(orig_heat, 1):
        print(f"[idf_editor] Clamped: {orig_cool}→{cooling}°C cool, {orig_heat}→{heating}°C heat")

    return cooling, heating


# ── eppy-based IDF editing (Req 1 primary method) ─────────
def _update_with_eppy(idf_path: Path, cooling: float, heating: float) -> bool:
    """
    Use eppy to load the IDF, find all ThermostatSetpoint:DualSetpoint
    objects and overwrite their schedule references with constant
    Schedule:Compact objects at the new values.

    Returns True on success, False if eppy fails for any reason.
    """
    try:
        from eppy.modeleditor import IDF as EppyIDF

        # eppy needs the IDD matching the IDF version
        idd_candidates = [
            Path(ENERGYPLUS_EXE).parent / "Energy+.idd",
            Path(r"C:\EnergyPlusV26-1-0\Energy+.idd"),
            Path(r"C:\EnergyPlusV24-1-0\Energy+.idd"),
            Path(r"C:\EnergyPlusV23-1-0\Energy+.idd"),
        ]
        idd_path = next((p for p in idd_candidates if p.exists()), None)

        if idd_path is None:
            print("[idf_editor] eppy: no IDD file found — falling back to regex")
            return False

        try:
            EppyIDF.setiddname(str(idd_path))
        except Exception:
            pass  # already set

        idf = EppyIDF(str(idf_path))

        # Update all Schedule:Compact objects that match the setpoint schedules
        updated = 0
        for sched in idf.idfobjects.get("SCHEDULE:COMPACT", []):
            name = (sched.Name or "").strip()

            if name == "Clg-SetP-Sch":
                # Update the occupied WeekDays "Until: 20:00" value
                _eppy_update_schedule_value(sched, cooling)
                updated += 1

            elif name == "Htg-SetP-Sch":
                _eppy_update_schedule_value(sched, heating)
                updated += 1

        if updated == 0:
            print("[idf_editor] eppy: schedule objects not found — falling back to regex")
            return False

        idf.save(str(idf_path))
        print(f"[idf_editor] eppy: updated {updated} schedule(s) → "
              f"Cooling {cooling}°C / Heating {heating}°C")
        return True

    except Exception as e:
        print(f"[idf_editor] eppy failed ({e}) — falling back to regex")
        return False


def _eppy_update_schedule_value(sched_obj, new_value: float):
    """
    Walk eppy schedule fieldvalues and update the value that follows
    'Until: 20:00' in a WeekDays block.
    """
    fields = sched_obj.fieldvalues  # list of raw field strings
    in_weekdays = False
    for idx, val in enumerate(fields):
        v = str(val).strip().lower()
        if "for: weekdays" in v or v == "for: weekdays":
            in_weekdays = True
        if in_weekdays and "until: 20:00" in v:
            # The value is the NEXT field
            if idx + 1 < len(fields):
                fields[idx + 1] = str(new_value)
            break


# ── Regex-based fallback ──────────────────────────────────
def _replace_occupied_setpoint(text: str, schedule_name: str, new_value: float) -> str:
    """
    Regex fallback: find Schedule:Compact block and replace
    the 'Until: 20:00,<value>,' in the WeekDays section.
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
            f"Regex: could not find setpoint pattern for '{schedule_name}'. "
            "IDF structure may have changed."
        )
    return pattern.sub(lambda m: f"{m.group(1)}{new_value}{m.group(3)}", text, count=1)


def _update_with_regex(idf_path: Path, cooling: float, heating: float):
    """Regex fallback for IDF setpoint editing."""
    text = idf_path.read_text(encoding="utf-8", errors="replace")
    text = _replace_occupied_setpoint(text, "Clg-SetP-Sch", cooling)
    text = _replace_occupied_setpoint(text, "Htg-SetP-Sch", heating)
    idf_path.write_text(text, encoding="utf-8")
    print(f"[idf_editor] regex: updated → Cooling {cooling}°C / Heating {heating}°C")


# ── Public API ────────────────────────────────────────────
def update_setpoints(
    cooling_setpoint: float,
    heating_setpoint: float,
    idf_path: Path = IDF_FILE,
) -> tuple[float, float]:
    """
    Write new occupied cooling/heating setpoints into building.idf.

    Uses eppy first (Req 1 — functional library bridge), falls back
    to regex if eppy is unavailable or the IDD cannot be found.

    Safety-clamped before every write.
    Returns the actual (cooling, heating) values written.
    """
    # 1. Safety clamp
    cooling_setpoint, heating_setpoint = _clamp_setpoints(
        float(cooling_setpoint), float(heating_setpoint)
    )

    # 2. Final guard
    if cooling_setpoint <= heating_setpoint:
        raise ValueError(
            f"Post-clamp: cooling ({cooling_setpoint}) ≤ heating ({heating_setpoint}). "
            "Logic error in _clamp_setpoints."
        )

    # 3. Backup before write
    idf_path.with_suffix(".idf.prev").unlink(missing_ok=True)
    shutil.copy(idf_path, idf_path.with_suffix(".idf.prev"))

    # 4. Try eppy first, fall back to regex
    success = _update_with_eppy(idf_path, cooling_setpoint, heating_setpoint)
    if not success:
        _update_with_regex(idf_path, cooling_setpoint, heating_setpoint)

    return cooling_setpoint, heating_setpoint


if __name__ == "__main__":
    update_setpoints(cooling_setpoint=24.0, heating_setpoint=20.0)
