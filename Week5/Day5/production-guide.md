# Production Deployment Guide (Day 5)

## Overview

This project demonstrates a production-style deployment using Docker.

It includes:

- Backend (Node.js)
- NGINX reverse proxy
- HTTPS using SSL (mkcert)
- Health checks
- Restart policies
- Log rotation
- Deployment automation (script)


## Prerequisites

Before running:

- Docker installed
- Docker Compose installed
- SSL certificates already created (Day 4)
- /etc/hosts configured:

127.0.0.1 app.local

## Step-by-Step Deployment

### Step 1: Navigate to project

cd Week5/Day5

###  Step 2: Stop old containers (IMP.)
If Day 4 containers are running:
sudo docker rm -f day4-nginx-1 day4-backend-1

###  Step 3: Make deploy script executable

chmod +x deploy.sh

### Step 4: Run deployment
./deploy.sh
(->Stops existing containers:
docker compose -f docker-compose.prod.yml down
->Starts production containers:
docker compose -f docker-compose.prod.yml up -d)

## What deploy.sh does

1. Stops existing containers:
docker compose -f docker-compose.prod.yml down

2. Starts production containers:
docker compose -f docker-compose.prod.yml up -d


## Verification

### Check running containers

docker ps
Expected:
- backend running
- nginx running


### Check logs

docker logs day5-backend-1
Expected:
Backend running on port 3000


### Check HTTP -> HTTPS redirect(All traffic forced to HTTPS)

curl -I http://app.local
Expected:
HTTP/1.1 301 Moved Permanently

### Check HTTPS response
curl -I https://app.local
Expected:
HTTP/1.1 200 OK

## Access Application

Open in browser:

https://app.local

Expected output:
Production stack working with Docker


## Features Implemented

### Reverse Proxy (NGINX)

Routes traffic to backend container.

### HTTPS (SSL)

- Using mkcert
- Secure communication enabled

---

### HTTP → HTTPS Redirect

All HTTP traffic is redirected to HTTPS.

### Health Check

healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000"]


### Restart Policy
command-> docker compose -f docker-compose.prod.yml restart backend

restart: always(Restart policy "always" ensures containers restart on failure or system restart, but not when manually stopped by the user.)


### Log Rotation

logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"

### Environment Variables (.env)

APP_DOMAIN=app.local  
NODE_ENV=production  

## Conclusion

This setup simulates a real production deployment environment with:

- Secure HTTPS setup
- Automated deployment
- Container health monitoring
- Scalable architecture using Docker