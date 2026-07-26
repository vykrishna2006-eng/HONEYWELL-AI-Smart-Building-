"""
Indoor Air Quality Calculator
"""


def calculate_iaq(co2):

    if co2 < 800:
        status = "Excellent"

    elif co2 < 1000:
        status = "Good"

    elif co2 < 1500:
        status = "Moderate"

    else:
        status = "Poor"

    return {
        "co2": co2,
        "iaq": status,
    }