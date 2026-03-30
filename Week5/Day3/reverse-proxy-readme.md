# Reverse Proxy & Load Balancing – Day 3

## Overview

This project demonstrates NGINX as a reverse proxy with load balancing.

Two backend Node.js services are deployed:
- backend1
- backend2

NGINX routes incoming requests to backend services using round-robin load balancing.

---

## Architecture

Client → NGINX → Backend1 / Backend2

NGINX listens on port 8080 and forwards /api requests to backend containers.

---

## Load Balancing

Round-robin is enabled using the upstream directive:

upstream backend_servers {
    server backend1:3000;
    server backend2:3000;
}

Each request is forwarded alternately between backend instances.


## Deployment

All services started using:

docker compose up -d


## Verification

Accessed:
http://localhost:8080/api

Refreshing the page showed alternating responses from backend1 and backend2, confirming load balancing.

### <--------- Commands in depth for me ----------->
# Reverse Proxy & Load Balancing – Day 3

## Overview

This project demonstrates NGINX as a reverse proxy with load balancing.

Two backend Node.js services:
- backend1
- backend2

NGINX distributes traffic between them.

## Architecture

Client → NGINX → Backend1 / Backend2


## Run Commands

### 1. Start Application
docker compose up -d --build
### Output:
Containers are created and started:
- backend1
- backend2
- nginx

### 2. Check Running Containers
docker ps

### Output:
Shows running containers:
backend1  
backend2  
nginx  

### 3. Access API

http://localhost:8080/api

### Output Example:
Response from 28e37284d004  

After refresh:
Response from a1b2c3d4e5f6  
--> Different IDs confirm load balancing


### 4. Check Logs

docker logs backend1  
docker logs backend2  
docker logs nginx  

### Output:
Backend servers show incoming requests  
NGINX logs routing activity  

### 5. Stop Application
docker compose down

## Services Description

### Backend
- Node.js app running on port 3000
- Returns container hostname
- Helps identify which server handled request

### NGINX
- Reverse proxy
- Runs on port 8080
- Routes /api requests to backend servers

## NGINX Configuration

upstream backend_servers {
    server backend1:3000;
    server backend2:3000;
}

server {
    listen 80;

    location /api {
        proxy_pass http://backend_servers;
    }
}

## Load Balancing
NGINX uses round-robin by default.
Requests flow like:
backend1 -> backend2 -> backend1 -> backend2


## Data Flow
Browser → localhost:8080/api  
 |  
NGINX  
 |
backend_servers (backend1/backend2)  
 | 
Response  

 ### remove severy conatiner:
 docker rm -f $(docker ps -aq) 
