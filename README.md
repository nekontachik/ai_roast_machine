# AI Roast Machine 🔥🤖

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-✅-blue.svg)](https://www.docker.com/)
[![Build Status](https://github.com/YOUR_USERNAME/AI-Roast-Machine/actions/workflows/tests.yml/badge.svg)](https://github.com/YOUR_USERNAME/AI-Roast-Machine/actions)

## 🚀 Features
- ✅ AI model testing with **LangTest, DeepChecks, and TextAttack**
- 🎭 **Roast Mode** – Generates sarcastic AI model evaluations
- 🖼️ **Meme Generator** – Creates AI failure memes
- 🔥 Supports **Docker & GitHub Actions**

## 📋 Project Structure

- `main.py` - Flask web application
- `minimal_test.py` - Lightweight test script (no NLTK/TextAttack dependencies)
- `test_ai_roast.py` - Full test script with mock data
- `download_nltk.py` - Script to pre-download NLTK packages and patch TextAttack
- `src/` - Core modules
  - `roast_generator.py` - Generates humorous roasts
  - `meme_generator.py` - Creates memes
  - `test_runner.py` - Runs model tests
- `models/` - Place your models here
- `test_results/` - Test results and roasts
- `memes/` - Generated memes
- `logs/` - Application logs

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run the minimal test script
docker-compose run --rm ai-roast-machine python -u minimal_test.py
```

### Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt
pip install tqdm

# Download NLTK packages and patch TextAttack
python download_nltk.py

# Run the minimal test
python minimal_test.py

# Or run the Flask app
python main.py
```

## 🧪 Testing Options

### Minimal Test
Use `minimal_test.py` for quick testing without NLTK/TextAttack dependencies:
```bash
python minimal_test.py
```

### Full Test with Mock Data
Use `test_ai_roast.py` for testing with mock data:
```bash
python test_ai_roast.py
```

## 🐳 Docker Options

The project includes:
- `dockerfile` - Docker image definition
- `docker-compose.yml` - Docker Compose configuration

To customize:
- Edit `dockerfile` to change the base image or dependencies
- Edit `docker-compose.yml` to change ports, volumes, or environment variables

## 🔧 Troubleshooting

### NLTK Download Issues
If you experience NLTK download loops:
1. Run `python download_nltk.py` to pre-download packages
2. Set the `NLTK_DATA` environment variable: `export NLTK_DATA=~/nltk_data`

### TextAttack Issues
If TextAttack hangs during initialization:
1. Run `python download_nltk.py` to patch TextAttack
2. Use `minimal_test.py` instead of the full test runner

## Overview

The AI Roast Machine is a system that:

1. Tests AI models using various datasets and prompts
2. Generates performance metrics for the models
3. Creates humorous "roasts" based on the model's performance
4. Generates meme images to visualize the results

## Features

- **Model Testing**: Test text generation models from Hugging Face
- **Diverse Datasets**: Use built-in datasets or create your own
- **Performance Metrics**: Measure speed, diversity, and other metrics
- **Humorous Roasts**: Generate funny critiques of model performance
- **Meme Generation**: Create visual representations of results
- **API Access**: Access all functionality through a FastAPI interface
- **Docker Support**: Run everything in isolated containers

## Getting Started

### Prerequisites

- Python 3.8+
- Docker (optional)
- 2GB+ of free disk space

### Installation

#### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-roast-machine.git
cd ai-roast-machine

# Build and run with Docker
docker-compose up -d
```

#### Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-roast-machine.git
cd ai-roast-machine

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API
python run_api.py
```

## Usage

### API Endpoints

- **GET /health**: Check if the API is running
- **POST /test**: Test an AI model
- **POST /roast**: Generate a roast based on test results
- **POST /meme**: Generate a meme based on test results

### Testing a Model

```bash
curl -X POST "http://localhost:8000/test" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "gpt2",
    "model_type": "text-generation",
    "prompts": ["Hello, how are you?", "What is AI?"]
  }'
```

### Generating a Roast

```bash
curl -X POST "http://localhost:8000/roast" \
  -H "Content-Type: application/json" \
  -d '{
    "test_results": {
      "model_name": "gpt2",
      "overall_score": 0.75,
      "metrics": {
        "accuracy": 0.8,
        "speed": 0.7,
        "diversity": 0.75
      }
    }
  }'
```

### Running Improvements

The project includes a script to run all improvements:

```bash
# Generate datasets, test models, and create roasts/memes
python src/run_improvements.py

# Test specific models
python src/run_improvements.py --models "gpt2,distilgpt2"

# Use custom prompts
python src/run_improvements.py --custom-prompts my_prompts.txt

# Skip certain steps
python src/run_improvements.py --skip-datasets --skip-roasts
```

## Project Structure

```
ai-roast-machine/
├── docker-compose.yml      # Docker configuration
├── requirements.txt        # Python dependencies
├── run_api.py              # API entry point
├── run_api_debug.py        # Debug version of API
├── src/                    # Source code
│   ├── api.py              # FastAPI implementation
│   ├── huggingface_tester.py  # Model testing with Hugging Face
│   ├── dataset_generator.py   # Dataset generation
│   └── run_improvements.py    # Script to run improvements
├── datasets/               # Generated datasets
├── test_results/           # Test results
├── memes/                  # Generated memes
├── logs/                   # Log files
└── notebooks/              # Jupyter notebooks
```

## Recent Improvements

1. **Real Model Testing**: Added integration with Hugging Face for testing real AI models
2. **Expanded Test Datasets**: Created diverse datasets for comprehensive testing
3. **Enhanced Meme Generation**: Implemented actual image generation for memes
4. **Improved Roasts**: Added more diverse and specific roasts based on metrics
5. **Comprehensive Logging**: Added detailed logging throughout the system

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Hugging Face for their amazing transformers library
- FastAPI for the efficient API framework
- The AI community for inspiration

## Running with Docker for Real Model Testing

For the best experience with real AI model testing, we recommend using Docker. This approach provides better resource management and isolation, which is crucial when working with AI models.

### Quick Start with Docker

```bash
# Make the run script executable
chmod +x run_docker.sh

# Run the Docker setup
./run_docker.sh
```

This will:
1. Create necessary directories
2. Build and start all Docker containers
3. Show you the URLs for all services

### Docker Services

The Docker setup includes several services:

- **API**: The main FastAPI service at http://localhost:8000
- **Debug API**: A debug version of the API at http://localhost:8001
- **Jupyter Notebook**: For interactive development at http://localhost:8888
- **Report Viewer**: A simple web server to view test results at http://localhost:8080
- **Improvements**: A service to run the improvements script

### Resource Management

Each Docker service is configured with resource limits to prevent memory issues:
- 4GB memory limit per container
- 2 CPU cores per container

You can adjust these limits in the `docker-compose.yml` file if needed.

### Running Tests with Real Models

To run tests with real models:

```bash
# Run the improvements service
docker-compose run --rm improvements python -m src.run_improvements --models "distilgpt2" --max-samples 5

# Or test a specific model
docker-compose run --rm improvements python -m src.run_improvements --models "gpt2" --max-samples 3
```

### Environment Variables

The Docker setup uses environment variables to control behavior:

- `USE_REAL_MODELS`: Set to "true" to use real Hugging Face models
- `MODEL_DEVICE`: Set to "cpu" or "cuda" for GPU support (if available)

These are already configured in the docker-compose.yml file.
