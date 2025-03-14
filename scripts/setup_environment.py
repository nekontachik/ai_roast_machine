#!/usr/bin/env python
"""
Setup Environment Script

This script sets up the environment for the AI Roast Machine by:
1. Creating necessary directories
2. Checking for required files
3. Setting up environment variables
"""
import os
import sys
import logging
from pathlib import Path
import shutil
import dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("setup_environment")

# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Directories to create
DIRECTORIES = [
    "logs",
    "test_results",
    "memes",
    "datasets",
    "notebooks",
    "models",
]

# Required files
REQUIRED_FILES = [
    ".env",
]

def create_directories():
    """Create necessary directories if they don't exist."""
    for directory in DIRECTORIES:
        dir_path = PROJECT_ROOT / directory
        if not dir_path.exists():
            logger.info(f"Creating directory: {directory}")
            dir_path.mkdir(parents=True, exist_ok=True)
        else:
            logger.info(f"Directory already exists: {directory}")

def check_required_files():
    """Check for required files and create templates if they don't exist."""
    # Check for .env file
    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        logger.warning(f"Required file not found: .env")
        logger.info("Creating template .env file")
        with open(env_file, "w") as f:
            f.write("""# AI Roast Machine Environment Variables

# OpenRouter API Key
OPENROUTER_API_KEY=your_api_key_here

# Model Settings
USE_REAL_MODELS=true
MODEL_DEVICE=cpu

# Logging
LOG_LEVEL=INFO

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG_API_PORT=8001
""")
        logger.warning("Please edit the .env file with your actual values")
    else:
        logger.info("Found .env file")
        # Load environment variables
        dotenv.load_dotenv(env_file)

def check_notebooks():
    """Check for Jupyter notebooks and create templates if they don't exist."""
    # Check for OpenRouter tests notebook
    notebook_file = PROJECT_ROOT / "notebooks" / "openrouter_tests.ipynb"
    if not notebook_file.exists():
        logger.info("Creating template OpenRouter tests notebook")
        template_notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["# OpenRouter Tests\n", "\n", "This notebook provides interactive testing of AI models using OpenRouter."]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": ["import sys\n", "import os\n", "import json\n", "from pathlib import Path\n", "\n", "# Add the project root to the path\n", "project_root = Path().resolve().parent\n", "sys.path.append(str(project_root))\n", "\n", "# Import the OpenRouter connector\n", "from src.openrouter_connector import query_model, get_available_models, test_model_bias"]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["## Available Models\n", "\n", "Let's first check what models are available through OpenRouter."]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": ["# Get available models\n", "models = get_available_models()\n", "print(f\"Found {len(models)} models\")\n", "\n", "# Display the first 5 models\n", "for i, model in enumerate(models[:5]):\n", "    print(f\"{i+1}. {model}\")\n"]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["## Test a Model\n", "\n", "Now let's test a model with a simple prompt."]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": ["# Test a model\n", "model_name = \"mistral-7b\"\n", "prompt = \"What is artificial intelligence?\"\n", "\n", "response = query_model(prompt, model=model_name)\n", "print(response)"]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["## Test Model Bias\n", "\n", "Let's test the model for bias."]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": ["# Test model bias\n", "model_name = \"mistral-7b\"\n", "bias_results = test_model_bias(model_name)\n", "\n", "print(f\"Bias score: {bias_results['bias_score']}\")\n", "print(f\"Potentially biased responses: {bias_results['biased_responses']}\")\n"]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "codemirror_mode": {
                        "name": "ipython",
                        "version": 3
                    },
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.8.10"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        # Create the notebook directory if it doesn't exist
        notebook_dir = notebook_file.parent
        if not notebook_dir.exists():
            notebook_dir.mkdir(parents=True, exist_ok=True)
            
        # Write the notebook file
        import json
        with open(notebook_file, "w") as f:
            json.dump(template_notebook, f, indent=2)
            
        logger.info(f"Created template notebook: {notebook_file}")
    else:
        logger.info(f"Found notebook: {notebook_file}")

def main():
    """Main function to set up the environment."""
    logger.info("Setting up environment for AI Roast Machine")
    
    # Create directories
    create_directories()
    
    # Check for required files
    check_required_files()
    
    # Check for notebooks
    check_notebooks()
    
    logger.info("Environment setup complete")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 