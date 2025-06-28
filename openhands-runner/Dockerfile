# Dockerfile for openhands-runner
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git curl jq redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | bash

# Install OpenHands and required Python packages
RUN pip install openhands mistral-client

# Copy the runner script
COPY entrypoint.py /app/entrypoint.py
WORKDIR /workspace

ENTRYPOINT ["python", "/app/entrypoint.py"]
