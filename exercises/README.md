# Docker Learning Exercises

This directory contains hands-on exercises to practice Docker skills.

## Exercise List

### Exercise 1: Build Your First Docker Image
**Difficulty**: Beginner  
**Objective**: Create a simple Dockerfile and build an image

**Tasks**:
1. Create a Dockerfile for a "Hello World" application
2. Build the Docker image
3. Run a container from the image
4. Verify the output

**Starting Point**:
```dockerfile
# Create a Dockerfile that:
# - Uses alpine:latest as base image
# - Runs echo "Hello Docker!" when started
```

**Solution**: Check `exercise-01-solution.md`

---

### Exercise 2: Run and Manage Containers
**Difficulty**: Beginner  
**Objective**: Practice container lifecycle management

**Tasks**:
1. Pull the `nginx:alpine` image
2. Run it in detached mode with a custom name
3. Map port 80 to port 8080 on your host
4. View container logs
5. Stop and remove the container

**Commands to Practice**:
- `docker pull`
- `docker run -d`
- `docker ps`
- `docker logs`
- `docker stop`
- `docker rm`

**Solution**: Check `exercise-02-solution.md`

---

### Exercise 3: Create a Multi-Container Application
**Difficulty**: Intermediate  
**Objective**: Use Docker Compose to orchestrate multiple services

**Tasks**:
1. Create a docker-compose.yml file with:
   - A web application (nginx)
   - A database (MySQL or PostgreSQL)
2. Define environment variables for the database
3. Create a named volume for database persistence
4. Start all services with docker-compose
5. Verify connectivity between services

**Solution**: Check `exercise-03-solution.md`

---

### Exercise 4: Work with Volumes and Data Persistence
**Difficulty**: Intermediate  
**Objective**: Understand Docker volumes for data persistence

**Tasks**:
1. Create a named volume
2. Run a container that writes data to the volume
3. Stop and remove the container
4. Run a new container with the same volume
5. Verify that data persists
6. Inspect the volume

**Commands to Practice**:
- `docker volume create`
- `docker volume ls`
- `docker volume inspect`
- `docker run -v`

**Solution**: Check `exercise-04-solution.md`

---

### Exercise 5: Docker Networking
**Difficulty**: Intermediate  
**Objective**: Create and manage Docker networks

**Tasks**:
1. Create a custom bridge network
2. Run two containers on the same network
3. Verify they can communicate using container names
4. Test network isolation with containers on different networks
5. Inspect network configuration

**Commands to Practice**:
- `docker network create`
- `docker network ls`
- `docker network inspect`
- `docker run --network`

**Solution**: Check `exercise-05-solution.md`

---

### Exercise 6: Multi-stage Builds
**Difficulty**: Advanced  
**Objective**: Optimize image size with multi-stage builds

**Tasks**:
1. Create a Node.js or Python application
2. Write a multi-stage Dockerfile:
   - Build stage: Install dependencies and build
   - Production stage: Copy only runtime artifacts
3. Compare sizes with single-stage build
4. Run the optimized image

**Solution**: Check `exercise-06-solution.md`

---

### Exercise 7: Docker Security Best Practices
**Difficulty**: Advanced  
**Objective**: Implement security best practices

**Tasks**:
1. Create a Dockerfile that:
   - Uses a non-root user
   - Has minimal base image
   - Includes a health check
   - Uses .dockerignore
2. Scan the image for vulnerabilities (optional: docker scan)
3. Run the container with read-only filesystem

**Solution**: Check `exercise-07-solution.md`

---

## How to Use These Exercises

1. Start with Exercise 1 and progress sequentially
2. Try to complete each exercise without looking at the solution
3. If stuck, review the relevant sections in the main README.md
4. Compare your solution with the provided solution
5. Experiment with variations of each exercise

## Additional Challenges

Once you complete all exercises, try these challenges:

- **Challenge 1**: Create a complete microservices application with 3+ services
- **Challenge 2**: Set up a CI/CD pipeline that builds and pushes Docker images
- **Challenge 3**: Deploy a Docker application to a cloud platform
- **Challenge 4**: Implement container monitoring and logging
- **Challenge 5**: Create a Docker-based development environment for your project

## Getting Help

- Review the main [README.md](../README.md) for Docker basics
- Check the [examples](../examples/) directory for reference implementations
- Search [Docker Documentation](https://docs.docker.com/)
- Ask questions on [Stack Overflow](https://stackoverflow.com/questions/tagged/docker)

Happy Learning! 🐳
