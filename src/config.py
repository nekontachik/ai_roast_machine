"""Configuration settings for the AI Roast Machine."""
import os
from typing import Dict, Any

# Load environment variables
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")

# Application info
APP_NAME = "AI Roast Machine"
APP_VERSION = "1.0.0"

# Output directories
TEST_OUTPUT_DIR = "test_results"
MEME_OUTPUT_DIR = "memes"

# Export config as a dictionary
config = {
    "DEBUG": DEBUG,
    "HOST": HOST,
    "PORT": PORT,
    "LOG_LEVEL": LOG_LEVEL,
    "LOG_FILE": LOG_FILE,
    "APP_NAME": APP_NAME,
    "APP_VERSION": APP_VERSION,
    "TEST_OUTPUT_DIR": TEST_OUTPUT_DIR,
    "MEME_OUTPUT_DIR": MEME_OUTPUT_DIR
} 