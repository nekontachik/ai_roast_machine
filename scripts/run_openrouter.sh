#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo -e "${RED}Error: Python is not installed or not in PATH${NC}"
    exit 1
fi

# Function to print usage information
print_usage() {
    echo -e "${BLUE}Usage:${NC} $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  cli                  Run the interactive CLI menu"
    echo "  api                  Start the FastAPI server"
    echo "  jupyter              Launch the Jupyter notebook"
    echo "  list-models          List available models from OpenRouter"
    echo "  test MODEL PROMPT    Test a specific model with a custom prompt"
    echo "  bias-test MODEL      Run bias tests on a specific model"
    echo "  help                 Show this help message"
    echo
    echo "Examples:"
    echo "  $0 cli"
    echo "  $0 list-models"
    echo "  $0 test mistral-7b \"Explain quantum computing\""
    echo "  $0 bias-test mistral-7b"
}

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Warning: .env file not found. Creating a template...${NC}"
    echo "OPENROUTER_API_KEY=your_api_key_here" > .env
    echo -e "${BLUE}Please edit the .env file and add your OpenRouter API key${NC}"
fi

# Create necessary directories if they don't exist
mkdir -p logs test_results

# Set PYTHONPATH to include the project root
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Process command line arguments
case "$1" in
    cli)
        echo -e "${GREEN}Starting OpenRouter CLI...${NC}"
        python -m src.menu
        ;;
    api)
        echo -e "${GREEN}Starting OpenRouter API server...${NC}"
        uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
        ;;
    jupyter)
        echo -e "${GREEN}Starting Jupyter notebook...${NC}"
        if [ -f "notebooks/openrouter_tests.ipynb" ]; then
            jupyter notebook notebooks/openrouter_tests.ipynb
        else
            echo -e "${RED}Notebook not found. Creating a new one...${NC}"
            mkdir -p notebooks
            touch notebooks/openrouter_tests.ipynb
            jupyter notebook notebooks/openrouter_tests.ipynb
        fi
        ;;
    list-models)
        echo -e "${GREEN}Fetching available models from OpenRouter...${NC}"
        python -c "from src.openrouter_connector import get_available_models; models = get_available_models(); print('\n'.join([f'{i+1}. {m.get(\"id\", \"Unknown\")} - {m.get(\"name\", \"Unknown\")}' for i, m in enumerate(models)]))"
        ;;
    test)
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo -e "${RED}Error: MODEL and PROMPT are required for test command${NC}"
            print_usage
            exit 1
        fi
        echo -e "${GREEN}Testing model $2 with prompt: $3${NC}"
        python -c "from src.openrouter_connector import query_model, extract_text_from_response; response = query_model('$3', '$2'); print(extract_text_from_response(response))"
        ;;
    bias-test)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: MODEL is required for bias-test command${NC}"
            print_usage
            exit 1
        fi
        echo -e "${GREEN}Running bias test on model $2...${NC}"
        python -c "from src.openrouter_connector import test_model_bias; results = test_model_bias('$2'); print(f'Bias score: {results[\"bias_score\"]:.2f}'); print(f'Potentially biased responses: {results[\"potentially_biased_responses\"]} out of {len(results[\"prompts\"])}')"
        ;;
    help|--help|-h)
        print_usage
        ;;
    *)
        echo -e "${RED}Error: Unknown command '$1'${NC}"
        print_usage
        exit 1
        ;;
esac

exit 0 