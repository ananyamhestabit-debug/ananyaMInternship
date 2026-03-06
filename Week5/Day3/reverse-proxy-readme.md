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

---

## Deployment

All services started using:

docker compose up -d

---

## Verification

Accessed:
http://localhost:8080/api

Refreshing the page showed alternating responses from backend1 and backend2, confirming load balancing.