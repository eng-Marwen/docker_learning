# Use official Python runtime as base image
FROM python:3.9-slim

# Set metadata
LABEL maintainer="docker-learning@example.com"
LABEL description="Simple Flask web application for Docker learning"

# Set working directory in container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port 5000
EXPOSE 5000

# Set environment variable
ENV FLASK_APP=app.py

# Run the application
CMD ["python", "app.py"]
