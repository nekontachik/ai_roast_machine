#!/usr/bin/env python
"""Run the FastAPI server for AI Roast Machine with debugpy enabled."""
from typing import Any
import debugpy
import uvicorn  # type: ignore
from src.config import config

def run_debug_server() -> None:
    """Run the FastAPI server in debug mode."""
    # Enable debugging
    debugpy.listen(("0.0.0.0", 5678))
    print("⚡ Debugpy server listening on port 5678")
    
    print(f"✨ Starting {config['APP_NAME']} API v{config['APP_VERSION']} in debug mode")
    uvicorn.run(
        "src.api:app",
        host=config["HOST"],
        port=config["PORT"],
        reload=True,  # Always reload in debug mode
        log_level="debug"
    )

if __name__ == "__main__":
    run_debug_server() 