#!/bin/bash
# Script to run the AI Roast Machine in Docker

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${GREEN}Starting AI Roast Machine with Docker...${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found. Creating a template .env file.${NC}"
    echo "OPENROUTER_API_KEY=your_api_key_here" > .env
    echo -e "${YELLOW}Please edit the .env file and add your OpenRouter API key.${NC}"
fi

# Create necessary directories
echo -e "${YELLOW}Creating necessary directories...${NC}"
mkdir -p logs test_results memes notebooks datasets

# Parse command line arguments
SERVICES="api debug jupyter report-viewer improvements"
OPENROUTER=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --openrouter)
            OPENROUTER=true
            shift
            ;;
        --only-openrouter)
            SERVICES="openrouter-api openrouter-cli"
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Usage: $0 [--openrouter] [--only-openrouter]"
            exit 1
            ;;
    esac
done

# Add OpenRouter services if requested
if [ "$OPENROUTER" = true ]; then
    SERVICES="$SERVICES openrouter-api openrouter-cli"
fi

# Build and start the containers
echo -e "${YELLOW}Building and starting Docker containers...${NC}"
docker-compose up -d $SERVICES

# Check if containers are running
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Docker containers started successfully!${NC}"
    echo -e "${YELLOW}Services available at:${NC}"
    echo -e "  - API: ${GREEN}http://localhost:8000${NC}"
    echo -e "  - API Documentation: ${GREEN}http://localhost:8000/docs${NC}"
    echo -e "  - Debug API: ${GREEN}http://localhost:8001${NC}"
    echo -e "  - Jupyter Notebook: ${GREEN}http://localhost:8888${NC}"
    echo -e "  - Report Viewer: ${GREEN}http://localhost:8080${NC}"
    
    # Show OpenRouter services if enabled
    if [ "$OPENROUTER" = true ] || [ "$SERVICES" = "openrouter-api openrouter-cli" ]; then
        echo -e "  - OpenRouter API: ${GREEN}http://localhost:8002${NC}"
        echo -e "  - OpenRouter API Documentation: ${GREEN}http://localhost:8002/docs${NC}"
    fi
    
    # Show running containers
    echo -e "\n${YELLOW}Running containers:${NC}"
    docker-compose ps
    
    # Show logs for the API container
    echo -e "\n${YELLOW}API container logs:${NC}"
    docker-compose logs --tail=10 api
    
    echo -e "\n${GREEN}To run tests with real models:${NC}"
    echo -e "  docker-compose run --rm improvements python -m src.run_improvements --models \"distilgpt2\" --max-samples 5"
    
    # Show OpenRouter commands if enabled
    if [ "$OPENROUTER" = true ] || [ "$SERVICES" = "openrouter-api openrouter-cli" ]; then
        echo -e "\n${GREEN}To run OpenRouter CLI:${NC}"
        echo -e "  docker-compose run --rm openrouter-cli python -m src.menu"
        
        echo -e "\n${GREEN}To test a model with OpenRouter:${NC}"
        echo -e "  docker-compose run --rm openrouter-cli python -m src.menu --model mistral-7b --prompt \"Your prompt here\""
        
        echo -e "\n${GREEN}To run bias tests with OpenRouter:${NC}"
        echo -e "  docker-compose run --rm openrouter-cli python -m src.menu --model mistral-7b --bias-test"
    fi
    
    echo -e "\n${GREEN}To stop the containers:${NC}"
    echo -e "  docker-compose down"
else
    echo -e "${RED}Failed to start Docker containers. Check the logs for errors.${NC}"
    exit 1
fi 