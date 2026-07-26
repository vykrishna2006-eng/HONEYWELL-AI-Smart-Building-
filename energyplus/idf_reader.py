"""
=========================================================
IDF Reader — eppy-based IDF inspection

Requirement 1 — "functional libraries (e.g., eppy) to bridge
Python with the underlying Input Data File (.idf)"

The MCP LLM tools call these functions to inspect the IDF
without human code modification.
=========================================================
"""
from __future__ import annotations
from pathlib import Path

from energyplus.config import IDF_FILE, ENERGYPLUS_EXE


def _get_idf(idf_path: Path = IDF_FILE):
    """Load IDF with eppy. Returns EppyIDF object or raises."""
    from eppy.modeleditor import IDF as EppyIDF

    idd_candidates = [
        Path(ENERGYPLUS_EXE).parent / "Energy+.idd",
        Path(r"C:\EnergyPlusV26-1-0\Energy+.idd"),
        Path(r"C:\EnergyPlusV24-1-0\Energy+.idd"),
        Path(r"C:\EnergyPlusV23-1-0\Energy+.idd"),
    ]
    idd_path = next((p for p in idd_candidates if p.exists()), None)
    if idd_path is None:
        raise FileNotFoundError("EnergyPlus IDD file not found. Check ENERGYPLUS_EXE path.")

    try:
        EppyIDF.setiddname(str(idd_path))
    except Exception:
        pass
    return EppyIDF(str(idf_path))


def get_current_setpoints(idf_path: Path = IDF_FILE) -> dict:
    """
    Read current cooling/heating setpoints from the IDF using eppy.
    Returns {cooling_setpoint_c, heating_setpoint_c, source}.
    """
    try:
        idf = _get_idf(idf_path)
        result = {"source": "eppy", "cooling_setpoint_c": None, "heating_setpoint_c": None}

        for sched in idf.idfobjects.get("SCHEDULE:COMPACT", []):
            name = (sched.Name or "").strip()
            fields = sched.fieldvalues
            in_weekdays = False
            for idx, val in enumerate(fields):
                v = str(val).strip().lower()
                if "for: weekdays" in v:
                    in_weekdays = True
                if in_weekdays and "until: 20:00" in v:
                    raw = str(fields[idx + 1]).strip() if idx + 1 < len(fields) else None
                    try:
                        sp = float(raw)
                    except Exception:
                        sp = None
                    if name == "Clg-SetP-Sch":
                        result["cooling_setpoint_c"] = sp
                    elif name == "Htg-SetP-Sch":
                        result["heating_setpoint_c"] = sp
                    break
        return result
    except Exception as e:
        return {"source": "error", "error": str(e)}


def get_idf_summary(idf_path: Path = IDF_FILE) -> dict:
    """
    Return a summary of the IDF: object type counts, zone names,
    HVAC equipment, current setpoints.
    Used by MCP LLM tools to inspect building config without
    human code modification.
    """
    try:
        idf = _get_idf(idf_path)

        obj_counts = {k: len(v) for k, v in idf.idfobjects.items() if v}

        zones = [z.Name for z in idf.idfobjects.get("ZONE", [])]

        thermostats = [
            {"name": t.Name}
            for t in idf.idfobjects.get("THERMOSTATSETPOINT:DUALSETPOINT", [])
        ]

        setpoints = get_current_setpoints(idf_path)

        return {
            "success":       True,
            "idf_file":      str(idf_path),
            "object_counts": obj_counts,
            "zones":         zones,
            "thermostats":   thermostats,
            "setpoints":     setpoints,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_idf_objects(object_type: str, idf_path: Path = IDF_FILE) -> dict:
    """
    List all IDF objects of a given type (e.g. 'ZONE', 'PEOPLE').
    Used by MCP tools to let the LLM inspect specific object classes.
    """
    try:
        idf = _get_idf(idf_path)
        objs = idf.idfobjects.get(object_type.upper(), [])
        return {
            "success": True,
            "object_type": object_type.upper(),
            "count": len(objs),
            "objects": [
                {k: getattr(obj, k, None) for k in obj.fieldnames}
                for obj in objs[:20]   # limit to 20
            ],
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    from pprint import pprint
    pprint(get_idf_summary())
