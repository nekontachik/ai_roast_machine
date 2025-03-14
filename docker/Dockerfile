# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set up Hugging Face cache directory
ENV HF_HOME=/app/.cache/huggingface
RUN mkdir -p $HF_HOME

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs test_results memes notebooks datasets

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/app/.cache/huggingface/transformers
ENV DATASETS_CACHE=/app/.cache/huggingface/datasets
ENV HF_DATASETS_CACHE=/app/.cache/huggingface/datasets

# Expose ports for FastAPI and Jupyter
EXPOSE 8000 8888

# Default command (can be overridden in docker-compose)
CMD ["python", "-u", "run_api.py"]
