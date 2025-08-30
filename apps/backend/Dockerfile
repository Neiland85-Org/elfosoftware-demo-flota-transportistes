# Dockerfile for Backend (FastAPI)
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from root directory and install Python dependencies
COPY ../../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy pyproject.toml and install the package in development mode
COPY pyproject.toml .
COPY src/ ./src/
RUN pip install -e .

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.presentation.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
