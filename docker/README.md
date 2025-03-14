# Docker Setup for AI Roast Machine

This directory contains all Docker-related files for the AI Roast Machine project.

## Files

- `Dockerfile`: Defines the Docker image for all services
- `docker-compose.yml`: Defines the services and their configurations
- `run_docker.sh`: Script to easily start and manage Docker containers

## Services

The Docker setup includes the following services:

1. **api**: Main API service for testing AI models
2. **debug**: Debug version of the API with debugpy support
3. **jupyter**: Jupyter notebook server for interactive testing
4. **report-viewer**: Simple web server for viewing test results
5. **improvements**: Service for running model improvements
6. **openrouter**: OpenRouter API integration

## Usage

From the project root, run:

```bash
./run_docker.sh
```

This will start all the necessary services. For more options, run:

```bash
./run_docker.sh --help
```

## Resource Management

Each service has resource limits configured to prevent memory issues:

- Memory limits: 4GB per service
- CPU limits: 2 cores per service (1 core for OpenRouter)

## Volumes

The following volumes are shared between services:

- `./src`: Source code
- `./logs`: Log files
- `./test_results`: Test results
- `./memes`: Generated memes
- `./notebooks`: Jupyter notebooks
- `./datasets`: Test datasets
- `huggingface_cache`: Shared cache for Hugging Face models

## Ports

- API: 8000
- Debug API: 8001
- Jupyter: 8888
- Report Viewer: 8080
- OpenRouter API: 8002 