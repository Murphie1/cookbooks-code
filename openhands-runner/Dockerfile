# Dockerfile for openhands-runner
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git curl jq redis-tools build-essential procps \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama (headless)
RUN curl -fsSL https://ollama.com/install.sh | bash

# Add Ollama env (required for use inside Docker)
ENV OLLAMA_ORIGINS="*"

# Install Python dependencies
RUN pip install --no-cache-dir openhands-ai openhands-aci mistralai

# Set working directory for Git operations
WORKDIR /workspace

# Copy entrypoint
COPY entrypoint.py /app/entrypoint.py

# Set default envs (can be overridden via docker run -e ...)
ENV LLM_PROVIDER=ollama
ENV LLM_BASE_URL=http://host.docker.internal:11434

# Define default command
ENTRYPOINT ["python", "/app/entrypoint.py"]
