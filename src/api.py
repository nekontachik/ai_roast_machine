"""FastAPI implementation of the AI Roast Machine."""
from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from typing import Dict, Any, Optional, List
import json
import os
import datetime
import random

# Import our testers
from src.mock_tester import MockTester
try:
    from src.huggingface_tester import HuggingFaceTester
    HUGGINGFACE_AVAILABLE = True
except ImportError:
    HUGGINGFACE_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Check if we should use real models
USE_REAL_MODELS = os.environ.get("USE_REAL_MODELS", "false").lower() == "true"
MODEL_DEVICE = os.environ.get("MODEL_DEVICE", "cpu")

logger.info(f"USE_REAL_MODELS: {USE_REAL_MODELS}")
logger.info(f"MODEL_DEVICE: {MODEL_DEVICE}")
logger.info(f"HUGGINGFACE_AVAILABLE: {HUGGINGFACE_AVAILABLE}")

# Create FastAPI app
app = FastAPI(
    title="AI Roast Machine",
    version="1.0.0",
    description="API for testing and roasting AI models"
)

class TestRequest(BaseModel):
    """Request model for testing an AI model."""
    model_name: str
    model_type: str = "text-generation"
    dataset_name: Optional[str] = None
    prompts: Optional[List[str]] = None
    max_samples: Optional[int] = 5

class RoastRequest(BaseModel):
    """Request model for roasting test results."""
    test_results: Dict[str, Any]

class ModelResult(BaseModel):
    """Model for test results."""
    model_name: str
    overall_score: float
    metrics: Dict[str, float]
    timestamp: str = datetime.datetime.now().isoformat()

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.datetime.now().isoformat(),
        "use_real_models": USE_REAL_MODELS,
        "huggingface_available": HUGGINGFACE_AVAILABLE
    }

@app.post("/test")
async def test_model(request: TestRequest, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """Test an AI model.
    
    Args:
        request: Test request containing model details
        
    Returns:
        Test results
    """
    try:
        # Determine which tester to use
        if USE_REAL_MODELS and HUGGINGFACE_AVAILABLE and not request.model_name.startswith("mock-"):
            logger.info(f"Using HuggingFaceTester for model {request.model_name}")
            tester = HuggingFaceTester(request.model_name, device=MODEL_DEVICE)
        else:
            logger.info(f"Using MockTester for model {request.model_name}")
            tester = MockTester(request.model_name)
        
        # Test with dataset if provided
        if request.dataset_name:
            tester.test_with_dataset(
                dataset_name=request.dataset_name,
                max_samples=request.max_samples or 5
            )
        # Test with provided prompts
        elif request.prompts:
            tester.test_generation(prompts=request.prompts)
        # Use default prompts
        else:
            default_prompts = [
                "Hello, how are you?",
                "What is artificial intelligence?",
                "Write a short poem about technology.",
                "Explain quantum computing to a 5-year-old.",
                "What will the future look like in 100 years?"
            ]
            tester.test_generation(prompts=default_prompts)
        
        # Calculate metrics
        results = tester.calculate_metrics()
        
        # Save results
        os.makedirs("test_results", exist_ok=True)
        with open(f"test_results/{request.model_name}_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        return results
    except Exception as e:
        logger.error(f"Error testing model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/roast")
async def generate_roast(request: RoastRequest) -> Dict[str, Any]:
    """Generate a roast based on test results.
    
    Args:
        request: Roast request containing test results
        
    Returns:
        Generated roast
    """
    try:
        model_name = request.test_results.get("model_name", "Unknown model")
        score = request.test_results.get("overall_score", 0.5)
        
        # Get metrics if available
        metrics = request.test_results.get("metrics", {})
        speed = metrics.get("speed", 0.5)
        diversity = metrics.get("diversity", 0.5)
        
        # Generate roast based on score and metrics
        roasts = []
        
        # Overall score roasts
        if score < 0.3:
            roasts.append(f"{model_name} is so bad, it couldn't even pass a Turing test with a goldfish.")
            roasts.append(f"I've seen pocket calculators with more intelligence than {model_name}.")
            roasts.append(f"{model_name} makes random word generators look like Shakespeare.")
        elif score < 0.7:
            roasts.append(f"{model_name} is like a student who studied just enough to pass, but not enough to impress.")
            roasts.append(f"{model_name} is the AI equivalent of a participation trophy.")
            roasts.append(f"Using {model_name} is like bringing a knife to a gunfight - technically a weapon, but...")
        else:
            roasts.append(f"{model_name} is pretty good, but still makes mistakes a human toddler wouldn't make.")
            roasts.append(f"Not bad for {model_name}, but I wouldn't trust it with my tax returns.")
            roasts.append(f"{model_name} is impressive, until you realize it's just sophisticated autocomplete.")
        
        # Speed-specific roasts
        if speed < 0.3:
            roasts.append(f"{model_name} is so slow, I started growing a beard while waiting for responses.")
        elif speed > 0.8:
            roasts.append(f"{model_name} is fast, I'll give it that. Too bad speed isn't everything.")
        
        # Diversity-specific roasts
        if diversity < 0.3:
            roasts.append(f"{model_name} has the vocabulary diversity of a broken record.")
        elif diversity > 0.8:
            roasts.append(f"{model_name} knows lots of words, shame it doesn't know how to use them properly.")
        
        # Select a random roast
        roast = random.choice(roasts)
        
        result = {
            "model_name": model_name,
            "score": score,
            "roast": roast,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Save roast
        os.makedirs("test_results", exist_ok=True)
        with open(f"test_results/{model_name}_roast.json", "w") as f:
            json.dump(result, f, indent=2)
        
        return result
    except Exception as e:
        logger.error(f"Error generating roast: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/meme")
async def generate_meme(request: RoastRequest) -> Dict[str, str]:
    """Generate a meme based on test results.
    
    Args:
        request: Request containing test results
        
    Returns:
        Path to generated meme
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        import textwrap
        
        model_name = request.test_results.get("model_name", "Unknown model")
        score = request.test_results.get("overall_score", 0.5)
        
        # Create memes directory if it doesn't exist
        os.makedirs("memes", exist_ok=True)
        
        # Select template based on score
        if score < 0.3:
            bg_color = (255, 200, 200)  # Light red
            text = f"{model_name} IS SO BAD\nIT MAKES RANDOM GUESSING LOOK SMART"
        elif score < 0.7:
            bg_color = (255, 255, 200)  # Light yellow
            text = f"{model_name}\nMEDIOCRITY AT ITS FINEST"
        else:
            bg_color = (200, 255, 200)  # Light green
            text = f"{model_name} IS PRETTY GOOD\nFOR A GLORIFIED AUTOCOMPLETE"
        
        # Create a simple meme image
        width, height = 800, 600
        image = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(image)
        
        try:
            # Try to load a font, fall back to default if not available
            font = ImageFont.truetype("Arial", 60)
        except IOError:
            font = ImageFont.load_default()
        
        # Wrap text and center it
        wrapped_text = textwrap.fill(text, width=20)
        text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Add text to image
        draw.text(position, wrapped_text, fill=(0, 0, 0), font=font)
        
        # Save the meme
        meme_path = f"memes/{model_name}_meme.png"
        image.save(meme_path)
        
        return {"meme_path": meme_path}
    except Exception as e:
        logger.error(f"Error generating meme: {str(e)}")
        
        # Fallback to text file if image generation fails
        meme_path = f"memes/{model_name}_meme.png"
        with open(meme_path, "w") as f:
            f.write(f"Meme for {model_name}")
        
        return {"meme_path": meme_path} 