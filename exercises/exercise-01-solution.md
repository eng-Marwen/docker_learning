# Exercise 1 Solution: Build Your First Docker Image

## Solution

### Step 1: Create a Dockerfile

Create a file named `Dockerfile`:

```dockerfile
# Use Alpine Linux as base image
FROM alpine:latest

# Set the default command
CMD ["echo", "Hello Docker!"]
```

### Step 2: Build the Docker image

```bash
docker build -t hello-docker .
```

**Expected output**:
```
[+] Building 2.3s (5/5) FINISHED
=> [internal] load build definition from Dockerfile
=> => transferring dockerfile: 123B
=> [internal] load .dockerignore
=> => transferring context: 2B
=> [1/1] FROM docker.io/library/alpine:latest
=> exporting to image
=> => exporting layers
=> => writing image sha256:abc123...
=> => naming to docker.io/library/hello-docker:latest
```

### Step 3: Run a container from the image

```bash
docker run hello-docker
```

**Expected output**:
```
Hello Docker!
```

### Step 4: Verify the image exists

```bash
docker images hello-docker
```

**Expected output**:
```
REPOSITORY      TAG       IMAGE ID       CREATED          SIZE
hello-docker    latest    abc123def456   10 seconds ago   7.05MB
```

## Alternative Approaches

### Using ENTRYPOINT instead of CMD

```dockerfile
FROM alpine:latest
ENTRYPOINT ["echo"]
CMD ["Hello Docker!"]
```

This allows you to override the message:

```bash
docker run hello-docker "Custom message!"
```

### Adding a LABEL

```dockerfile
FROM alpine:latest
LABEL maintainer="your-email@example.com"
LABEL description="My first Docker image"
CMD ["echo", "Hello Docker!"]
```

### Interactive version

```dockerfile
FROM alpine:latest
CMD ["/bin/sh"]
```

Run interactively:

```bash
docker run -it hello-docker
```

## Key Concepts

- **FROM**: Specifies the base image
- **CMD**: Default command to run when container starts
- **docker build**: Creates an image from a Dockerfile
- **docker run**: Creates and starts a container from an image
- **-t flag**: Tags the image with a name

## Common Issues

### Issue: "docker: command not found"
**Solution**: Make sure Docker is installed and running

### Issue: Permission denied
**Solution**: Add your user to the docker group or use sudo

```bash
sudo usermod -aG docker $USER
# Log out and back in
```

### Issue: Build fails with "Cannot connect to Docker daemon"
**Solution**: Start Docker service

```bash
# Linux
sudo systemctl start docker

# macOS/Windows
# Start Docker Desktop application
```

## Next Steps

- Try modifying the Dockerfile to use different base images (ubuntu, python, node)
- Add multiple CMD instructions and observe which one executes
- Practice with different build tags: `docker build -t hello-docker:v1.0 .`
