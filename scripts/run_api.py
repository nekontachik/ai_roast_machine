#!/usr/bin/env python
"""Run the FastAPI server for AI Roast Machine."""
from typing import Any
import uvicorn  # type: ignore
from src.config import config

def run_server() -> None:
    """Run the FastAPI server."""
    print(f"✨ Starting {config['APP_NAME']} API v{config['APP_VERSION']}")
    log_level = str(config["LOG_LEVEL"]).lower()
    uvicorn.run(
        "src.api:app",
        host=config["HOST"],
        port=config["PORT"],
        reload=config["DEBUG"],
        log_level=log_level
    )

if __name__ == "__main__":
    run_server() 