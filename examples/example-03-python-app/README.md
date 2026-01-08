# Example 03: Python Application with Best Practices

This example demonstrates Docker best practices for building production-ready images.

## Features

- **Multi-stage builds**: Reduces final image size
- **Non-root user**: Enhanced security
- **Health checks**: Built-in container health monitoring
- **Minimal base image**: Uses slim Python variant
- **.dockerignore**: Excludes unnecessary files

## Files

- `Dockerfile`: Multi-stage build with security best practices
- `app.py`: Simple Python HTTP server
- `requirements.txt`: Dependencies (empty in this example)
- `.dockerignore`: Files to exclude from build context

## How to Build and Run

### Build the image

```bash
docker build -t python-best-practices .
```

### Run the container

```bash
docker run -p 8000:8000 python-best-practices
```

### Access the application

- Main page: `http://localhost:8000`
- Health check: `http://localhost:8000/health`
- Container info: `http://localhost:8000/info`

### Check image size

```bash
docker images python-best-practices
```

### Verify health status

```bash
docker ps
# Look for the health status in the STATUS column
```

### View health check logs

```bash
docker inspect --format='{{json .State.Health}}' <container_id> | python -m json.tool
```

## Best Practices Explained

### 1. Multi-stage Builds

The Dockerfile uses two stages:
- **Builder stage**: Installs dependencies
- **Production stage**: Contains only runtime requirements

This significantly reduces the final image size.

### 2. Non-root User

Running as a non-root user (`appuser`) improves security by limiting potential damage if the container is compromised.

```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### 3. Health Checks

The `HEALTHCHECK` instruction allows Docker to test if the container is working properly:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
```

### 4. Minimal Base Image

Using `python:3.9-slim` instead of the full Python image reduces size by hundreds of megabytes.

### 5. Layer Optimization

Dependencies are copied and installed before the application code, leveraging Docker's layer caching.

### 6. .dockerignore

Similar to .gitignore, excludes unnecessary files from the build context:

```
__pycache__/
*.pyc
venv/
.git/
```

## Security Benefits

- No root access inside container
- Minimal attack surface with slim image
- Health monitoring for reliability
- Separate build and runtime environments

## Image Size Comparison

Compare different approaches:

```bash
# This example (multi-stage + slim)
docker images python-best-practices

# Full Python image (for comparison)
docker pull python:3.9
docker images python:3.9

# Alpine variant (even smaller)
docker pull python:3.9-alpine
docker images python:3.9-alpine
```

## Advanced Usage

### Override default command

```bash
docker run -p 8000:8000 python-best-practices python -c "print('Custom command')"
```

### Mount volume for development

```bash
docker run -p 8000:8000 -v $(pwd):/app python-best-practices
```

### Check user inside container

```bash
docker run python-best-practices whoami
# Output: appuser
```

### Inspect health status

```bash
docker run -d --name health-test python-best-practices
sleep 10
docker inspect health-test | grep -A 10 "Health"
```
