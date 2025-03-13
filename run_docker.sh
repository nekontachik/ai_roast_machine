#!/bin/bash
# Script to run the AI Roast Machine in Docker

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

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

# Create necessary directories
echo -e "${YELLOW}Creating necessary directories...${NC}"
mkdir -p logs test_results memes notebooks datasets

# Build and start the containers
echo -e "${YELLOW}Building and starting Docker containers...${NC}"
docker-compose up -d

# Check if containers are running
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Docker containers started successfully!${NC}"
    echo -e "${YELLOW}Services available at:${NC}"
    echo -e "  - API: ${GREEN}http://localhost:8000${NC}"
    echo -e "  - API Documentation: ${GREEN}http://localhost:8000/docs${NC}"
    echo -e "  - Debug API: ${GREEN}http://localhost:8001${NC}"
    echo -e "  - Jupyter Notebook: ${GREEN}http://localhost:8888${NC}"
    echo -e "  - Report Viewer: ${GREEN}http://localhost:8080${NC}"
    
    # Show running containers
    echo -e "\n${YELLOW}Running containers:${NC}"
    docker-compose ps
    
    # Show logs for the API container
    echo -e "\n${YELLOW}API container logs:${NC}"
    docker-compose logs --tail=10 api
    
    echo -e "\n${GREEN}To run tests with real models:${NC}"
    echo -e "  docker-compose run --rm improvements python -m src.run_improvements --models \"distilgpt2\" --max-samples 5"
    
    echo -e "\n${GREEN}To stop the containers:${NC}"
    echo -e "  docker-compose down"
else
    echo -e "${RED}Failed to start Docker containers. Check the logs for errors.${NC}"
    exit 1
fi 