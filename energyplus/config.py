from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Change this if your installation path is different
ENERGYPLUS_EXE = r"C:\EnergyPlusV26-1-0\energyplus.exe"

IDF_FILE = BASE_DIR / "idf" / "building.idf"

WEATHER_FILE = BASE_DIR / "weather" / "weather.epw"

OUTPUT_DIR = BASE_DIR / "output"