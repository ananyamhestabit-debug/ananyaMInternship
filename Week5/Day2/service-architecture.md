# Multi-Container Application – Day 2

## Overview

This project demonstrates a multi-container application using Docker Compose.

It includes:
- React Client (Frontend)
- Node.js Server (Backend)
- MongoDB Database

All services run using a single command.

---

## Run Commands

### Start Application
docker compose up -d --build


### Stop Application
docker compose down


### Check Running Containers
docker ps


### View Logs
docker logs server
docker logs client
docker logs mongo


## Services Description
### 1. Client (React)
- Runs on port 3000
- Displays UI in browser
- Connects to backend

### 2. Server (Node + Express)
- Runs on port 5000
- Connects to MongoDB
- Handles API requests

Mongo Connection:
mongodb://mongo:27017/testdb
### "mongo" is the service name used as hostname.

### 3. MongoDB
- Internal container database
- Uses volume for data persistence
- Not exposed to host

---

## Docker Networking

Docker Compose automatically creates a network.

All services communicate using service names.

Example:

### server-->mongo
No IP address needed.


## Volumes
MongoDB uses:

### mongo-data
This ensures:
- Data is not lost after container restart
- Persistent storage


## Logs Verification
Verified using-->
docker logs server
Output:
Mongo Connected


## Final Result
Multi-container app working  
Backend connected to database  
Frontend running  
Logs verified  
Data persistence working  

---

## Conclusion

This setup demonstrates:
- Docker Compose orchestration
- Multi-container architecture
- Networking between containers
- Persistent storage using volumes