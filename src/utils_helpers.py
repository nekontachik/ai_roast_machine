"""Utility functions for the AI Roast Machine."""
import os
import json
import logging
from logging.handlers import RotatingFileHandler
from typing import Dict, List, Any, Optional, Union
import datetime

logger = logging.getLogger(__name__)


def setup_logging(log_file: str, log_level: str, log_format: str = "json") -> None:
    """Configure logging with enhanced features.
    
    Args:
        log_file: Path to log file
        log_level: Logging level (DEBUG, INFO, etc.)
        log_format: Log format ('json' or 'text')
    """
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Set up basic configuration
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Define formatters
    if log_format == "json":
        formatter = logging.Formatter(
            lambda x: json.dumps({
                'timestamp': datetime.datetime.utcnow().isoformat(),
                'level': x.levelname,
                'module': x.module,
                'function': x.funcName,
                'line': x.lineno,
                'message': x.getMessage(),
                'extra': getattr(x, 'extra', {})
            })
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(module)s:%(funcName)s:%(lineno)d] - %(message)s'
        )
    
    # Set up file handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Log initial setup
    logging.info("Logging configured", extra={
        'log_file': log_file,
        'log_level': log_level,
        'log_format': log_format
    })


def save_json(data: Dict[str, Any], output_path: str) -> str:
    """Save data to a JSON file.

    Args:
        data: Data to save
        output_path: Path to save the data

    Returns:
        Path to the saved file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    
    logger.info(f"Data saved to {output_path}")
    return output_path


def load_json(input_path: str) -> Dict[str, Any]:
    """Load data from a JSON file.

    Args:
        input_path: Path to the JSON file

    Returns:
        Data loaded from the file
    """
    try:
        with open(input_path, "r") as f:
            data = json.load(f)
        
        logger.info(f"Data loaded from {input_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading JSON from {input_path}: {str(e)}")
        return {}


def generate_timestamp() -> str:
    """Generate a timestamp string.

    Returns:
        Timestamp string in the format YYYYMMDD_HHMMSS
    """
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def generate_output_filename(prefix: str, extension: str = "json") -> str:
    """Generate an output filename with a timestamp.

    Args:
        prefix: Prefix for the filename
        extension: File extension

    Returns:
        Filename with timestamp
    """
    timestamp = generate_timestamp()
    return f"{prefix}_{timestamp}.{extension}"


def log_with_context(**kwargs: Any) -> Dict[str, Any]:
    """Create a context dictionary for structured logging.
    
    Args:
        **kwargs: Key-value pairs to add to context
        
    Returns:
        Dictionary with context information
    """
    return {'extra': kwargs}
