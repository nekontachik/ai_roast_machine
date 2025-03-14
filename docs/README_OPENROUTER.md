# AI Roast Machine - OpenRouter Integration

This extension to the AI Roast Machine project adds support for testing and evaluating AI models using the [OpenRouter API](https://openrouter.ai/), which provides access to a wide range of AI models including those from Anthropic, OpenAI, and more.

## Features

- **OpenRouter Connector**: Query various AI models through a unified API
- **Interactive CLI**: Test models through a user-friendly command-line interface
- **FastAPI Endpoints**: Run tests and query models through a REST API
- **Jupyter Notebook**: Interactive analysis and visualization of model performance
- **Bias Testing**: Evaluate models for potential bias in responses

## Setup

### Prerequisites

- Python 3.8+
- OpenRouter API key (get one at [OpenRouter](https://openrouter.ai/))

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-roast-machine.git
   cd ai-roast-machine
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

## Usage

### CLI Mode

Run the interactive CLI menu:

```bash
./scripts/run_openrouter.sh cli
```

Command-line options:
```bash
# List available models
./scripts/run_openrouter.sh list-models

# Test a specific model with bias test
./scripts/run_openrouter.sh bias-test mistral-7b

# Test a specific model with a custom prompt
./scripts/run_openrouter.sh test mistral-7b "Your prompt here"
```

### FastAPI Mode

Start the API server:

```bash
./scripts/run_openrouter.sh api
```

API endpoints:
- `GET /models/`: List available models
- `POST /query/`: Query a model with a prompt
- `POST /run-tests/`: Run bias tests on a model
- `GET /test-results/`: Get all test results
- `GET /test-results/{model}`: Get test results for a specific model

Example API request:
```bash
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{"model": "mistral-7b", "prompt": "Explain quantum computing"}'
```

### Jupyter Notebook

Launch the Jupyter notebook:

```bash
./scripts/run_openrouter.sh jupyter
```

The notebook provides an interactive environment for:
- Fetching and displaying available models
- Testing individual models with custom prompts
- Comparing responses from multiple models
- Testing models for potential bias
- Saving and loading test results
- Performing advanced analysis on model responses

### Docker

If you're using Docker:

```bash
# Build and start the containers with OpenRouter support
./run_docker.sh --openrouter

# Start only the OpenRouter service
./run_docker.sh --only-openrouter

# Run the CLI in Docker
docker-compose run --rm openrouter python -m src.menu

# Run tests in Docker
docker-compose run --rm openrouter python -m src.menu --model mistral-7b --bias-test
```

## File Structure

- `src/openrouter_connector.py`: Core module for interacting with OpenRouter API
- `src/menu.py`: Interactive CLI interface
- `src/api.py`: FastAPI server implementation
- `notebooks/openrouter_tests.ipynb`: Jupyter notebook for interactive testing
- `scripts/run_openrouter.sh`: Script to run OpenRouter components
- `scripts/test_openrouter.py`: Test script for OpenRouter connector
- `logs/`: Directory for test results and logs

## Example Workflow

1. Start by exploring available models:
   ```bash
   ./scripts/run_openrouter.sh list-models
   ```

2. Run a bias test on a specific model:
   ```bash
   ./scripts/run_openrouter.sh bias-test mistral-7b
   ```

3. Compare multiple models using the interactive CLI:
   ```bash
   ./scripts/run_openrouter.sh cli
   # Then select option 2 to test multiple models
   ```

4. For more detailed analysis, use the Jupyter notebook:
   ```bash
   ./scripts/run_openrouter.sh jupyter
   ```

## Extending

To add new test types or metrics:

1. Add new functions to `src/openrouter_connector.py`
2. Update the CLI menu in `src/menu.py`
3. Add new endpoints to `src/api.py`
4. Create new analysis cells in the Jupyter notebook

## Troubleshooting

- **API Key Issues**: Ensure your OpenRouter API key is correctly set in the `.env` file
- **Model Availability**: Some models may be temporarily unavailable or require specific permissions
- **Rate Limiting**: OpenRouter may impose rate limits on API calls
- **Logging**: Check the logs in the `logs/` directory for detailed error information

## License

This project is licensed under the MIT License - see the LICENSE file for details. 