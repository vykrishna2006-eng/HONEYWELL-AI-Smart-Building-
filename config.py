"""
=========================================================
AI Smart Building Optimization System
Global Configuration
=========================================================
"""

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# --------------------------------------------------------
# Project Information
# --------------------------------------------------------

APP_NAME = os.getenv("APP_NAME", "AI Smart Building Optimization")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "True") == "True"

# --------------------------------------------------------
# Base Directories
# --------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATASET_DIR = BASE_DIR / "datasets"
RAW_DATA_DIR = DATASET_DIR / "raw"
PROCESSED_DATA_DIR = DATASET_DIR / "processed"

DATABASE_DIR = BASE_DIR / "database"

MODEL_DIR = BASE_DIR / "ml" / "saved_models"

ENERGYPLUS_DIR = BASE_DIR / "energyplus"

REPORT_DIR = BASE_DIR / "reports"

LOG_DIR = BASE_DIR / "logs"

# --------------------------------------------------------
# Dataset
# --------------------------------------------------------

RAW_DATASET = RAW_DATA_DIR / "Smart_Building_Industrial_Dataset_1Year.xlsx"

PROCESSED_DATASET = PROCESSED_DATA_DIR / "clean_sensor_data.csv"

# --------------------------------------------------------
# Database
# --------------------------------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DATABASE_DIR/'smart_building.db'}"
)

# --------------------------------------------------------
# Server
# --------------------------------------------------------

HOST = os.getenv("HOST", "0.0.0.0")

PORT = int(os.getenv("PORT", "8000"))

# --------------------------------------------------------
# Ollama
# --------------------------------------------------------

OLLAMA_HOST = os.getenv("OLLAMA_HOST")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

# --------------------------------------------------------
# EnergyPlus
# --------------------------------------------------------

ENERGYPLUS_OUTPUT = os.getenv("ENERGYPLUS_OUTPUT")

# --------------------------------------------------------
# Logging
# --------------------------------------------------------

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")