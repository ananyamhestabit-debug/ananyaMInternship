# Multi-Container Application – Day 2

## Overview

This project demonstrates a multi-container application using Docker Compose.
It includes three services:

1. Client – React application (Frontend)
2. Server – Node.js + Express API (Backend)
3. MongoDB – Database

All services are deployed using a single command:

docker compose up -d

---

## Services Description

### 1. Client (React)
- Runs on port 3000
- Provides frontend interface
- Communicates with the backend server

### 2. Server (Node + Express)
- Runs on port 5000
- Connects to MongoDB using container networking
- Handles API requests

Mongo connection string used:

mongodb://mongo:27017/testdb

Here, "mongo" is the service name and acts as the hostname inside Docker network.

### 3. MongoDB
- Runs internally on port 27017
- Uses a named volume for persistent storage
- Not exposed to host machine (internal communication only)

---

## Docker Networking

Docker Compose automatically creates a default bridge network.
All services can communicate using their service names.

Example:
Server connects to Mongo using hostname "mongo".

This eliminates the need for manual IP configuration.

---

## Volumes

MongoDB uses a named volume:

mongo-data

This ensures that database data persists even if the container is removed or restarted.

---

## Logs Verification

Logs were verified using:

docker logs server
docker logs client
docker logs mongo

Server logs confirmed successful MongoDB connection.

---

## Conclusion

This setup successfully demonstrates:

- Multi-container orchestration
- Container networking
- Persistent storage using volumes
- Centralized deployment using Docker Compose