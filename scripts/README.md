# Scripts for AI Roast Machine

This directory contains utility scripts for the AI Roast Machine project.

## Available Scripts

### Docker Scripts

- `run_docker.sh`: Script to start and manage Docker containers
- `run_openrouter.sh`: Script to run OpenRouter integration

### Testing Scripts

- `test_openrouter.py`: Script to test the OpenRouter connector
- `test_api.py`: Script to test the API endpoints
- `test_health.py`: Script to check the health of the services
- `test_ai_roast.py`: Script to test the AI roasting functionality

### Setup Scripts

- `setup_environment.py`: Script to set up the environment for the project
- `download_nltk.py`: Script to download NLTK data

### API Scripts

- `run_api.py`: Script to run the API server
- `run_api_debug.py`: Script to run the API server in debug mode

### Analysis Scripts

- `model_comparison.py`: Script to compare different AI models

## Usage

Most scripts can be run directly from the command line:

```bash
python scripts/script_name.py
```

For shell scripts, use:

```bash
./scripts/script_name.sh
```

Some scripts may require additional arguments. Run with `--help` to see available options:

```bash
python scripts/script_name.py --help
``` 