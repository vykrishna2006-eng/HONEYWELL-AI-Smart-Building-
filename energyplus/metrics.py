import pandas as pd
from pathlib import Path

from energyplus.parser import get_csv_file


def _load_dataframe():
    csv_file = get_csv_file()

    print("CSV File:", csv_file)

    if csv_file is None:
        return None

    csv_path = Path(csv_file)

    if not csv_path.exists():
        print("CSV does not exist!")
        return None

    try:
        df = pd.read_csv(csv_path)

        print("\n========== CSV COLUMNS ==========")
        for col in df.columns:
            print(col)
        print("=================================\n")

        return df

    except Exception as e:
        print(e)
        return None

def _find_column(df, keywords):
    """
    Finds the first column whose name contains all keywords.
    """

    if df is None:
        return None

    for column in df.columns:

        name = column.lower()

        if all(word.lower() in name for word in keywords):
            return column

    return None


def _mean(df, column):

    if df is None or column is None:
        return None

    try:
        return round(float(df[column].mean()), 2)
    except Exception:
        return None


# --------------------------------------------------------
# Indoor Temperature
# --------------------------------------------------------

def get_indoor_temperature():

    df = _load_dataframe()

    if df is None:
        return None

    cols = [
        c for c in df.columns
        if "Zone Air Temperature" in c
    ]

    if not cols:
        return None

    return round(df[cols].mean().mean(), 2)

# --------------------------------------------------------
# Radiant Temperature
# --------------------------------------------------------

def get_radiant_temperature():
    df = _load_dataframe()

    cols = [c for c in df.columns if "Zone Mean Radiant Temperature" in c]

    if not cols:
        return None

    return round(df[cols].mean().mean(), 2)

# --------------------------------------------------------
# Relative Humidity
# --------------------------------------------------------

def get_humidity():
    df = _load_dataframe()

    cols = [c for c in df.columns if "Zone Air Relative Humidity" in c]

    if not cols:
        return None

    return round(df[cols].mean().mean(), 2)


# --------------------------------------------------------
# CO2
# --------------------------------------------------------

def get_co2():

    df = _load_dataframe()

    col = _find_column(
        df,
        [
            "CO2"
        ]
    )

    return _mean(df, col)


# --------------------------------------------------------
# Occupancy
# --------------------------------------------------------

def get_occupancy():
    df = _load_dataframe()

    cols = [c for c in df.columns if "People Occupant Count" in c]

    if not cols:
        return None

    return round(df[cols].mean().mean(), 2)


# --------------------------------------------------------
# Outdoor Temperature
# --------------------------------------------------------

def get_outdoor_temperature():

    df = _load_dataframe()

    if df is None:
        return None

    cols = [
        c for c in df.columns
        if "Site Outdoor Air Drybulb Temperature" in c
    ]

    if not cols:
        return None

    return round(df[cols].mean().mean(), 2)


# --------------------------------------------------------
# Wind Speed
# --------------------------------------------------------

def get_wind_speed():
    df = _load_dataframe()

    cols = [c for c in df.columns if "Site Wind Speed" in c]

    if not cols:
        return None

    return round(df[cols].mean().mean(), 2)


# --------------------------------------------------------
# Solar Radiation
# --------------------------------------------------------

def get_solar_radiation():
    df = _load_dataframe()

    cols = [c for c in df.columns if "Site Direct Solar Radiation Rate per Area" in c]

    if not cols:
        return None

    return round(df[cols].mean().mean(), 2)


# --------------------------------------------------------
# Cooling Energy
# --------------------------------------------------------

def get_cooling_energy():

    df = _load_dataframe()

    if df is None:
        return None

    cols = [
        c for c in df.columns
        if "Zone Air System Sensible Cooling Rate" in c
    ]

    if not cols:
        return None

    return round(df[cols].sum().sum() / 1000, 2)

# --------------------------------------------------------
# Heating Energy
# --------------------------------------------------------

def get_heating_energy():

    df = _load_dataframe()

    if df is None:
        return None

    cols = [
        c for c in df.columns
        if "Zone Air System Sensible Heating Rate" in c
    ]

    if not cols:
        return None

    return round(df[cols].sum().sum() / 1000, 2)

def get_dewpoint():

    df = _load_dataframe()

    if df is None:
        return None

    cols = [
        c for c in df.columns
        if "Zone Mean Air Dewpoint Temperature" in c
    ]

    if not cols:
        return None

    return round(df[cols].mean().mean(), 2)


# --------------------------------------------------------
# Total Energy
# --------------------------------------------------------

def get_total_energy():

    cooling = get_cooling_energy() or 0

    heating = get_heating_energy() or 0

    return round(cooling + heating, 2)


# --------------------------------------------------------
# Peak Demand
# --------------------------------------------------------

def get_peak_demand():

    df = _load_dataframe()

    if df is None:
        return None

    cols = [
        c for c in df.columns
        if "Chiller Electricity Rate" in c
    ]

    if not cols:
        return None

    return round(df[cols].max().max() / 1000, 2)


# --------------------------------------------------------
# Carbon Intensity
# --------------------------------------------------------

def get_carbon_intensity():

    """
    Placeholder.

    Later this can be connected to:
    - ElectricityMap API
    - WattTime
    - Utility carbon datasets

    Current default:
        420 gCO₂/kWh
    """

    return 420


# --------------------------------------------------------
# Air Speed
# --------------------------------------------------------

def get_air_speed():
    """
    Placeholder until available from simulation.
    """

    return 0.15


# --------------------------------------------------------
# All Metrics
# --------------------------------------------------------

def get_all_metrics():

    return {

        "indoor_temperature":
            get_indoor_temperature(),

        "radiant_temperature":
            get_radiant_temperature(),

        "humidity":
            get_humidity(),

        "air_speed":
            get_air_speed(),

        "co2":
            get_co2(),

        "occupancy":
            get_occupancy(),

        "outdoor_temperature":
            get_outdoor_temperature(),

        "wind_speed":
            get_wind_speed(),

        "solar_radiation":
            get_solar_radiation(),

        "cooling_energy":
            get_cooling_energy(),

        "heating_energy":
            get_heating_energy(),

        "total_energy":
            get_total_energy(),

        "peak_demand":
            get_peak_demand(),

        "carbon_intensity":
            get_carbon_intensity(),
    }


if __name__ == "__main__":

    from pprint import pprint

    print("Humidity:", get_humidity())
    
    print("Radiant:", get_radiant_temperature())
    print("Occupancy:", get_occupancy())
    print("Wind:", get_wind_speed())
    print("Solar:", get_solar_radiation())
    
 