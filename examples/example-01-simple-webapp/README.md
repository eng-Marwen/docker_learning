# Example 01: Simple Web Application

This example demonstrates how to create a simple Flask web application and containerize it with Docker.

## Files

- `app.py`: A simple Flask web application
- `requirements.txt`: Python dependencies
- `Dockerfile`: Instructions to build the Docker image

## How to Build and Run

### Build the Docker image

```bash
docker build -t simple-webapp .
```

### Run the container

```bash
docker run -p 5000:5000 simple-webapp
```

### Access the application

Open your browser and navigate to: `http://localhost:5000`

### Alternative: Run in detached mode

```bash
docker run -d -p 5000:5000 --name my-webapp simple-webapp
```

### View logs

```bash
docker logs my-webapp
```

### Stop the container

```bash
docker stop my-webapp
```

### Remove the container

```bash
docker rm my-webapp
```

## What You'll Learn

- How to write a basic Dockerfile
- How to build a Docker image
- How to run a container with port mapping
- How to view container logs
- How to manage container lifecycle

## Dockerfile Breakdown

- `FROM python:3.9-slim`: Uses a lightweight Python base image
- `WORKDIR /app`: Sets the working directory
- `COPY requirements.txt .`: Copies dependencies file first (for caching)
- `RUN pip install`: Installs Python packages
- `COPY app.py .`: Copies application code
- `EXPOSE 5000`: Documents that the container listens on port 5000
- `CMD ["python", "app.py"]`: Defines the default command to run
