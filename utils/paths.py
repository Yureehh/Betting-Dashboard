"""
Paths Folder

This file contains the paths to the data directories.
It is used to ensure that the necessary directories are created and available for data storage.
"""

import os
from pathlib import Path

# Define the base directory path relative to this file's location
BASE_DIR = Path(os.getcwd())

# Directories for data storage
DATA_DIR = BASE_DIR / "data"
MODEL_VALIDATION_DIR = DATA_DIR / "model_validation"

# Bets ledger
BETS_PATH = DATA_DIR / "bets_ledger.csv"

# Model validation
ACCURACY_OVER_SAMPLES = MODEL_VALIDATION_DIR / "LightGBM_Accuracy_Over_Samples.png"
HISTORICAL_ACCURACY = MODEL_VALIDATION_DIR / "LightGBM_Historical_Accuracy.png"
LEAGUE_ACCURACIES = MODEL_VALIDATION_DIR / "LightGBM_league_accuracies.json"
MODEL_METRICS = MODEL_VALIDATION_DIR / "LightGBM_metrics.json"
