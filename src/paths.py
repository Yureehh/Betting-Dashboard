"""
Paths Module

This file contains the paths to the data directories and files used in the project.
It ensures that the necessary directories are created and available for data storage and access.
"""

import os
from pathlib import Path

# Define the base directory path relative to the current working directory
BASE_DIR = Path(os.getcwd())

# Directories for data storage
DATA_DIR = BASE_DIR / "data"
MODEL_VALIDATION_DIR = DATA_DIR / "model_validation"

# Ensure that the necessary directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
MODEL_VALIDATION_DIR.mkdir(parents=True, exist_ok=True)

# Paths for model validation outputs
ACCURACY_OVER_SAMPLES_PATH = (
    MODEL_VALIDATION_DIR / "OutcomePrediction_Accuracy_Over_Samples.png"
)
HISTORICAL_ACCURACY_PATH = (
    MODEL_VALIDATION_DIR / "OutcomePrediction_Historical_Accuracy.png"
)
LEAGUE_ACCURACIES_PATH = (
    MODEL_VALIDATION_DIR / "OutcomePrediction_league_accuracies.json"
)
MODEL_METRICS_PATH = MODEL_VALIDATION_DIR / "OutcomePrediction_metrics.json"
