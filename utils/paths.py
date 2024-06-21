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

# Bets ledger
BETS_PATH = DATA_DIR / "bets_ledger.csv"
