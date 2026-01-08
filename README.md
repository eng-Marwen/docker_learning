# Docker Learning Repository 🐳

Welcome to the Docker Learning Repository! This repository is designed to help you learn Docker and its utilities through practical examples, exercises, and comprehensive documentation.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Docker Basics](#docker-basics)
  - [What is Docker?](#what-is-docker)
  - [Key Concepts](#key-concepts)
- [Essential Docker Commands](#essential-docker-commands)
- [Dockerfile Guide](#dockerfile-guide)
- [Docker Compose](#docker-compose)
- [Practical Examples](#practical-examples)
- [Exercises](#exercises)
- [Best Practices](#best-practices)
- [Additional Resources](#additional-resources)

## Introduction

Docker is a platform that enables developers to package applications into containers—standardized executable components combining application source code with the operating system (OS) libraries and dependencies required to run that code in any environment.

## Prerequisites

Before starting with Docker, you should have:

- Basic understanding of command line/terminal usage
- Familiarity with basic programming concepts
- A computer with administrator/root access
- At least 4GB of RAM (8GB recommended)

## Installation

### Linux

```bash
# Update package index
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER

# Verify installation
docker --version
```

### macOS

1. Download Docker Desktop from [Docker Hub](https://hub.docker.com/editions/community/docker-ce-desktop-mac)
2. Install the .dmg file
3. Start Docker Desktop
4. Verify: `docker --version`

### Windows

1. Download Docker Desktop from [Docker Hub](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
2. Run the installer
3. Enable WSL 2 if prompted
4. Start Docker Desktop
5. Verify: `docker --version`

## Docker Basics

### What is Docker?

Docker is a containerization platform that packages your application and all its dependencies together in the form of containers to ensure that your application works seamlessly in any environment.

### Key Concepts

- **Image**: A read-only template with instructions for creating a Docker container. Images are built from Dockerfiles.
- **Container**: A runnable instance of an image. You can create, start, stop, move, or delete a container.
- **Dockerfile**: A text file that contains instructions for building a Docker image.
- **Docker Hub**: A registry service for sharing Docker images.
- **Volume**: Persistent data storage for containers.
- **Network**: Communication channel between containers.

## Essential Docker Commands

### Image Commands

```bash
# Pull an image from Docker Hub
docker pull <image_name>:<tag>

# List all images
docker images

# Build an image from Dockerfile
docker build -t <image_name>:<tag> .

# Remove an image
docker rmi <image_id>

# Tag an image
docker tag <image_id> <repository>:<tag>
```

### Container Commands

```bash
# Run a container
docker run <image_name>

# Run container in background (detached mode)
docker run -d <image_name>

# Run container with name
docker run --name <container_name> <image_name>

# Run container with port mapping
docker run -p <host_port>:<container_port> <image_name>

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop a container
docker stop <container_id>

# Start a stopped container
docker start <container_id>

# Remove a container
docker rm <container_id>

# View container logs
docker logs <container_id>

# Execute command in running container
docker exec -it <container_id> <command>

# Access container shell
docker exec -it <container_id> /bin/bash
```

### System Commands

```bash
# View Docker system information
docker info

# View Docker version
docker version

# Remove unused data
docker system prune

# View resource usage
docker stats
```

## Dockerfile Guide

A Dockerfile is a text document that contains all the commands to assemble an image. Here's a breakdown of common instructions:

```dockerfile
# Base image
FROM ubuntu:20.04

# Maintainer information
LABEL maintainer="your-email@example.com"

# Set working directory
WORKDIR /app

# Copy files from host to container
COPY . /app

# Run commands during build
RUN apt-get update && apt-get install -y python3

# Set environment variables
ENV APP_ENV=production

# Expose port
EXPOSE 8080

# Define volume mount point
VOLUME /data

# Default command to run
CMD ["python3", "app.py"]
```

### Dockerfile Instructions

- `FROM`: Specifies the base image
- `LABEL`: Adds metadata to the image
- `RUN`: Executes commands during build
- `CMD`: Provides default command for container
- `ENTRYPOINT`: Configures container to run as executable
- `COPY`: Copies files from host to image
- `ADD`: Similar to COPY but with additional features
- `WORKDIR`: Sets working directory
- `ENV`: Sets environment variables
- `EXPOSE`: Documents port exposure
- `VOLUME`: Creates mount point for volumes

## Docker Compose

Docker Compose is a tool for defining and running multi-container Docker applications. You use a YAML file to configure your application's services.

### Basic docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

### Docker Compose Commands

```bash
# Start services
docker-compose up

# Start services in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# List services
docker-compose ps

# Execute command in service
docker-compose exec <service_name> <command>
```

## Practical Examples

Check the `/examples` directory for hands-on examples:

- **example-01-simple-webapp**: Basic web application with Dockerfile
- **example-02-multi-container**: Multi-container application with Docker Compose
- **example-03-python-app**: Python application with dependencies

## Exercises

Practice your Docker skills with exercises in the `/exercises` directory:

1. **Exercise 1**: Build your first Docker image
2. **Exercise 2**: Run and manage containers
3. **Exercise 3**: Create a multi-container application
4. **Exercise 4**: Work with volumes and data persistence
5. **Exercise 5**: Implement Docker networking

## Best Practices

### 1. Use Official Base Images
```dockerfile
FROM node:16-alpine
```

### 2. Minimize Layer Count
```dockerfile
# Good: Single RUN instruction
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*
```

### 3. Use .dockerignore
Create a `.dockerignore` file to exclude unnecessary files:
```
node_modules
npm-debug.log
.git
.env
```

### 4. Don't Run as Root
```dockerfile
RUN useradd -m appuser
USER appuser
```

### 5. Use Multi-stage Builds
```dockerfile
# Build stage
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
```

### 6. Leverage Build Cache
Place frequently changing instructions at the end of Dockerfile.

### 7. Use Specific Tags
```dockerfile
# Good
FROM node:16.14.0-alpine

# Avoid
FROM node:latest
```

### 8. Keep Images Small
- Use alpine variants
- Remove unnecessary files
- Combine commands
- Use multi-stage builds

## Additional Resources

### Official Documentation
- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

### Tutorials and Courses
- [Docker Getting Started](https://docs.docker.com/get-started/)
- [Play with Docker](https://labs.play-with-docker.com/)
- [Docker Curriculum](https://docker-curriculum.com/)

### Community
- [Docker Community Forums](https://forums.docker.com/)
- [Docker Slack](https://dockercommunity.slack.com/)
- [Stack Overflow - Docker Tag](https://stackoverflow.com/questions/tagged/docker)

### Books
- "Docker Deep Dive" by Nigel Poulton
- "Docker in Action" by Jeff Nickoloff
- "The Docker Book" by James Turnbull

## Contributing

Contributions are welcome! If you have improvements or additional examples, please feel free to submit a pull request.

## License

This repository is for educational purposes. Feel free to use and modify as needed for your learning journey.

---

**Happy Dockering! 🐳**