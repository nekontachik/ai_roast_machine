from flask import Flask, jsonify
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check endpoint for Docker healthcheck"""
    return jsonify({"status": "healthy"})

@app.route('/')
def home():
    """Home endpoint"""
    logger.info("Home endpoint accessed")
    return jsonify({
        "message": "✅ AI Roast Machine is running successfully!",
        "status": "online"
    })

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    logger.info("Starting AI Roast Machine")
    print("✅ AI Roast Machine is running successfully!")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=8000)