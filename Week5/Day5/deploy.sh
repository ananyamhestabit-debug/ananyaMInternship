#!/bin/bash

echo "Starting production deployment..."

docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d

echo "Deployment finished."