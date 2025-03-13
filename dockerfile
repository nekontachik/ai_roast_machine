FROM python:3.10-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary files
COPY main.py .
COPY src/ ./src/
COPY models/ ./models/

# Create directories that might be needed
RUN mkdir -p logs

EXPOSE 8000

# Run with unbuffered output
CMD ["python", "-u", "main.py"]
