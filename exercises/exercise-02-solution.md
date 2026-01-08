# Exercise 2 Solution: Run and Manage Containers

## Solution

### Step 1: Pull the nginx:alpine image

```bash
docker pull nginx:alpine
```

**Expected output**:
```
alpine: Pulling from library/nginx
a0d0a0d46f8b: Pull complete
...
Status: Downloaded newer image for nginx:alpine
docker.io/library/nginx:alpine
```

### Step 2: Run in detached mode with custom name

```bash
docker run -d --name my-nginx -p 8080:80 nginx:alpine
```

**Expected output**:
```
a1b2c3d4e5f6... (container ID)
```

**Flags explained**:
- `-d`: Detached mode (runs in background)
- `--name my-nginx`: Custom container name
- `-p 8080:80`: Maps host port 8080 to container port 80

### Step 3: Verify the container is running

```bash
docker ps
```

**Expected output**:
```
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                  NAMES
a1b2c3d4e5f6   nginx:alpine   "/docker-entrypoint.…"   10 seconds ago  Up 9 seconds   0.0.0.0:8080->80/tcp   my-nginx
```

### Step 4: Test the web server

```bash
curl http://localhost:8080
```

Or open `http://localhost:8080` in your browser.

### Step 5: View container logs

```bash
docker logs my-nginx
```

**Expected output**:
```
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
...
2024/01/08 10:00:00 [notice] 1#1: nginx/1.24.0
2024/01/08 10:00:00 [notice] 1#1: start worker processes
```

### Step 6: Follow logs in real-time

```bash
docker logs -f my-nginx
```

Press `Ctrl+C` to stop following logs.

### Step 7: Inspect container details

```bash
docker inspect my-nginx
```

### Step 8: Execute command in running container

```bash
docker exec -it my-nginx /bin/sh
```

Inside the container:
```bash
# Check nginx version
nginx -v

# List files
ls -la

# Exit
exit
```

### Step 9: Stop the container

```bash
docker stop my-nginx
```

Verify it's stopped:
```bash
docker ps -a
```

**Expected output** shows STATUS as "Exited":
```
CONTAINER ID   IMAGE          STATUS                     NAMES
a1b2c3d4e5f6   nginx:alpine   Exited (0) 5 seconds ago   my-nginx
```

### Step 10: Remove the container

```bash
docker rm my-nginx
```

Verify removal:
```bash
docker ps -a
# Should not show my-nginx
```

## Additional Commands

### Start a stopped container

```bash
docker start my-nginx
```

### Restart a running container

```bash
docker restart my-nginx
```

### Stop and remove in one command

```bash
docker rm -f my-nginx
```

### Remove all stopped containers

```bash
docker container prune
```

### View container resource usage

```bash
docker stats my-nginx
```

### Copy files to/from container

```bash
# From host to container
docker cp index.html my-nginx:/usr/share/nginx/html/

# From container to host
docker cp my-nginx:/etc/nginx/nginx.conf ./nginx.conf
```

## Practice Variations

### 1. Run multiple nginx containers

```bash
docker run -d --name nginx1 -p 8081:80 nginx:alpine
docker run -d --name nginx2 -p 8082:80 nginx:alpine
docker run -d --name nginx3 -p 8083:80 nginx:alpine
```

### 2. Run with custom HTML

```bash
echo "<h1>Hello from Docker!</h1>" > index.html
docker run -d --name custom-nginx -p 8080:80 -v $(pwd)/index.html:/usr/share/nginx/html/index.html nginx:alpine
```

### 3. Run with environment variables

```bash
docker run -d --name nginx-env -p 8080:80 -e NGINX_HOST=example.com nginx:alpine
```

### 4. Run with automatic restart

```bash
docker run -d --name nginx-restart --restart unless-stopped -p 8080:80 nginx:alpine
```

## Troubleshooting

### Issue: Port already in use

**Error**: `bind: address already in use`

**Solution**: Use a different port or stop the conflicting container

```bash
# Find what's using the port
lsof -i :8080

# Or use a different port
docker run -d --name my-nginx -p 8081:80 nginx:alpine
```

### Issue: Container name already in use

**Error**: `Conflict. The container name "/my-nginx" is already in use`

**Solution**: Remove the existing container first

```bash
docker rm my-nginx
# Or use force
docker rm -f my-nginx
```

### Issue: Cannot connect to container

**Solution**: Check if container is running and port mapping is correct

```bash
docker ps
docker port my-nginx
```

## Key Takeaways

- `-d` runs containers in the background
- `--name` assigns a friendly name for easier management
- `-p` maps ports from host to container
- `docker logs` shows container output
- `docker exec` runs commands in running containers
- Always clean up stopped containers with `docker rm`
