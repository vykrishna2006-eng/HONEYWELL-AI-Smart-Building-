class BuildingConstraints:
    """
    Building operating constraints.
    """

    # Temperature
    MIN_HVAC_SETPOINT = 18
    MAX_HVAC_SETPOINT = 28

    # Occupancy
    MAX_OCCUPANCY = 100

    # Indoor Air Quality
    MAX_CO2 = 1000

    # Comfort
    MIN_COMFORT = 80

    # Humidity
    MIN_HUMIDITY = 30
    MAX_HUMIDITY = 60

    # Energy
    MAX_ENERGY = 60

    # Lighting
    MAX_LIGHTING = 100