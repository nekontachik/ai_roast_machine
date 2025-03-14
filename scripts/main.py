"""AI Roast Machine - A tool for testing and humorously evaluating AI models."""
from flask import Flask, jsonify, request, render_template_string
import os
import logging
import json
from typing import Dict, Any

# Import our modules
from src.config import config
from src.utils_helpers import setup_logging, save_json, generate_output_filename
from src.test_runner import run_model_tests
from src.roast_generator import generate_model_roast
from src.meme_generator import generate_model_meme

# Configure logging
setup_logging(config.LOG_FILE, config.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)


@app.route("/health")
def health_check():
    """Health check endpoint for Docker healthcheck."""
    return jsonify({"status": "healthy"})


@app.route("/")
def home():
    """Home endpoint."""
    logger.info("Home endpoint accessed")
    return jsonify(
        {
            "message": "✅ AI Roast Machine is running successfully!",
            "status": "online",
            "version": config.APP_VERSION,
        }
    )


@app.route("/test", methods=["POST"])
def test_model():
    """Test an AI model and return the results."""
    data = request.json or {}
    model_name = data.get("model_name", config.DEFAULT_MODEL)
    model_type = data.get("model_type", "text-generation")
    
    logger.info(f"Testing model: {model_name}")
    
    # Generate output paths
    timestamp = generate_output_filename("", "")
    test_output = f"{config.TEST_OUTPUT_DIR}/test_{timestamp}.json"
    roast_output = f"{config.TEST_OUTPUT_DIR}/roast_{timestamp}.json"
    meme_output = f"{config.MEME_OUTPUT_DIR}/meme_{timestamp}.png"
    
    # Run tests
    test_results = run_model_tests(model_name, model_type, test_output)
    
    # Generate roast
    roast_results = generate_model_roast(test_results)
    save_json(roast_results, roast_output)
    
    # Generate meme
    meme_path = generate_model_meme(test_results, meme_output)
    
    # Return results
    return jsonify({
        "model_name": model_name,
        "test_results": test_results,
        "roast": roast_results,
        "meme_path": meme_path,
    })


@app.route("/roast", methods=["POST"])
def roast_model():
    """Generate a roast for an AI model based on test results."""
    data = request.json or {}
    
    # Check if test results are provided
    if "test_results" in data:
        test_results = data["test_results"]
    else:
        # If not, run tests first
        model_name = data.get("model_name", config.DEFAULT_MODEL)
        model_type = data.get("model_type", "text-generation")
        test_results = run_model_tests(model_name, model_type)
    
    # Generate roast
    roast_results = generate_model_roast(test_results)
    
    return jsonify({
        "model_name": test_results.get("model_name", "Unknown Model"),
        "roast": roast_results,
    })


@app.route("/meme", methods=["POST"])
def generate_meme():
    """Generate a meme for an AI model based on test results."""
    data = request.json or {}
    
    # Check if test results are provided
    if "test_results" in data:
        test_results = data["test_results"]
    else:
        # If not, run tests first
        model_name = data.get("model_name", config.DEFAULT_MODEL)
        model_type = data.get("model_type", "text-generation")
        test_results = run_model_tests(model_name, model_type)
    
    # Generate meme
    output_path = f"{config.MEME_OUTPUT_DIR}/meme_{generate_output_filename('', '')}.png"
    meme_path = generate_model_meme(test_results, output_path)
    
    return jsonify({
        "model_name": test_results.get("model_name", "Unknown Model"),
        "meme_path": meme_path,
    })


if __name__ == "__main__":
    # Create necessary directories
    os.makedirs(config.TEST_OUTPUT_DIR, exist_ok=True)
    os.makedirs(config.MEME_OUTPUT_DIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    logger.info(f"Starting {config.APP_NAME} v{config.APP_VERSION}")
    print(f"✅ {config.APP_NAME} is running successfully!")

    # Run the Flask app
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
