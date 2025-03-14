"""FastAPI server for AI Roast Machine with OpenRouter integration."""
import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import our modules
from .openrouter_connector import get_models, query_model, test_bias

# Configure logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("openrouter-api")

# Initialize FastAPI app
app = FastAPI(
    title="AI Roast Machine API",
    description="API for testing and evaluating AI models using OpenRouter",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define request and response models
class ModelQueryRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: Optional[int] = 1024
    temperature: Optional[float] = 0.7
    system_prompt: Optional[str] = None
    top_p: Optional[float] = 1.0
    frequency_penalty: Optional[float] = 0.0
    presence_penalty: Optional[float] = 0.0

class BiasTestRequest(BaseModel):
    model: str
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9

class TestResultsResponse(BaseModel):
    model: str
    timestamp: str
    results: Dict[str, Any]

# Helper function to save test results
def save_test_results(results: Dict[str, Any]) -> str:
    """Save test results to a JSON file.
    
    Args:
        results: Test results to save
        
    Returns:
        Path to saved results
    """
    # Add timestamp to results if not present
    if "timestamp" not in results:
        results["timestamp"] = datetime.now().isoformat()
    
    # Create filename based on model and timestamp
    model_name = results.get("model", "unknown")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/model_tests_{model_name}_{timestamp}.json"
    
    # Save to file
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    
    # Also append to the combined log file
    combined_log_file = "logs/model_tests.json"
    
    try:
        # Load existing log if it exists
        if os.path.exists(combined_log_file):
            with open(combined_log_file, "r") as f:
                try:
                    log_data = json.load(f)
                    if not isinstance(log_data, list):
                        log_data = [log_data]
                except json.JSONDecodeError:
                    log_data = []
        else:
            log_data = []
        
        # Append new results
        log_data.append(results)
        
        # Save updated log
        with open(combined_log_file, "w") as f:
            json.dump(log_data, f, indent=2)
            
    except Exception as e:
        logger.error(f"Error updating combined log file: {e}")
    
    logger.info(f"Saved test results to {filename}")
    return filename

# Define API endpoints
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "AI Roast Machine API",
        "version": "1.0.0",
        "description": "API for testing and evaluating AI models using OpenRouter",
        "endpoints": [
            {"path": "/models/", "description": "Get available models"},
            {"path": "/query/", "description": "Query a model with a prompt"},
            {"path": "/run-tests/", "description": "Run bias tests on a model"},
            {"path": "/test-results/", "description": "Get all test results"},
            {"path": "/test-results/{model}", "description": "Get test results for a specific model"}
        ]
    }

@app.get("/models/")
async def get_available_models():
    """Get available models from OpenRouter."""
    try:
        models = get_models()
        return {"models": models}
    except Exception as e:
        logger.error(f"Error getting models: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting models: {str(e)}")

@app.post("/query/")
async def query_model_endpoint(request: ModelQueryRequest):
    """Query a model with a prompt."""
    try:
        response = query_model(
            prompt=request.prompt,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            system_prompt=request.system_prompt,
            top_p=request.top_p,
            frequency_penalty=request.frequency_penalty,
            presence_penalty=request.presence_penalty
        )
        
        # Save results
        results = {
            "model": request.model,
            "prompt": request.prompt,
            "response": response,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "system_prompt": request.system_prompt
        }
        filename = save_test_results(results)
        
        return {
            "model": request.model,
            "response": response,
            "results_file": filename
        }
    except Exception as e:
        logger.error(f"Error querying model: {e}")
        raise HTTPException(status_code=500, detail=f"Error querying model: {str(e)}")

@app.post("/run-tests/")
async def run_tests(request: BiasTestRequest, background_tasks: BackgroundTasks):
    """Run bias tests on a model."""
    try:
        # Start bias test in background
        background_tasks.add_task(
            run_bias_test_background, 
            request.model,
            request.temperature,
            request.top_p
        )
        
        return {
            "status": "success",
            "message": f"Bias test for {request.model} started in background",
            "model": request.model
        }
    except Exception as e:
        logger.error(f"Error starting bias test: {e}")
        raise HTTPException(status_code=500, detail=f"Error starting bias test: {str(e)}")

async def run_bias_test_background(model: str, temperature: float = 0.7, top_p: float = 0.9):
    """Run bias test in background."""
    try:
        logger.info(f"Running bias test for {model} in background")
        results = test_bias(model, temperature=temperature, top_p=top_p)
        filename = save_test_results(results)
        logger.info(f"Bias test for {model} completed, results saved to {filename}")
    except Exception as e:
        logger.error(f"Error in background bias test for {model}: {e}")

@app.get("/test-results/")
async def get_all_test_results():
    """Get all test results."""
    try:
        combined_log_file = "logs/model_tests.json"
        
        if not os.path.exists(combined_log_file):
            return {"results": []}
        
        with open(combined_log_file, "r") as f:
            try:
                results = json.load(f)
                if not isinstance(results, list):
                    results = [results]
            except json.JSONDecodeError:
                results = []
        
        return {"results": results}
    except Exception as e:
        logger.error(f"Error getting test results: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting test results: {str(e)}")

@app.get("/test-results/{model}")
async def get_model_test_results(model: str):
    """Get test results for a specific model."""
    try:
        combined_log_file = "logs/model_tests.json"
        
        if not os.path.exists(combined_log_file):
            return {"results": []}
        
        with open(combined_log_file, "r") as f:
            try:
                all_results = json.load(f)
                if not isinstance(all_results, list):
                    all_results = [all_results]
            except json.JSONDecodeError:
                all_results = []
        
        # Filter results for the specified model
        model_results = [r for r in all_results if r.get("model") == model]
        
        return {"model": model, "results": model_results}
    except Exception as e:
        logger.error(f"Error getting model test results: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting model test results: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 