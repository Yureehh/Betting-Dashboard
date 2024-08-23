"""
Paths Module

This module defines and manages the paths to data directories and files used in the project.
It ensures that the necessary directories are created and available for data storage and access.
"""

from pathlib import Path

# Define the base directory path relative to the current working directory
BASE_DIR = Path.cwd()

# Directories for data storage
IMGS_DIR = BASE_DIR / "imgs"

# Ensure that the necessary directories exist
for directory in [IMGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Paths for logo images
LOGO_PATH = str(IMGS_DIR / "logo.png")
RELATIVE_LOGO_PATH = "imgs/logo.png"
