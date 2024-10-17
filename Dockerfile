# Use Python 3.9 slim as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set PYTHONPATH to allow imports from the current directory
ENV PYTHONPATH=/app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app/ ./app/
COPY models/ ./models/
COPY tests/ ./tests/
COPY rfm_clusters.csv .
COPY predictions.db .

# Run the tests to ensure everything works
RUN pytest tests/

# Expose port for FastAPI
EXPOSE 8000

# Command to run FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
