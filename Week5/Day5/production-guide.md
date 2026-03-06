# Production Deployment Guide

## Overview

This setup demonstrates a production-style Docker deployment using:

- Docker Compose
- NGINX reverse proxy
- HTTPS with self-signed certificates
- Health checks
- Restart policies
- Deployment automation

## Environment Configuration

Secrets are stored in `.env` file.

## Deployment

Run:

./deploy.sh

This will start the production stack using docker-compose.prod.yml.

## Services

Backend: Node.js application  
Reverse Proxy: NGINX with HTTPS

## Health Check

Backend service includes a health check using curl to verify availability.

## Logging

Log rotation is configured to prevent large log files.