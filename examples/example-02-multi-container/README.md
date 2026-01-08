# Example 02: Multi-Container Application

This example demonstrates how to use Docker Compose to orchestrate multiple containers that work together.

## Architecture

- **Web Service**: Flask application that tracks visits
- **Redis Service**: In-memory data store for visit counting

## Files

- `docker-compose.yml`: Defines multiple services and their configuration
- `app.py`: Flask application that connects to Redis
- `requirements.txt`: Python dependencies
- `Dockerfile`: Build instructions for the web service

## How to Run

### Start all services

```bash
docker-compose up
```

Or run in detached mode:

```bash
docker-compose up -d
```

### View logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs web
docker-compose logs redis
```

### Check running services

```bash
docker-compose ps
```

### Access the application

Open your browser and navigate to:
- Main page: `http://localhost:8080`
- Visit counter: `http://localhost:8080/visits`
- Health check: `http://localhost:8080/health`

### Stop all services

```bash
docker-compose down
```

### Stop and remove volumes

```bash
docker-compose down -v
```

## What You'll Learn

- How to define multiple services in docker-compose.yml
- How to configure service dependencies with `depends_on`
- How to use environment variables for configuration
- How to create and use Docker volumes for data persistence
- How to configure Docker networks for service communication
- How to expose ports and map them to host ports

## Docker Compose Features

### Service Configuration
- `build`: Build image from Dockerfile
- `image`: Use existing image
- `ports`: Port mapping
- `environment`: Environment variables
- `depends_on`: Service dependencies
- `restart`: Restart policy

### Volumes
Volumes provide persistent storage that survives container restarts. In this example, Redis data is stored in a named volume.

### Networks
Networks allow containers to communicate with each other. Services in the same network can reach each other by service name.

## Useful Commands

```bash
# Rebuild services
docker-compose build

# Rebuild and start
docker-compose up --build

# Scale a service
docker-compose up --scale web=3

# Execute command in service
docker-compose exec web /bin/bash

# View resource usage
docker-compose stats
```

## Troubleshooting

If you encounter connection issues:

1. Check that all services are running: `docker-compose ps`
2. Check logs: `docker-compose logs`
3. Verify network connectivity: `docker-compose exec web ping redis`
4. Restart services: `docker-compose restart`
