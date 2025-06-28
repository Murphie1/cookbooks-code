# Dockerfile for openhands-runner
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git curl jq redis-tools build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama (headless)
RUN curl -fsSL https://ollama.com/install.sh | bash

# Install Python dependencies
RUN pip install --no-cache-dir openhands-aci mistralai

# Copy the runner script
COPY entrypoint.py /app/entrypoint.py

# Set working directory
WORKDIR /workspace

# Define default command
ENTRYPOINT ["python", "/app/entrypoint.py"]
