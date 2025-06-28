# fastapi_app/Dockerfile

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional, for pip compiling)
RUN apt-get update && apt-get install -y build-essential git && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY fastapi_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI app code
COPY fastapi_app/ .

# Expose the port FastAPI will run on
EXPOSE 8000

# Start the FastAPI server with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
