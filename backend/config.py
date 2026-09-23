import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = BASE_DIR / "database" / "codevanta.db"

# Execution constraints
DEFAULT_TIMEOUT_SECONDS = 30.0
MAX_OUTPUT_LENGTH = 10000
MAX_CODE_LENGTH = 65536

# Command paths (uses system PATH by default)
PYTHON_EXECUTABLE = "python"
JAVAC_EXECUTABLE = "javac"
JAVA_EXECUTABLE = "java"
