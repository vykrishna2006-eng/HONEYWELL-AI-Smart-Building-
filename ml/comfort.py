"""
PMV / PPD Comfort Calculator
"""

from pythermalcomfort.models import pmv_ppd_iso


def calculate_comfort(
    air_temp,
    radiant_temp,
    humidity,
    air_speed,
    met=1.2,
    clo=0.6,
):

    result = pmv_ppd_iso(
        tdb=air_temp,
        tr=radiant_temp,
        vr=air_speed,
        rh=humidity,
        met=met,
        clo=clo,
    )

    return {
        "pmv": round(result.pmv, 2),
        "ppd": round(result.ppd, 2),
    }