# Exercise 5 Solution: Docker Networking

## Solution

### Step 1: Create a custom bridge network

```bash
docker network create my-network
```

Verify creation:
```bash
docker network ls
```

**Expected output**:
```
NETWORK ID     NAME         DRIVER    SCOPE
abc123def456   bridge       bridge    local
def456ghi789   host         host      local
ghi789jkl012   none         null      local
jkl012mno345   my-network   bridge    local
```

### Step 2: Run two containers on the same network

```bash
# Run first container (web server)
docker run -d --name web --network my-network nginx:alpine

# Run second container (client)
docker run -d --name client --network my-network alpine sleep 3600
```

### Step 3: Verify containers can communicate using container names

```bash
# Access client container
docker exec -it client sh

# Inside the client container, ping the web container by name
ping -c 3 web

# Expected output: successful ping to web container
# PING web (172.18.0.2): 56 data bytes
# 64 bytes from 172.18.0.2: seq=0 ttl=64 time=0.123 ms
# ...

# Install curl and test HTTP connection
apk add --no-cache curl
curl http://web

# Expected output: nginx default page HTML

exit
```

### Step 4: Test network isolation

```bash
# Create another network
docker network create isolated-network

# Run container on isolated network
docker run -d --name isolated --network isolated-network alpine sleep 3600

# Try to ping from client to isolated (should fail)
docker exec -it client ping -c 3 isolated
# Expected: ping: bad address 'isolated'

# Try to ping from isolated to web (should fail)
docker exec -it isolated ping -c 3 web
# Expected: ping: bad address 'web'
```

### Step 5: Connect container to multiple networks

```bash
# Connect isolated container to my-network
docker network connect my-network isolated

# Now isolated can reach both networks
docker exec -it isolated ping -c 3 web
# Expected: successful ping
```

### Step 6: Inspect network configuration

```bash
# Inspect the network
docker network inspect my-network
```

**Expected output** (partial):
```json
[
    {
        "Name": "my-network",
        "Driver": "bridge",
        "Containers": {
            "abc123": {
                "Name": "web",
                "IPv4Address": "172.18.0.2/16"
            },
            "def456": {
                "Name": "client",
                "IPv4Address": "172.18.0.3/16"
            }
        }
    }
]
```

### Step 7: Inspect container network settings

```bash
docker inspect web --format='{{json .NetworkSettings.Networks}}' | python3 -m json.tool
```

### Step 8: Clean up

```bash
# Stop and remove containers
docker stop web client isolated
docker rm web client isolated

# Remove networks
docker network rm my-network isolated-network
```

## Network Types

### 1. Bridge Network (Default)

```bash
# Containers can communicate with each other
docker run -d --name app1 nginx
docker run -d --name app2 nginx
```

### 2. Host Network

```bash
# Container shares host's network namespace
docker run -d --network host nginx
# Accessible directly on host ports (no -p needed)
```

### 3. None Network

```bash
# Container has no network access
docker run -d --network none alpine sleep 3600
```

### 4. Custom Bridge Network (Recommended)

```bash
docker network create --driver bridge my-bridge
docker run -d --network my-bridge nginx
```

## Practical Example: Multi-tier Application

### Three-tier app with separate networks

```bash
# Create networks
docker network create frontend
docker network create backend

# Database (backend only)
docker run -d \
  --name db \
  --network backend \
  -e POSTGRES_PASSWORD=secret \
  postgres:alpine

# API (both networks)
docker run -d \
  --name api \
  --network backend \
  -e DB_HOST=db \
  nginx:alpine

docker network connect frontend api

# Web (frontend only)
docker run -d \
  --name web \
  --network frontend \
  -p 8080:80 \
  nginx:alpine

# Verify network isolation
# web can reach api
docker exec web ping -c 3 api

# web cannot reach db (as expected)
docker exec web ping -c 3 db
# Expected: ping: bad address 'db'

# api can reach db
docker exec api ping -c 3 db
```

## Docker Compose Network Example

```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    networks:
      - frontend
    ports:
      - "8080:80"

  api:
    image: node:16-alpine
    networks:
      - frontend
      - backend
    command: sleep 3600

  db:
    image: postgres:alpine
    networks:
      - backend
    environment:
      POSTGRES_PASSWORD: secret

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access
```

## Network Management Commands

### Create network with custom subnet

```bash
docker network create \
  --driver bridge \
  --subnet 192.168.100.0/24 \
  --gateway 192.168.100.1 \
  --ip-range 192.168.100.128/25 \
  custom-network
```

### Run container with specific IP

```bash
docker run -d \
  --name web \
  --network custom-network \
  --ip 192.168.100.10 \
  nginx:alpine
```

### List networks

```bash
docker network ls
```

### Inspect network

```bash
docker network inspect bridge
```

### Disconnect container from network

```bash
docker network disconnect my-network container-name
```

### Connect container to network

```bash
docker network connect my-network container-name
```

### Remove unused networks

```bash
docker network prune
```

### Remove specific network

```bash
docker network rm network-name
```

## DNS Resolution

Docker provides automatic DNS resolution in custom networks:

```bash
# Create network
docker network create app-net

# Run services
docker run -d --name service1 --network app-net nginx:alpine
docker run -d --name service2 --network app-net nginx:alpine

# service1 can reach service2 by name
docker exec service1 ping service2

# service2 can reach service1 by name
docker exec service2 ping service1
```

## Port Publishing

### Publish to specific host interface

```bash
# Only localhost
docker run -d -p 127.0.0.1:8080:80 nginx

# Specific IP
docker run -d -p 192.168.1.100:8080:80 nginx

# All interfaces (default)
docker run -d -p 8080:80 nginx
```

### Random host port

```bash
docker run -d -p 80 nginx
# Check assigned port
docker port container-name
```

### Publish multiple ports

```bash
docker run -d -p 8080:80 -p 8443:443 nginx
```

## Network Debugging

### Check connectivity

```bash
# Ping test
docker exec container1 ping container2

# DNS test
docker exec container1 nslookup container2

# Port test
docker exec container1 nc -zv container2 80
```

### Inspect network traffic

```bash
# Install tcpdump in container
docker exec -it container sh
apk add tcpdump
tcpdump -i eth0
```

### Check network interfaces

```bash
docker exec container ip addr show
docker exec container ip route show
```

## Advanced: Overlay Networks (Swarm)

For multi-host networking:

```bash
# Initialize swarm
docker swarm init

# Create overlay network
docker network create --driver overlay my-overlay

# Deploy service on overlay network
docker service create \
  --name web \
  --network my-overlay \
  --replicas 3 \
  nginx:alpine
```

## Best Practices

### 1. Use custom networks for service isolation

```bash
docker network create app-network
docker run --network app-network myapp
```

### 2. Use network aliases

```bash
docker run --network my-net --network-alias db postgres
docker run --network my-net --network-alias api node-app
```

### 3. Implement network segmentation

```bash
# Frontend network
docker network create frontend

# Backend network (internal)
docker network create backend --internal
```

### 4. Use Docker Compose for complex networking

```yaml
networks:
  frontend:
  backend:
    internal: true
```

### 5. Document network architecture

Create a network diagram for your application.

## Troubleshooting

### Issue: Containers can't communicate

**Check:**
1. Are they on the same network?
2. Are the services running?
3. Are the ports exposed?

```bash
docker network inspect network-name
docker ps
docker port container-name
```

### Issue: DNS resolution not working

**Solution:** Use custom bridge network (not default bridge)

```bash
# Default bridge doesn't support DNS
docker network create my-network
docker run --network my-network nginx
```

### Issue: Port conflict

**Solution:** Use different host port

```bash
docker run -p 8081:80 nginx  # Instead of 8080
```

### Issue: Can't access container from host

**Solution:** Check port mapping and firewall

```bash
docker port container-name
# Check if port is listening
netstat -tlnp | grep 8080
```

## Key Takeaways

- Custom bridge networks provide automatic DNS resolution
- Use networks for service isolation and security
- Containers on different networks can't communicate (by default)
- A container can belong to multiple networks
- Host network mode shares host's network stack
- Always use custom networks instead of default bridge
- Network segmentation improves security
