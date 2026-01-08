# Exercise 4 Solution: Work with Volumes and Data Persistence

## Solution

### Step 1: Create a named volume

```bash
docker volume create my-data
```

Verify creation:
```bash
docker volume ls
```

**Expected output**:
```
DRIVER    VOLUME NAME
local     my-data
```

### Step 2: Run container and write data to volume

```bash
docker run -it --name writer -v my-data:/data alpine sh
```

Inside the container:
```bash
# Create a file with data
echo "Hello from Docker volume!" > /data/message.txt
echo "Persistent data test" > /data/test.txt

# Verify files were created
ls -la /data/
cat /data/message.txt

# Exit the container
exit
```

### Step 3: Stop and remove the container

```bash
docker stop writer
docker rm writer
```

Verify container is removed:
```bash
docker ps -a | grep writer
# Should return nothing
```

### Step 4: Run new container with same volume

```bash
docker run -it --name reader -v my-data:/data alpine sh
```

Inside the container:
```bash
# Check if data persists
ls -la /data/
cat /data/message.txt
cat /data/test.txt

# The files should still be there!
exit
```

### Step 5: Inspect the volume

```bash
docker volume inspect my-data
```

**Expected output**:
```json
[
    {
        "CreatedAt": "2024-01-08T10:00:00Z",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/my-data/_data",
        "Name": "my-data",
        "Options": {},
        "Scope": "local"
    }
]
```

### Step 6: View volume contents (advanced)

On Linux:
```bash
sudo ls -la $(docker volume inspect my-data --format '{{ .Mountpoint }}')
```

On macOS/Windows:
```bash
# Access through a container
docker run --rm -v my-data:/data alpine ls -la /data
docker run --rm -v my-data:/data alpine cat /data/message.txt
```

### Step 7: Clean up

```bash
# Remove container
docker rm -f reader

# Remove volume
docker volume rm my-data
```

## Volume Types

### 1. Named Volumes (Recommended)

```bash
docker volume create my-volume
docker run -v my-volume:/app/data myapp
```

### 2. Anonymous Volumes

```bash
docker run -v /app/data myapp
```

### 3. Bind Mounts

```bash
docker run -v $(pwd)/data:/app/data myapp
```

## Practical Example: Database with Persistent Storage

### MySQL with named volume

```bash
# Create volume
docker volume create mysql-data

# Run MySQL
docker run -d \
  --name mysql-db \
  -e MYSQL_ROOT_PASSWORD=secret \
  -v mysql-data:/var/lib/mysql \
  mysql:8.0

# Connect and create database
docker exec -it mysql-db mysql -p

# In MySQL prompt:
CREATE DATABASE testdb;
USE testdb;
CREATE TABLE users (id INT, name VARCHAR(50));
INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob');
SELECT * FROM users;
exit;

# Stop and remove container
docker stop mysql-db
docker rm mysql-db

# Data still exists in volume
docker volume inspect mysql-data

# Start new MySQL container with same volume
docker run -d \
  --name mysql-db-new \
  -e MYSQL_ROOT_PASSWORD=secret \
  -v mysql-data:/var/lib/mysql \
  mysql:8.0

# Wait for MySQL to start, then verify data persists
sleep 10
docker exec -it mysql-db-new mysql -psecret -e "SELECT * FROM testdb.users;"

# Expected output:
# +------+-------+
# | id   | name  |
# +------+-------+
# |    1 | Alice |
# |    2 | Bob   |
# +------+-------+
```

## Bind Mount Example

### Development with live reloading

```bash
# Create a simple app
mkdir my-app
cd my-app
echo "console.log('Hello v1');" > app.js

# Run with bind mount
docker run -it --rm \
  -v $(pwd):/app \
  -w /app \
  node:16-alpine \
  node app.js

# Output: Hello v1

# Modify the file on host
echo "console.log('Hello v2');" > app.js

# Run again
docker run -it --rm \
  -v $(pwd):/app \
  -w /app \
  node:16-alpine \
  node app.js

# Output: Hello v2 (changes reflected immediately)
```

## Volume Management Commands

### List all volumes

```bash
docker volume ls
```

### Create volume with specific driver

```bash
docker volume create --driver local \
  --opt type=none \
  --opt device=/path/on/host \
  --opt o=bind \
  my-volume
```

### Remove unused volumes

```bash
docker volume prune
```

### Remove specific volume

```bash
docker volume rm volume-name
```

### Copy data from volume

```bash
# Create temporary container to access volume
docker run --rm -v my-volume:/source -v $(pwd):/backup alpine \
  tar czf /backup/backup.tar.gz -C /source .
```

### Restore data to volume

```bash
# Extract backup to volume
docker run --rm -v my-volume:/target -v $(pwd):/backup alpine \
  tar xzf /backup/backup.tar.gz -C /target
```

## Volume vs Bind Mount Comparison

| Feature | Named Volume | Bind Mount |
|---------|-------------|------------|
| **Managed by** | Docker | User |
| **Location** | Docker area | Anywhere |
| **Portability** | High | Low |
| **Performance** | Optimized | Variable |
| **Use case** | Production | Development |
| **Backup** | Docker commands | Standard tools |

## Best Practices

### 1. Use named volumes for production

```bash
docker volume create prod-data
docker run -v prod-data:/app/data myapp
```

### 2. Use bind mounts for development

```bash
docker run -v $(pwd):/app myapp
```

### 3. Never store data in containers

❌ Bad:
```bash
docker run myapp  # Data lost when container stops
```

✅ Good:
```bash
docker run -v app-data:/app/data myapp
```

### 4. Back up volumes regularly

```bash
docker run --rm -v my-volume:/data -v $(pwd):/backup alpine \
  tar czf /backup/volume-backup-$(date +%Y%m%d).tar.gz -C /data .
```

### 5. Use read-only volumes when appropriate

```bash
docker run -v my-volume:/data:ro myapp
```

## Troubleshooting

### Issue: Permission denied in volume

**Solution**: Adjust permissions or run as specific user

```bash
docker run -u $(id -u):$(id -g) -v my-volume:/data myapp
```

### Issue: Volume not found

**Solution**: Create volume first

```bash
docker volume create my-volume
```

### Issue: Data not persisting

**Solution**: Ensure volume is mounted correctly

```bash
# Check volume mount
docker inspect container-name | grep -A 10 Mounts
```

### Issue: Volume is full

**Solution**: Clean up or increase disk space

```bash
# Check volume size
docker system df -v

# Remove unused volumes
docker volume prune
```

## Advanced: Volume Plugins

Docker supports volume plugins for advanced storage:

- NFS volumes
- Cloud storage (AWS EBS, Azure Disk)
- Distributed storage (GlusterFS, Ceph)

Example with NFS:
```bash
docker volume create --driver local \
  --opt type=nfs \
  --opt o=addr=192.168.1.1,rw \
  --opt device=:/path/to/dir \
  nfs-volume
```

## Key Takeaways

- Named volumes are Docker-managed and persist data
- Bind mounts link host directories to containers
- Volumes survive container deletion
- Always use volumes for database containers
- Back up important volumes regularly
- Use read-only mounts for security when possible
