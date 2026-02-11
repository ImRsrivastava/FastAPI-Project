1.  Introduction to Docker
2.  Docker Architecture
3.  Installing Docker
4.  Docker Image
5.  Docker Container
6.  Docker Networking
7.  Docker Volumes & Storage
8.  Docker Compose
9.  Docker Registry
10. Multi-stage Docker Builds
11. Monitoring & Logging in Docker
12. Orchestrating Docker with Kubernetes (Introduction)
Projects:
    1.  3 Tier Application with Docker Compose
    2.  Deploying a Web application with Nginx & MySql


==========================================================================================================
DOCKER – COMPLETE NOTES
==========================================================================================================

Docker is a containerization platform that helps developers
package applications along with their dependencies and run
them consistently across different environments.

Without Docker:
- App works on developer machine
- Fails on server due to dependency mismatch

With Docker:
- App + dependencies = Container
- Runs same everywhere

==========================================================================================================
1. WHAT IS A CONTAINER?
==========================================================================================================

A container is a lightweight, isolated environment that runs
an application along with everything it needs:
- OS libraries
- Runtime (Node, PHP, Python, etc.)
- Dependencies
- Configuration

Containers:
- Are fast
- Use fewer resources than virtual machines
- Share the host OS kernel

==========================================================================================================
2. DOCKER ARCHITECTURE (HOW DOCKER WORKS)
==========================================================================================================

Docker works using a client–server architecture.

MAIN COMPONENTS:

1) Docker Engine
----------------
- Core software that makes Docker work
- Installed on your system
- Responsible for running containers

Think of Docker Engine as:
"Engine of a car that actually runs it"

2) Docker Daemon (dockerd)
-------------------------
- Background service
- Runs continuously
- Does the actual work:
  - Pull images
  - Create containers
  - Start/stop containers
  - Manage networks & volumes

Docker Daemon listens for requests from Docker CLI.

3) Docker CLI
-------------
- Command-line interface used by users
- Examples:
  docker run
  docker build
  docker ps
  docker stop

CLI DOES NOT DO THE WORK.
It only sends commands to Docker Daemon.

FLOW:
User → Docker CLI → Docker Daemon → Container

==========================================================================================================
3. INSTALL DOCKER ON LINUX
==========================================================================================================

Step 1: Update package list
    sudo apt update

Why?
- Ensures latest package info is used

Step 2: Install Docker
    sudo apt install docker.io

After installation:
- Docker service starts automatically
- Docker Daemon runs in background

Check Docker:
    docker --version

==========================================================================================================
4. WHY ADD USER TO DOCKER GROUP?
==========================================================================================================

By default:
- Docker commands need sudo
- Example:
    sudo docker ps

This is inconvenient.

Solution:
Add your user to Docker group.

Steps:

Check current user:
    whoami

Add user to docker group:
    sudo usermod -aG docker $USER

Refresh permissions:
    newgrp docker

Now you can run:
    docker ps
without sudo.

==========================================================================================================
5. DOCKER IMAGES (BASIC IDEA)
==========================================================================================================

Image:
- Read-only template
- Used to create containers

Example:
- mysql image
- nginx image
- node image

Think of image as:
"Blueprint of a house"

Container is:
"Actual house built from blueprint"

==========================================================================================================
6. DOCKER CONTAINERS
==========================================================================================================

Container:
- Running instance of an image
- Has its own:
  - File system
  - Network
  - Processes

Commands:
    docker ps        → running containers
    docker ps -a     → all containers
    docker stop      → stop container
    docker rm        → remove container

==========================================================================================================
7. DOCKER NETWORKING (VERY IMPORTANT)
==========================================================================================================

By default:
- Each container is isolated
- Containers cannot talk to each other

Why networking is needed?
- Frontend needs backend
- Backend needs database

Docker networking allows containers to communicate.

=====================================================
8. TYPES OF DOCKER NETWORKS
=====================================================

Docker supports multiple network types.

IMPORTANT ONES:

1) Host Network
---------------
- Container shares host network
- Same IP as host
- No port mapping needed

Example:
    Port 80 inside container = Port 80 on host

Pros:
- Fast
Cons:
- No isolation
- Security risk

2) Bridge Network (Default)
--------------------------
- Default Docker network
- Containers can talk to host
- Requires port mapping

Example:
    -p 8080:80

Host → 8080
Container → 80

3) User Defined Bridge (RECOMMENDED)
-----------------------------------
- Custom network created by user
- Containers communicate using container names
- Better DNS support

Example:
- mysql container reachable as "mysql"
- No IP needed

Best for:
- Microservices
- Multi-container apps

4) None Network
---------------
- No network access
- Fully isolated container

Use case:
- Security testing
- Offline jobs

ADVANCED NETWORKS (Mostly Docker Swarm):

5) MACVLAN
----------
- Assigns MAC address to container
- Appears as physical device

6) IPVLAN
---------
- Similar to MACVLAN but simpler routing

7) Overlay
----------
- Multi-host networking
- Used in Docker Swarm / Kubernetes

=====================================================
9. CHECK DOCKER NETWORKS
=====================================================

List networks:
    docker network ls

=====================================================
10. CREATE USER DEFINED NETWORK
=====================================================

Syntax:
    docker network create <name> -d <driver>

Example:
    docker network create myNetwork -d bridge

Why user-defined network?
- Automatic DNS resolution
- Containers talk by name
- Cleaner architecture

=====================================================
11. RUN CONTAINERS WITH CUSTOM NETWORK
=====================================================

MySQL Container:
---------------
    docker run -d \
    --name mysql \
    --network myNetwork \
    -e MYSQL_ROOT_PASSWORD=Root123 \
    -e MYSQL_DATABASE=dockerdev \
    mysql

Explanation:
- -d → detached mode
- --name → container name
- --network → attach to custom network
- -e → environment variables

React App Container:
-------------------
    docker run -d \
    -p 3030:5173 \
    --network myNetwork \
    -e MYSQL_HOST=mysql \
    -e MYSQL_USER=root \
    -e MYSQL_PASSWORD=Root123 \
    -e MYSQL_DATABASE=dockerdev \
    react-profile:latest

Important:
- MYSQL_HOST=mysql works because of custom network
- Container name acts as hostname

==========================================================================================================
12. DOCKER VOLUMES (DATA PERSISTENCE)
==========================================================================================================

Problem:
- Container data is temporary
- Removing container deletes data

Solution:
- Docker Volumes

Volume:
- External storage
- Managed by Docker
- Independent of container lifecycle

=====================================================
13. CHECK DOCKER VOLUMES
=====================================================

    docker volume ls

=====================================================
14. CREATE DOCKER VOLUME
=====================================================

    docker volume create mysql-data

=====================================================
15. INSPECT DOCKER VOLUME
=====================================================

    docker inspect mysql-data

Shows:
- Physical location on host
- Mount details

=====================================================
16. ATTACH VOLUME TO MYSQL CONTAINER
=====================================================

    docker run -d \
    --name mysql \
    --network myNetwork \
    -v mysql-data:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=Root123 \
    -e MYSQL_DATABASE=dockerdev \
    mysql

Explanation:
- mysql-data → volume name
- /var/lib/mysql → MySQL data directory

Result:
- Data persists even after container deletion

=====================================================
17. BIND MOUNT (HOST DIRECTORY)
=====================================================

Alternative to volumes.

Use local directory directly.

Example host path:
    /var/www/html/mysql

Command:
    docker run -d \
    --name mysql \
    --network myNetwork \
    -v /var/www/html/mysql:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=Root123 \
    -e MYSQL_DATABASE=dockerdev \
    mysql

Result:
- Data stored directly on host
- Easy backup
- Easy inspection

=====================================================
18. VOLUME VS BIND MOUNT
=====================================================

Volume:
- Managed by Docker
- Safer
- Portable

Bind Mount:
- Managed by user
- Direct access
- Depends on host path

=====================================================
19. WHEN TO USE WHAT?
=====================================================

Use Volume:
- Production
- Portability
- Clean management

Use Bind Mount:
- Development
- Debugging
- Local backups


==========================================================================================================
20. DOCKER COMPOSE (MULTI-CONTAINER MANAGEMENT)
==========================================================================================================
As applications grow, they usually require multiple services
to run together, such as:
- Frontend (React / Angular)
- Backend (Node / Laravel / FastAPI)
- Database (MySQL / PostgreSQL)
- Cache (Redis)
- Queue (RabbitMQ)

Managing all these using individual Docker commands becomes
difficult and error-prone.

=====================================================
21. PROBLEM WITHOUT DOCKER COMPOSE
=====================================================

Without Docker Compose, we manually run multiple commands:

- Build Docker image
    docker build -t app-name .

- Create Docker network
    docker network create myNetwork

- Create Docker volume
    docker volume create mysql-data

- Run database container
    docker run -d --name mysql --network myNetwork -v mysql-data:/var/lib/mysql ...

- Run application container
    docker run -d --name app --network myNetwork -p 3000:3000 ...

Problems with this approach:
- Too many commands to remember
- Order matters (network, volume first)
- Hard to manage in teams
- Difficult to restart entire setup
- Not version controlled properly

=====================================================
22. WHAT IS DOCKER COMPOSE?
=====================================================

Docker Compose is a tool that allows you to:
- Define
- Configure
- Run

multiple Docker containers using a **single YAML file**
called:

    docker-compose.yml

In simple words:
Docker Compose is a way to create and manage
**multiple related containers as one application**.

=====================================================
23. WHAT DOES docker-compose.yml CONTAIN?
=====================================================

The `docker-compose.yml` file is a combination of:
- Services (containers)
- Images or build instructions
- Networks
- Volumes
- Environment variables
- Port mappings
- Dependencies between services

Instead of writing multiple Docker commands,
we define everything in ONE file.

=====================================================
24. SINGLE COMMAND POWER OF DOCKER COMPOSE
=====================================================

With Docker Compose, all of the following can be done
using ONE command:

- Build images
- Create networks
- Create volumes
- Start containers
- Stop containers

Single command:
    docker compose up -d

Stop everything:
    docker compose down

=====================================================
25. BASIC STRUCTURE OF docker-compose.yml
=====================================================

A basic docker-compose.yml file contains:

- version (optional in newer versions)
- services
- networks (optional)
- volumes (optional)

High-level structure:

services:
  service-name:
    image / build
    ports
    environment
    volumes
    networks

=====================================================
26. EXAMPLE: MYSQL + APPLICATION USING DOCKER COMPOSE
=====================================================

Example docker-compose.yml:

-----------------------------------
version: "3.9"

services:

  mysql:
    image: mysql
    container_name: mysql
    environment:
      MYSQL_ROOT_PASSWORD: Root123
      MYSQL_DATABASE: dockerdev
    volumes:
      - mysql-data:/var/lib/mysql
    networks:
      - myNetwork

  app:
    image: react-profile:latest
    container_name: react-app
    ports:
      - "3030:5173"
    environment:
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: Root123
      MYSQL_DATABASE: dockerdev
    depends_on:
      - mysql
    networks:
      - myNetwork

volumes:
  mysql-data:

networks:
  myNetwork:
    driver: bridge
-----------------------------------

=====================================================
27. EXPLANATION OF ABOVE FILE
=====================================================

services:
- Defines all containers needed for the application

mysql service:
- Uses MySQL image
- Creates database automatically
- Stores data in Docker volume
- Connected to custom network

app service:
- Runs frontend/backend application
- Exposes port to host
- Connects to MySQL using service name
- Starts only after MySQL (depends_on)

volumes:
- Defines persistent storage
- Created automatically by Docker Compose

networks:
- Defines custom bridge network
- Created automatically

=====================================================
28. HOW TO RUN DOCKER COMPOSE
=====================================================

Step 1: Go to directory where docker-compose.yml exists
    cd project-folder

Step 2: Start containers
    docker compose up -d

Step 3: Check running containers
    docker compose ps

=====================================================
29. STOP AND REMOVE EVERYTHING
=====================================================

Stop containers:
    docker compose down

Stop + remove volumes:
    docker compose down -v

=====================================================
30. BENEFITS OF DOCKER COMPOSE
=====================================================

- Single command to manage entire application
- Clean and readable configuration
- Easy for teams to share
- Version controlled
- Less manual mistakes
- Perfect for development & testing

=====================================================
31. WHEN TO USE DOCKER COMPOSE
=====================================================

Use Docker Compose when:
- Multiple containers are required
- Local development
- Testing environments
- Small to medium projects
- Microservices on a single host

==========================================================================================================
32. DOCKER REGISTRY (IMAGE STORAGE & DISTRIBUTION)
==========================================================================================================

Docker Registry is a place where Docker images are stored,
shared, and downloaded.

In simple words:
Docker Registry is like GitHub, but for Docker images.

Instead of source code, it stores:
- Docker Images
- Different versions (tags) of images

=====================================================
33. WHY DO WE NEED A DOCKER REGISTRY?
=====================================================

Without a registry:
- Images exist only on your local system
- Cannot share images with team members
- Cannot deploy images to servers easily

With a registry:
- Build image once
- Push it to registry
- Pull it anywhere (server, cloud, CI/CD)

=====================================================
34. TYPES OF DOCKER REGISTRIES
=====================================================

1) Docker Hub (Public Registry)
-------------------------------
- Default Docker registry
- Maintained by Docker
- Free public repositories
- Paid private repositories

Example:
    mysql
    nginx
    node

Image format:
    username/image-name:tag

Example:
    rishabh/react-profile:latest

2) Private Registry
-------------------
- Hosted by organization
- More secure
- Used in enterprises

Examples:
- AWS ECR
- Azure Container Registry
- Google Artifact Registry
- Self-hosted registry

=====================================================
35. DOCKER HUB WORKFLOW
=====================================================

Typical image workflow:

1. Build image locally
2. Tag image
3. Push image to registry
4. Pull image on another machine
5. Run container

=====================================================
36. LOGIN TO DOCKER REGISTRY
=====================================================

Login to Docker Hub:
    docker login

You will be asked for:
- Docker Hub username
- Password / Access Token

=====================================================
37. TAG DOCKER IMAGE
=====================================================

Before pushing, image must be tagged.

Syntax:
    docker tag <local-image> <username>/<image-name>:<tag>

Example:
    docker tag react-profile rishabh/react-profile:latest

=====================================================
38. PUSH IMAGE TO DOCKER REGISTRY
=====================================================

Push image:
    docker push rishabh/react-profile:latest

Now image is available in Docker Hub.

=====================================================
39. PULL IMAGE FROM REGISTRY
=====================================================

On any machine:
    docker pull rishabh/react-profile:latest

=====================================================
40. BENEFITS OF DOCKER REGISTRY
=====================================================

- Centralized image storage
- Easy collaboration
- CI/CD integration
- Version control using tags
- Faster deployments

=====================================================
41. REAL-WORLD USE CASE
=====================================================

Developer:
- Builds image
- Pushes to registry

Server:
- Pulls image
- Runs container

CI/CD:
- Automatically builds & pushes image
- Automatically deploys

==========================================================================================================
42. MULTI-STAGE DOCKER BUILDS
==========================================================================================================

Multi-stage Docker build is an advanced Dockerfile technique
used to:
- Reduce image size
- Improve security
- Optimize build process

It allows multiple `FROM` statements
inside a single Dockerfile.

=====================================================
43. PROBLEM WITH NORMAL DOCKERFILE
=====================================================

In a normal Dockerfile:
- Build tools stay inside final image
- Image becomes large
- Unnecessary files included

Example problems:
- Node modules build cache
- Compilers
- Temporary files

=====================================================
44. WHAT IS MULTI-STAGE BUILD?
=====================================================

Multi-stage build divides Dockerfile into stages:

- Stage 1: Build stage
- Stage 2: Runtime stage

Only required output is copied
from build stage to final image.

=====================================================
45. BASIC MULTI-STAGE DOCKERFILE STRUCTURE
=====================================================

General format:

-----------------------------------
FROM base-image AS builder
# build steps

FROM runtime-image
# copy required files from builder
-----------------------------------

Each `FROM` keyword starts a new stage.

=====================================================
46. EXAMPLE: MULTI-STAGE NODE / REACT BUILD
=====================================================

-----------------------------------
# Stage 1: Build stage
FROM node:18 AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Runtime stage
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
-----------------------------------

=====================================================
47. EXPLANATION OF ABOVE DOCKERFILE
=====================================================

Stage 1 (builder):
- Uses Node image
- Installs dependencies
- Builds application
- Contains build tools (not needed later)

Stage 2 (runtime):
- Uses lightweight nginx image
- Copies only final build output
- No node_modules
- No build tools

=====================================================
48. BENEFITS OF MULTI-STAGE BUILDS
=====================================================

- Smaller image size
- Faster container startup
- Better security
- Clean production image
- Separation of build & runtime

=====================================================
49. MULTI-STAGE BUILD WITH PYTHON (EXAMPLE)
=====================================================

-----------------------------------
# Stage 1: Builder
FROM python:3.11 AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user -r requirements.txt

COPY . .

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

ENV PATH=/root/.local/bin:$PATH

CMD ["python", "main.py"]
-----------------------------------

=====================================================
50. WHEN TO USE MULTI-STAGE BUILDS
=====================================================

Use multi-stage builds when:
- Application needs compilation/build
- You want small production images
- Security is important
- CI/CD pipelines are used

=====================================================
51. DOCKER REGISTRY vs DOCKER COMPOSE vs MULTI-STAGE
=====================================================

Docker Registry:
- Stores and distributes images

Docker Compose:
- Runs multiple containers together

Multi-stage Build:
- Optimizes how images are built

















=====================================================
END OF DOCUMENT
=====================================================

