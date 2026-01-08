# Exercise 3 Solution: Create a Multi-Container Application

## Solution

### Step 1: Create project directory

```bash
mkdir wordpress-docker
cd wordpress-docker
```

### Step 2: Create docker-compose.yml

Create a file named `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # Database service
  db:
    image: mysql:8.0
    volumes:
      - db_data:/var/lib/mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wpuser
      MYSQL_PASSWORD: wppassword
    networks:
      - wp-network

  # WordPress service
  wordpress:
    depends_on:
      - db
    image: wordpress:latest
    ports:
      - "8080:80"
    restart: always
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wpuser
      WORDPRESS_DB_PASSWORD: wppassword
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - wp_data:/var/www/html
    networks:
      - wp-network

volumes:
  db_data:
  wp_data:

networks:
  wp-network:
    driver: bridge
```

### Step 3: Start all services

```bash
docker-compose up -d
```

**Expected output**:
```
Creating network "wordpress-docker_wp-network" ... done
Creating volume "wordpress-docker_db_data" ... done
Creating volume "wordpress-docker_wp_data" ... done
Creating wordpress-docker_db_1 ... done
Creating wordpress-docker_wordpress_1 ... done
```

### Step 4: Verify services are running

```bash
docker-compose ps
```

**Expected output**:
```
Name                          Command               State          Ports
----------------------------------------------------------------------------------------
wordpress-docker_db_1         docker-entrypoint.sh mysqld      Up      3306/tcp, 33060/tcp
wordpress-docker_wordpress_1  docker-entrypoint.sh apach ...   Up      0.0.0.0:8080->80/tcp
```

### Step 5: View logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs wordpress
docker-compose logs db
```

### Step 6: Test the application

Open your browser and navigate to `http://localhost:8080`

You should see the WordPress installation page.

### Step 7: Verify connectivity between services

```bash
# Access WordPress container
docker-compose exec wordpress /bin/bash

# Inside the container, test database connection
apt-get update && apt-get install -y default-mysql-client
mysql -h db -u wpuser -pwppassword wordpress

# Exit MySQL
exit

# Exit container
exit
```

### Step 8: Inspect the network

```bash
docker network ls
docker network inspect wordpress-docker_wp-network
```

### Step 9: Inspect volumes

```bash
docker volume ls
docker volume inspect wordpress-docker_db_data
docker volume inspect wordpress-docker_wp_data
```

### Step 10: Stop services

```bash
docker-compose down
```

### Step 11: Stop and remove volumes

```bash
docker-compose down -v
```

## Alternative: PostgreSQL Version

Create `docker-compose-postgres.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: apppassword
    networks:
      - app-network

  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    depends_on:
      - db
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

Run with:
```bash
docker-compose -f docker-compose-postgres.yml up -d
```

## Additional Configurations

### With phpMyAdmin for database management

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    volumes:
      - db_data:/var/lib/mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wpuser
      MYSQL_PASSWORD: wppassword

  wordpress:
    depends_on:
      - db
    image: wordpress:latest
    ports:
      - "8080:80"
    restart: always
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wpuser
      WORDPRESS_DB_PASSWORD: wppassword
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - wp_data:/var/www/html

  phpmyadmin:
    depends_on:
      - db
    image: phpmyadmin:latest
    ports:
      - "8081:80"
    environment:
      PMA_HOST: db
      MYSQL_ROOT_PASSWORD: rootpassword

volumes:
  db_data:
  wp_data:
```

Access phpMyAdmin at `http://localhost:8081`

## Useful Commands

### View service logs in real-time

```bash
docker-compose logs -f
```

### Rebuild services

```bash
docker-compose up -d --build
```

### Scale a service

```bash
docker-compose up -d --scale wordpress=3
```

### Execute commands in services

```bash
docker-compose exec wordpress bash
docker-compose exec db mysql -u root -p
```

### View resource usage

```bash
docker-compose stats
```

### Restart specific service

```bash
docker-compose restart wordpress
```

## Troubleshooting

### Issue: Services fail to start

Check logs:
```bash
docker-compose logs
```

### Issue: Database connection failed

1. Ensure database is ready before WordPress starts
2. Check environment variables match
3. Wait for database initialization (can take 30-60 seconds)

Add healthcheck:
```yaml
db:
  healthcheck:
    test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
    timeout: 20s
    retries: 10
```

### Issue: Port already in use

Change the host port:
```yaml
wordpress:
  ports:
    - "8081:80"  # Changed from 8080
```

### Issue: Data not persisting

Ensure volumes are defined and mounted correctly. Check:
```bash
docker volume ls
docker volume inspect <volume_name>
```

## Key Concepts

- **depends_on**: Ensures services start in correct order
- **volumes**: Named volumes for data persistence
- **networks**: Custom networks for service communication
- **environment**: Configuration through environment variables
- **restart**: Automatic restart policy

## Best Practices

1. **Use named volumes** for data persistence
2. **Define explicit networks** for better isolation
3. **Set restart policies** for reliability
4. **Use environment variables** for configuration
5. **Document service dependencies** with depends_on
6. **Don't commit sensitive data** - use .env files

### Example .env file

Create `.env`:
```
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=wordpress
MYSQL_USER=wpuser
MYSQL_PASSWORD=wppassword
```

Update docker-compose.yml:
```yaml
db:
  environment:
    MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    MYSQL_DATABASE: ${MYSQL_DATABASE}
    MYSQL_USER: ${MYSQL_USER}
    MYSQL_PASSWORD: ${MYSQL_PASSWORD}
```

## Next Steps

- Add more services (Redis cache, Elasticsearch, etc.)
- Implement health checks for all services
- Set up service dependencies with healthchecks
- Configure resource limits
- Add monitoring and logging services
